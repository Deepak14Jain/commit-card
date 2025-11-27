# Stop Matching Keywords, Start Matching Context: Introducing Commit Card 

> Hiring developers is hard. Understanding where they fit in your codebase is harder.

We’ve all seen it happen: A candidate looks perfect on paper. Their resume is a soup of matching keywords—React, Python, AWS. You hire them, but three months later, they are struggling. Not because they aren't talented, but because their style doesn't match your needs.

Maybe you hired a "Greenfield Cowboy" (great at starting from scratch) for a legacy refactoring job. Maybe you hired a "Scripting Wizard" for a complex distributed systems role.

Keywords don't capture this. **Context** does.

That’s why I built Commit Card—an open-source intelligence tool that uses LLMs to bridge the gap between a developer's proven history and a codebase's actual needs.

---

### The Big Idea

Commit Card isn't another resume scanner. It’s a Technical Fit Analyzer.

It takes two inputs:

- The Developer: A GitHub ID (e.g., torvalds).

- The Context: A Target Repository URL (e.g., your-company/legacy-backend).

It doesn't just check if the languages match. It uses Google's Gemini 2.5 Flash model to synthesize a deep, qualitative report. It answers questions like:

> "This developer writes high-churn refactors; can they handle our technical debt?"

> "They have 500 commits in C++ memory management; are they the right person to fix our segmentation faults?"

### Under the Hood: The Architecture

I wanted Commit Card to be fast, modular, and easy to contribute to. I chose a Single-Service Monolith architecture for the backend to keep operational overhead low and development speed high.

#### The Stack

- **Backend**: Python & FastAPI (for high-performance async orchestration).

- **Brain**: Google Gemini 2.5 Flash (via the google-generativeai SDK).

- **Memory**: Firebase Firestore (NoSQL storage for reports).

- **Data**: httpx and GitPython for extraction.

#### The Workflow

Here is what happens when you hit the `/generate-report` endpoint:

**The Orchestrator**: The request hits src/orchestration/manager.py. This module acts as the traffic controller. It immediately spins up two parallel asynchronous tasks.

**The Eyes (Extraction Layer)**:

- Developer Extractor: Hits the GitHub API to fetch the user's recent contribution history, calculating metrics like "Language Entropy" and "Commit Frequency."

- Repo Analyzer: Scans the target repository. Instead of a heavy clone, it uses smart API heuristics to identify "High Churn Files" (files changed most often) and "Complexity Hotspots."

**The Synthesis (LLM Layer)**: Once the data is ready, it is passed to the Gemini 2.5 Flash model. We use a structured "Senior Architect" system prompt to force the LLM to think critically about fit, not just summarize data.

**The Persistence**: The final report is saved to Firestore, generating a unique ID so it can be shared with your hiring team.

### Why Gemini 2.5?

For this specific use case, speed is everything. A user waiting for a report doesn't want to wait 45 seconds.

Gemini 2.5 Flash proved to be the perfect balance. It handles the large context window (JSON dumps of repo stats can get big) effortlessly and returns structured Markdown analysis in seconds.

### Identifying the "First Project"

One of my favorite features is the **"Recommended First Assignment"** section of the report.

Instead of generic advice, Commit Card tries to match the developer's specific strength to a repository's specific weakness.

> Example Output:
The candidate has extensive experience in Python Unit Testing. Given that your repository's /tests/ directory has seen zero activity in 6 months despite high churn in /src/, the ideal first project is to stabilize the payment module by increasing test coverage.

---

### 🤝 Call for Contributors

Commit Card is currently a robust Backend API. The logic is sound, the LLM is smart, and the database is connected.

But we need a Frontend.

I am looking for open-source contributors who want to help build the UI. Whether you are a React pro, a Vue enthusiast, or a Tailwind master, I’d love your help to visualize this data.

We also need help with:

- Better Static Analysis: Improving the repo_analyzer.py to detect more code smells without cloning.

- Prompt Engineering: Refining the system prompts for even sharper insights.

### Get Involved

The project is live on GitHub.

- Clone it.

- Generate your API keys.

- Run the analysis.

Let's move hiring from "Keyword Matching" to "Context Matching." 🃏