from __future__ import annotations

import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from app.render import (
    render_api_summary,
    render_overview,
    render_pathway,
    render_skill_dependencies,
)
from app.services.graph_service import build_service

app = FastAPI(
    title="Curriculum Knowledge Graph",
    version="0.1.0",
    description=(
        "Curriculum graph for courses, prerequisites, skills, outcomes, and pathway bottleneck analysis in higher education."
    ),
)

service = build_service()


@app.get("/", response_class=HTMLResponse)
def overview() -> str:
    return render_overview()


@app.get("/pathway", response_class=HTMLResponse)
def pathway_page() -> str:
    return render_pathway()


@app.get("/skills", response_class=HTMLResponse)
def skills_page() -> str:
    return render_skill_dependencies()


@app.get("/api-summary", response_class=HTMLResponse)
def api_summary_page() -> str:
    return render_api_summary()


@app.get("/api/dashboard/summary")
def dashboard_summary() -> dict:
    return service.summary()


@app.get("/api/courses")
def courses() -> list[dict]:
    return service.course_nodes()


@app.get("/api/courses/{course_id}")
def course(course_id: str) -> dict:
    value = service.course(course_id)
    if value is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return value


@app.get("/api/skills")
def skills() -> list[dict]:
    return service.skill_map()


@app.get("/api/sample")
def sample() -> dict:
    return service.sample_payload()


@app.get("/openapi.json")
def openapi_spec() -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(app.openapi())))


if __name__ == "__main__":
    import os

    import uvicorn

    port = int(os.environ.get("PORT", "4706"))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
