# Module: aegis-code/api/server.py

from typing import Dict
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI(
    title="Aegis Code API",
    description="API for the multi-agent code modernizaion and PR review system.",
    version="0.1.0",
)


@app.get("/health", tags=["Status"])
async def health_check() -> Dict[str, str]:
    """
    Provides a simple health check of the API server.

    This endpoint can be used by monitoring services (like AWS APP runner's health checks)
    to verify that the application is running and responsive.

    Returns:
        A dictionary indiating the operational status of the service.
    """
    return {"status": "ok"}


@app.post("/modernize-codebase", tags=["Workflows"])
async def modernize_codebase() -> Dict[str, str]:
    """
    Endpoint to trigger the codebase modernization workflow.

    Accepts details about a target respository
    and initiate the LangGraph-based modernization team.

    Returns:
        A dictionary confirming that the process has been initiated.

    """

    return {"message": "Modernization process successfully started."}


@app.post("/review-pr", tags=["Workflows"])
async def review_pr() -> Dict[str, str]:
    """
    Endpoint to trigger the PR Review workflow.

    This endpoint will be called by a GitHUb Action when a review
    is requested on a pull request. It will trigger the PR review
    agent team.

    Returns:
        A dictionary confirming that the review has been initiated.
    """
    return {"message": "PR review process successfully started."}
