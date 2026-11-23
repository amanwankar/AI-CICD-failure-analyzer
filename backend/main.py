
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="AI CI/CD Failure Analyzer",
    version="0.1.0"
)


class LogPayload(BaseModel):
    workflow_name: str = Field(
        min_length=1,
        max_length=100
    )
    logs: str = Field(
        min_length=1,
        max_length=20000
    )


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "service": "ai-cicd-failure-analyzer",
        "ai_connected": False
    }


@app.post("/api/analyze")
def analyze(payload: LogPayload):
    keywords = (
        "error",
        "failed",
        "fatal",
        "no such file",
        "exception",
        "cannot find"
    )

    error_lines = [
        line.strip()
        for line in payload.logs.splitlines()
        if any(
            keyword in line.lower()
            for keyword in keywords
        )
    ]

    return {
        "workflow_name": payload.workflow_name,
        "status": "received",
        "analysis_type": "keyword_only",
        "error_lines": error_lines[:10],
        "message": "AI analysis not connected yet."
    }
