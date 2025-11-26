# Commit Card

Commit Card is an open-source intelligence tool that matches a developer's Git history to a company's codebase needs.

It moves beyond simple keyword matching by using Large Language Models (LLMs) to synthesize a "Developer Profile" (from public Git activity) against a "Codebase Context" (from the target repository) to generate an actionable hiring fit report.

---

### Features

- **Dual-Pronged Analysis:**

    - **Developer Scanner:** Fetches public contribution history, language proficiency, and technical focus areas from GitHub.

    - **Repo Context Analyzer:** Analyzes target repositories for language distribution, high-churn files, and potential complexity hotspots.

- **AI Synthesis:** Uses Google Gemini 2.5 Flash to generate a human-readable "Fit Assessment" report.

- **Actionable Insights:** Suggests the best "First Project" for a candidate and identifies potential skill gaps.

- **History & Persistence:** Stores generated reports in Firebase Firestore for team sharing and historical tracking.

### 🛠️ Tech Stack

- Backend: Python 3.10+, FastAPI

- AI/LLM: Google Gemini API (gemini-2.5-flash-preview)

- Database: Firebase Firestore (NoSQL)

- Data Extraction: httpx, GitPython

- Validation: Pydantic

### Installation & Setup

**Prerequisites**

- Python 3.9 or higher

- A Google Cloud Project with the Gemini API enabled.

- A Firebase Project with Firestore enabled.

- A GitHub Account (for API tokens).

**Clone the Repository**

```
git clone https://github.com/Deepak14Jain/commit-card.git
cd commit-card
```

**Install Dependencies**
```
# Recommended: Create a virtual environment
python -m venv .venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

**Configuration**

Create a `.env` file in the root directory. Do not commit this file.

```
# Google Gemini API Key
GOOGLE_API_KEY="your_gemini_api_key_here"

# GitHub Token (Optional but recommended for higher rate limits)
GITHUB_TOKEN="your_github_pat_here"

# Firebase Credentials File Path
FIREBASE_CREDENTIALS_PATH="firebase_key.json"

# App Settings
APP_ENV="development"
PORT=8000
```

**Firebase Setup**

- Download your Service Account JSON key from the Firebase Console.

- Rename it to firebase_key.json.

- Place it in the root directory of the project.

- Ensure firebase_key.json is in your .gitignore.

## 🏃‍♂️ Running the Application

- Start the FastAPI server using Uvicorn:
    ```
    uvicorn src.main:app --reload
    ```
- The API will be available at http://localhost:8000.

### API Documentation

Once the server is running, visit the interactive Swagger UI to test endpoints:

- Swagger UI: http://localhost:8000/docs

- ReDoc: http://localhost:8000/redoc

### Architecture

The backend follows a Single-Service Monolith pattern for simplicity and speed:

- `src/main.py`: API Entry point.

- `src/orchestration/`: Coordinates data fetching and LLM synthesis.

- `src/data_extraction/`: Modules for GitHub API and Code Analysis.

- `src/llm/`: Client for interacting with Google Gemini.

- `src/persistence/`: Firestore database logic.

### License

This project is licensed under the MIT License - see the LICENSE file for details.