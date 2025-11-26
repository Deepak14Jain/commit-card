import asyncio
from typing import Optional

# Import our data models
from src.models import ReportResponse

# Import the modules we will build next
# (These imports will fail until we create the files in the next steps)
from src.data_extraction.git_extractor import extract_developer_profile
from src.data_extraction.repo_analyzer import analyze_repo_context
from src.llm.client import generate_hiring_report
from src.persistence.firestore import save_report_to_firestore

async def orchestrate_report_generation(
    git_id: str,
    repo_url: str,
    auth_token: Optional[str],
    user_id: str
) -> ReportResponse:
    """
    Coordinator function that runs the full pipeline:
    Extraction -> Synthesis -> Persistence -> Response
    """
    print(f"🎼 Orchestrator started for {git_id} -> {repo_url}")

    try:
        # --- Step 1: Parallel Data Extraction ---
        # We run both extractors at the same time to save speed.
        # asyncio.gather allows concurrent execution.
        
        print("⏳ Step 1: Fetching data from GitHub...")
        
        # Launch both tasks
        dev_task = asyncio.create_task(extract_developer_profile(git_id))
        repo_task = asyncio.create_task(analyze_repo_context(repo_url, auth_token))

        # Wait for both to finish
        dev_profile, repo_context = await asyncio.gather(dev_task, repo_task)

        # Check for failures in extraction
        if not dev_profile or not repo_context:
            error_msg = "Failed to extract data."
            if not dev_profile: error_msg += f" Could not find user {git_id}."
            if not repo_context: error_msg += f" Could not access repo {repo_url}."
            
            return ReportResponse(
                success=False,
                markdown_content="",
                error=error_msg
            )

        print("✅ Step 1 Complete: Data received.")

        # --- Step 2: LLM Synthesis ---
        print("⏳ Step 2: Sending data to Gemini LLM...")
        
        llm_result = await generate_hiring_report(dev_profile, repo_context)

        if not llm_result:
            return ReportResponse(
                success=False,
                markdown_content="",
                error="LLM Generation failed. Please try again."
            )

        print("✅ Step 2 Complete: Report generated.")

        # --- Step 3: Persistence ---
        print("⏳ Step 3: Saving to Firestore...")
        
        # We assume llm_result is a dictionary containing 'text' and 'sources'
        full_report_data = {
            "git_id": git_id,
            "repo_url": repo_url,
            "report_markdown": llm_result.get("text", ""),
            "sources": llm_result.get("sources", []),
            "developer_summary": dev_profile.dict(), # Save raw data for debugging/graphs
            "codebase_summary": repo_context.dict()
        }

        report_id = save_report_to_firestore(full_report_data, app_id="commit-card", user_id=user_id)
        
        print(f"✅ Step 3 Complete. Report ID: {report_id}")

        # --- Step 4: Final Response ---
        return ReportResponse(
            success=True,
            report_id=str(report_id) if report_id else None,
            markdown_content=llm_result.get("text", ""),
            sources=llm_result.get("sources", []),
            developer_summary=dev_profile, # We return these so the UI can show charts if needed
            codebase_summary=repo_context
        )

    except Exception as e:
        print(f"❌ Orchestrator Error: {e}")
        return ReportResponse(
            success=False,
            markdown_content="",
            error=str(e)
        )