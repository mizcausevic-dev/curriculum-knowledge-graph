# Curriculum Knowledge Graph Architecture

## Intent

This repo models a curriculum as a graph of:

- courses
- prerequisite edges
- skill dependencies
- program outcomes

The goal is to show which courses unlock the most downstream progression and
which skills become structural bottlenecks for a capstone or final pathway.

## Flow

1. `app/data/sample_curriculum.json` stores the seeded program map.
2. `app/services/graph_service.py` computes course bottlenecks, pathways, and skill ladders.
3. `app/main.py` exposes HTML proof routes and JSON APIs.
4. `app/render.py` generates the graph proof pages for the README.
5. `scripts/render_readme_assets.py` captures PNG screenshots from those pages.

## Routes

- `/`
  - overview of bottlenecks and graph posture
- `/pathway`
  - capstone route explorer
- `/skills`
  - skill dependency board
- `/api-summary`
  - sample payload and route surface
- `/api/dashboard/summary`
  - summary metrics
- `/api/courses`
  - course node details
- `/api/courses/{course_id}`
  - single course detail
- `/api/skills`
  - skill dependency map
- `/api/sample`
  - compact demo payload

## Why It Matters

Student success is not only about student behavior. It is also about whether the
curriculum structure creates unnecessary chokepoints. This repo focuses on the
structural side of academic progression.
