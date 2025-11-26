from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any

# --- Request Model ---
# This is what the Frontend MUST send to /api/generate-report
class ReportRequest(BaseModel):
    git_id: str = Field(..., description="The developer's GitHub/GitLab username", example="torvalds")
    repo_url: HttpUrl = Field(..., description="The full URL of the target repository", example="https://github.com/fastapi/fastapi")
    auth_token: Optional[str] = Field(None, description="Optional GitHub PAT for accessing private repos")
    user_id: str = Field(..., description="The ID of the hiring manager requesting the report")

# --- Response Models ---
# These define the structured data we return to the UI

class DeveloperProfileSummary(BaseModel):
    top_languages: List[Dict[str, Any]]
    contribution_style: str
    tech_focus: List[str]

class CodebaseContextSummary(BaseModel):
    languages: List[Dict[str, Any]]
    high_churn_files: List[str]
    complexity_hotspots: List[str]

class ReportResponse(BaseModel):
    success: bool
    report_id: Optional[str] = None
    markdown_content: str = Field(..., description="The full LLM generated report in Markdown")
    sources: Optional[List[Dict[str, str]]] = None
    error: Optional[str] = None

    # We also include the raw data used, in case the UI wants to show graphs later
    developer_summary: Optional[DeveloperProfileSummary] = None
    codebase_summary: Optional[CodebaseContextSummary] = None