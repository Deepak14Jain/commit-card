# Contributing to Commit Card

First off, thanks for taking the time to contribute! 🎉

Commit Card is an open-source project, and we welcome contributions from the community. Whether it's fixing bugs, improving the documentation, or proposing new features, your help is appreciated.

### ⚡ Quick Start for Developers

- Fork the repository on GitHub.

- Clone your fork locally.

- Set up your environment (see the README for full setup instructions).

Create a branch for your feature or fix.

### Project Structure

To help you navigate the codebase, here is a brief overview of the backend structure in src/:

- `main.py`: The entry point. This is where FastAPI is initialized and routes are defined.

- `schemas.py`: Pydantic models. If you are changing the API input/output, start here.

- `orchestration/`: The "Business Logic" layer. The manager.py file controls the flow of data.

- `data_extraction/`:

    - `git_extractor.py`: Logic for fetching developer profiles.

    - `repo_analyzer.py`: Logic for analyzing target codebases.

- `llm/`: Contains the prompt engineering and Gemini API client.

### Development Workflow

1. **Create a Branch**
    Create a descriptive branch name for your changes:
    ```
    git checkout -b feature/improved-repo-analysis
    # or
    git checkout -b fix/api-timeout-bug
    ```

2. **Coding Standards**
**Type Hinting:** We use Python type hints strictly. Ensure function signatures are typed.
**Async:** The core architecture is asynchronous (async/await). Please preserve this pattern to ensure performance.
**Environment Variables:** Never hardcode secrets. Always use os.getenv and add new keys to `.env`.

3. **Testing**
Before submitting, run the application locally and verify that the API generates a report successfully.
    ```
    uvicorn src.main:app --reload
    ```
    > Note: We are working on adding a comprehensive pytest suite.

4. **Commit Messages**
We follow a rough "Conventional Commits" style:
    - `feat: Add support for GitLab repositories`
    - `fix: Handle rate limit errors from GitHub API`
    - `docs: Update setup instructions`

### Security

**CRITICAL**: Never commit the `firebase_key.json` or your `.env` file. These contain sensitive credentials.
If you accidentally commit them, you must revoke the keys immediately and rotate your credentials.

### Pull Request Process
1. Push your branch to your fork.

2. Open a Pull Request against the main branch of the original repository.

3. Provide a clear description of what your changes do.

4. If your PR changes the API contract, please update the Pydantic models in models.py.

---

### Community

If you have questions, feel free to open a Discussion or an Issue on GitHub. We want to make contributing as easy as possible!