import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

# Import our data models
from src.models import ReportRequest, ReportResponse

# Import the core logic (We will build this file next)
from src.orchestration.manager import orchestrate_report_generation

# --- 1. Setup & Configuration ---
load_dotenv()  # Load variables from .env

# Lifecycle manager (optional, but good practice for DB connections)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (e.g., connect to DB)
    print("🚀 Commit Card Backend starting up...")
    yield
    # Shutdown logic
    print("🛑 Commit Card Backend shutting down...")

app = FastAPI(
    title="Commit Card API",
    description="Analyzes developer fit for a specific codebase using LLMs.",
    version="1.0.0",
    lifespan=lifespan
)

# --- 2. Security (CORS) ---
# Allow the frontend to talk to this backend
origins = [
    "http://localhost:3000", # Common React/Frontend port
    "http://127.0.0.1:3000",
    "*"                      # Allow all for development convenience
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. Routes ---

@app.get("/health")
async def health_check():
    """Simple health check to ensure server is running."""
    return {"status": "active", "environment": os.getenv("APP_ENV", "unknown")}

@app.post("/api/generate-report", response_model=ReportResponse)
async def generate_report_endpoint(request: ReportRequest):
    """
    Main Endpoint: Receives Git ID and Repo URL, returns the LLM analysis.
    """
    try:
        print(f"📥 Received request: Developer={request.git_id}, Repo={request.repo_url}")
        
        # Delegate the heavy lifting to the Orchestration Layer
        result = await orchestrate_report_generation(
            git_id=request.git_id,
            repo_url=str(request.repo_url),
            auth_token=request.auth_token,
            user_id=request.user_id
        )

        # Check for logical errors returned by the orchestrator
        if not result.success:
             raise HTTPException(status_code=500, detail=result.error)

        return result

    except Exception as e:
        # Catch unexpected server crashes
        print(f"❌ Critical Error in Main: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run the server directly for debugging
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)