import uvicorn
from fastapi import FastAPI, HTTPException

# Adjust imports to be relative to the project root for when the API is run as a module
# This will be refined as we integrate more modules.
try:
    from autoprojectmanagement.services.cli_commands import CLICommands
except ImportError:
    # This allows running the script directly for development, 
    # assuming the parent directory is in the Python path.
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from autoprojectmanagement.services.cli_commands import CLICommands


# Create a FastAPI app instance
app = FastAPI(
    title="AutoProjectManagement API",
    description="API for the Automated Project Management System.",
    version="1.0.0",
)

# Create an instance of the command handler to access the business logic
# This is a temporary step. In the future, we will call the logic more directly.
cli_commands = CLICommands()


@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the AutoProjectManagement API!"}


# --- API Version 1 ---

@app.get("/api/v1/projects/{project_id}/status", tags=["Projects"])
def get_project_status(project_id: str, format: str = 'json'):
    """
    Get the status of a specific project.
    This is the first endpoint to be migrated from the CLI.
    """
    # We directly call the existing logic from cli_commands.
    # In the future, this logic will be better integrated into services
    # that are independent of the CLI.
    status_data = cli_commands.get_project_status(project_id, format)
    
    if not status_data:
        raise HTTPException(status=404, detail=f"Project '{project_id}' not found.")
        
    if format == 'json':
        # The get_project_status for 'json' might return a string. We ensure it's a dict.
        import json
        try:
            return json.loads(status_data)
        except (json.JSONDecodeError, TypeError):
            # If it's not a valid JSON string, wrap it.
            return {"status_data": status_data}

    return {"status_data": status_data}


# --- Main execution block ---

def start():
    """
    A function to start the uvicorn server.
    This can be called from a separate script or via `python -m autoprojectmanagement.api.main`.
    """
    uvicorn.run("autoprojectmanagement.api.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    start()