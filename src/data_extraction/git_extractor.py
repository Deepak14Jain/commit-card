import os
import httpx
from collections import Counter
from typing import Optional, List, Dict, Any
from src.models import DeveloperProfileSummary

# GitHub API Base URL
GITHUB_API_BASE = "https://api.github.com"

async def extract_developer_profile(git_id: str) -> Optional[DeveloperProfileSummary]:
    """
    Fetches public data for a GitHub user and aggregates their technical profile.
    """
    
    # 1. Setup Auth (Important for Rate Limits)
    # Even for public data, unauthenticated requests are limited to 60/hr.
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Commit-Card-App"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    print(f"🔍 [GitExtractor] Fetching profile for: {git_id}")

    async with httpx.AsyncClient() as client:
        try:
            # --- Step A: Verify User & Get Basic Info ---
            user_resp = await client.get(f"{GITHUB_API_BASE}/users/{git_id}", headers=headers)
            
            if user_resp.status_code == 404:
                print(f"❌ User {git_id} not found.")
                return None
            elif user_resp.status_code != 200:
                print(f"❌ GitHub API Error: {user_resp.text}")
                return None

            user_data = user_resp.json()
            public_repos_count = user_data.get("public_repos", 0)

            # --- Step B: Fetch Repositories (Limit to top 30 recently updated) ---
            # We sort by updated to get their *current* skills, not what they did 5 years ago.
            params = {"sort": "updated", "direction": "desc", "per_page": 30}
            repos_resp = await client.get(f"{GITHUB_API_BASE}/users/{git_id}/repos", headers=headers, params=params)
            
            if repos_resp.status_code != 200:
                print(f"❌ Failed to fetch repos for {git_id}")
                return None

            repos = repos_resp.json()

            # --- Step C: Aggregate Metrics ---
            language_counter = Counter()
            topics = []
            total_stars = 0
            
            for repo in repos:
                # 1. Languages
                lang = repo.get("language")
                if lang:
                    # We weight the language by the size of the repo (size is in KB)
                    # This prevents a "Hello World" in Java counting the same as a massive Python app.
                    weight = repo.get("size", 1) // 100 # Simple weighting heuristic
                    if weight < 1: weight = 1
                    language_counter[lang] += weight

                # 2. Tech Focus (Topics)
                repo_topics = repo.get("topics", [])
                topics.extend(repo_topics)
                
                # 3. Stars (Proxy for quality/impact)
                total_stars += repo.get("stargazers_count", 0)

            # --- Step D: Format Output ---
            
            # 1. Top Languages
            top_langs = [
                {"name": lang, "score": count} 
                for lang, count in language_counter.most_common(3)
            ]

            # 2. Tech Focus (Top 5 keywords)
            top_topics = [t[0] for t in Counter(topics).most_common(5)]

            # 3. Contribution Style (Heuristic based on data)
            style_desc = f"Maintains {public_repos_count} public repos with {total_stars} total stars."
            if not top_langs:
                style_desc += " No language data available."
            else:
                primary_lang = top_langs[0]['name']
                style_desc += f" Heavily focused on {primary_lang} development."
            
            if user_data.get("hireable"):
                style_desc += " Explicitly marked as 'Hireable' on GitHub."

            print(f"✅ [GitExtractor] Success for {git_id}")
            
            return DeveloperProfileSummary(
                top_languages=top_langs,
                contribution_style=style_desc,
                tech_focus=top_topics
            )

        except Exception as e:
            print(f"❌ [GitExtractor] Exception: {e}")
            return None