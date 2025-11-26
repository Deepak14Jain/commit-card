import os
import google.generativeai as genai
from typing import Dict, Any, Optional

# Import the Pydantic models for type hinting
from src.models import DeveloperProfileSummary, CodebaseContextSummary

async def generate_hiring_report(
    dev_profile: DeveloperProfileSummary, 
    repo_context: CodebaseContextSummary
) -> Optional[Dict[str, Any]]:
    """
    Synthesizes the developer profile and codebase context into a hiring report.
    """
    
    # 1. Setup API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        return None

    genai.configure(api_key=api_key)

    # 2. Configure the Model
    # We use 'gemini-1.5-flash' for high speed and low cost, perfect for summarization.
    model = genai.GenerativeModel('models/gemini-2.5-flash-preview-09-2025')

    # 3. Construct the Prompt
    # We convert Pydantic models to dicts for clean JSON formatting
    dev_json = dev_profile.model_dump_json(indent=2)
    repo_json = repo_context.model_dump_json(indent=2)

    system_instruction = (
        "You are a Senior Engineering Architect. Your goal is to assess if a developer "
        "is a good fit for a specific codebase based on their contribution history and the "
        "codebase's current needs.\n\n"
        "Input Data:\n"
        f"--- Developer Profile ---\n{dev_json}\n\n"
        f"--- Codebase Context ---\n{repo_json}\n\n"
        "Task:\n"
        "Generate a report in Markdown format. Do not use JSON in the output.\n"
        "Structure the report exactly as follows:\n"
        "1. **Core Fit Assessment**: A honest summary (Strong/Moderate/Weak) with reasoning.\n"
        "2. **Immediate Impact**: Recommend a specific file or module they should work on first.\n"
        "3. **Strategic Value**: Where can they help in the long run?\n"
        "4. **Potential Risks**: Gaps in their stack vs the repo's stack."
    )

    try:
        # 4. Call the API
        # functionality: "google_search_retrieval" could be added here if needed for deeper context
        response = model.generate_content(system_instruction)

        # 5. Extract Text
        if response.text:
            return {
                "text": response.text,
                "sources": [] # Standard Gemini text generation usually doesn't return sources unless using grounding tools
            }
        else:
            return None

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return None