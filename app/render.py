from __future__ import annotations

import html
import json
from pathlib import Path

from app.services.graph_service import build_service


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def page_shell(title: str, kicker: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_escape(title)}</title>
  <style>
    :root {{
      --bg: #07111d;
      --panel: #0d1a2b;
      --line: #1d3655;
      --text: #eef2ff;
      --muted: #98a7c2;
      --accent: #68b7ff;
      --warning: #ffc86b;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", Inter, sans-serif;
      background: linear-gradient(180deg, #07111d 0%, #091827 100%);
      color: var(--text);
    }}
    .page {{
      width: 1440px;
      margin: 0 auto;
      padding: 48px 52px 64px;
      background:
        radial-gradient(circle at top right, rgba(104,183,255,0.16), transparent 30%),
        linear-gradient(180deg, rgba(11,25,41,0.95), rgba(6,14,24,0.98));
      min-height: 920px;
    }}
    .frame {{
      border: 1px solid var(--line);
      border-radius: 34px;
      padding: 28px 32px 36px;
      background: rgba(11, 22, 37, 0.88);
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 15px;
      letter-spacing: 0.34em;
      text-transform: uppercase;
      margin-bottom: 18px;
      font-weight: 700;
    }}
    h1 {{
      margin: 0;
      font-size: 66px;
      line-height: 0.98;
      color: #f4f1e3;
      font-family: Georgia, "Times New Roman", serif;
      max-width: 1120px;
    }}
    .lede {{
      margin-top: 18px;
      max-width: 920px;
      color: var(--muted);
      font-size: 18px;
      line-height: 1.6;
    }}
    .pill-row {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 24px;
    }}
    .pill {{
      border-radius: 999px;
      padding: 10px 16px;
      background: #1a2f4d;
      border: 1px solid #29486e;
      color: #f5f8ff;
      font-size: 15px;
      font-weight: 600;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin-top: 28px;
    }}
    .stat {{
      padding: 22px 22px 18px;
      border-radius: 24px;
      background: #12233a;
      border: 1px solid #25415f;
      min-height: 168px;
    }}
    .label {{
      color: #a8b6cd;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 13px;
      margin-bottom: 14px;
    }}
    .value {{
      color: #f4f1e3;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 48px;
      line-height: 0.95;
      margin-bottom: 12px;
    }}
    .copy {{
      color: #c1cadc;
      font-size: 16px;
      line-height: 1.5;
    }}
    .section {{
      margin-top: 34px;
      border-radius: 28px;
      border: 1px solid #203654;
      background: #0d1524;
      padding: 28px;
    }}
    .section-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }}
    .card {{
      border-radius: 22px;
      border: 1px solid #263d5f;
      background: #131e32;
      padding: 22px;
      min-height: 250px;
    }}
    .card .kicker {{
      color: var(--accent);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.18em;
      margin-bottom: 18px;
      font-weight: 700;
    }}
    .card h2 {{
      font-size: 24px;
      line-height: 1.15;
      margin: 0 0 14px;
      color: #f4f1e3;
      font-family: Georgia, "Times New Roman", serif;
    }}
    .card p, .card li, .queue td, .queue th {{
      color: #bdc7d9;
      font-size: 16px;
      line-height: 1.55;
      margin: 0;
    }}
    .card ul {{
      padding-left: 18px;
      margin: 0;
    }}
    .queue {{
      width: 100%;
      border-collapse: collapse;
    }}
    .queue th, .queue td {{
      text-align: left;
      padding: 14px 12px;
      border-bottom: 1px solid #203654;
      vertical-align: top;
    }}
    .queue th {{
      color: #8fbfff;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 12px;
    }}
    .json {{
      background: #07101b;
      border: 1px solid #284462;
      border-radius: 22px;
      padding: 24px;
      margin-top: 24px;
    }}
    pre {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      color: #d7f7da;
      font-size: 15px;
      line-height: 1.45;
      font-family: Consolas, "SFMono-Regular", monospace;
    }}
  </style>
</head>
<body>
  <div class="page">
    <div class="frame">
      <div class="eyebrow">{_escape(kicker)}</div>
      {body}
    </div>
  </div>
</body>
</html>
"""


def render_overview() -> str:
    service = build_service()
    summary = service.summary()
    bottlenecks = service.bottlenecks()
    body = f"""
      <h1>Map the curriculum so prerequisites, skill gaps, and capstone bottlenecks stop hiding in the catalog.</h1>
      <p class="lede">
        Curriculum Knowledge Graph models courses, prerequisite edges, skill dependencies,
        and program outcomes so faculty and academic leaders can see which nodes unlock the most downstream progression.
      </p>
      <div class="pill-row">
        <div class="pill">course prerequisite graph</div>
        <div class="pill">skill dependency mapping</div>
        <div class="pill">pathway bottleneck analysis</div>
        <div class="pill">program outcome proof</div>
      </div>
      <div class="stats">
        <div class="stat"><div class="label">Courses mapped</div><div class="value">{summary['courseCount']}</div><div class="copy">Courses modeled as graph nodes with skills, outcomes, and prerequisite edges.</div></div>
        <div class="stat"><div class="label">Skill dependencies</div><div class="value">{summary['skillDependencyCount']}</div><div class="copy">Explicit skill ladders that show what later competencies depend on.</div></div>
        <div class="stat"><div class="label">Capstone path</div><div class="value">{summary['capstonePathLength']}</div><div class="copy">Shortest prerequisite path from entry course to capstone completion.</div></div>
        <div class="stat"><div class="label">Top bottleneck</div><div class="value">{_escape(summary['highestBottleneckCourse'])}</div><div class="copy">{_escape(summary['leadRecommendation'])}</div></div>
      </div>
      <div class="section">
        <div class="section-grid">
          {''.join(
              f'''<div class="card"><div class="kicker">{_escape(course["term"])}</div><h2>{_escape(course["courseId"])} · {_escape(course["title"])}</h2><p>Bottleneck score: {course["bottleneckScore"]} • Unlocks: {course["unlocksCount"]} • Prereqs: {course["prerequisiteCount"]}</p><p>Skills: {_escape(", ".join(course["skills"]))}</p></div>'''
              for course in bottlenecks
          )}
        </div>
      </div>
    """
    return page_shell("Curriculum Knowledge Graph - Overview", "curriculum knowledge graph", body)


def render_pathway() -> str:
    service = build_service()
    path = service.pathway("IS-101", "IS-410")
    courses = {course["courseId"]: course for course in service.course_nodes()}
    rows = "".join(
        f"""
        <tr>
          <td>{_escape(course_id)}</td>
          <td>{_escape(courses[course_id]['title'])}</td>
          <td>{_escape(courses[course_id]['term'])}</td>
          <td>{_escape(", ".join(courses[course_id]['skills']))}</td>
        </tr>
        """
        for course_id in path
    )
    body = f"""
      <h1>The graph makes the capstone path obvious enough to redesign, protect, or accelerate.</h1>
      <p class="lede">
        Instead of reading prerequisites course by course, this pathway view shows how the student journey stacks into the capstone and where one failing node slows the whole program.
      </p>
      <div class="section">
        <table class="queue">
          <thead>
            <tr>
              <th>Course</th>
              <th>Title</th>
              <th>Term</th>
              <th>Skills reinforced</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    """
    return page_shell("Curriculum Knowledge Graph - Pathway", "capstone pathway", body)


def render_skill_dependencies() -> str:
    skills = build_service().skill_map()
    body = f"""
      <h1>Skill ladders explain why one course matters far beyond its own syllabus.</h1>
      <p class="lede">
        Skill dependencies show how a local course decision can affect later assessment performance, capstone outcomes, and overall program coherence.
      </p>
      <div class="section">
        <div class="section-grid">
          {''.join(
              f'''<div class="card"><div class="kicker">{_escape(skill["skill"])}</div><h2>Depends on {_escape(", ".join(skill["dependsOn"]))}</h2><p>Taught in: {_escape(", ".join(skill["taughtIn"]))}</p></div>'''
              for skill in skills
          )}
        </div>
      </div>
    """
    return page_shell("Curriculum Knowledge Graph - Skill Dependencies", "skill dependency board", body)


def render_api_summary() -> str:
    payload = build_service().sample_payload()
    body = f"""
      <h1>A small API surface that can feed catalog tools, pathway explorers, and advising systems.</h1>
      <p class="lede">
        The graph service exposes courses, bottlenecks, and pathway outputs in a machine-readable form that other EdTech systems can build on.
      </p>
      <div class="section-grid">
        <div class="card"><div class="kicker">routes</div><h2>Summary, bottlenecks, and course detail APIs.</h2><p><code>/api/dashboard/summary</code>, <code>/api/courses</code>, <code>/api/courses/{'{course_id}'}</code>, and <code>/api/sample</code>.</p></div>
        <div class="card"><div class="kicker">fit</div><h2>Built for curriculum leadership and pathway analysis.</h2><p>It works well for program review, curriculum redesign, and advising enablement.</p></div>
        <div class="card"><div class="kicker">payload</div><h2>Sample graph payload from the local service.</h2><p>Small enough to inspect quickly, rich enough to prove the knowledge-graph story.</p></div>
      </div>
      <div class="json"><pre>{_escape(json.dumps(payload, indent=2))}</pre></div>
    """
    return page_shell("Curriculum Knowledge Graph - API Summary", "api summary", body)


def write_static_proof_pages(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-capstone-pathway.html": render_pathway(),
        "03-skill-dependencies.html": render_skill_dependencies(),
        "04-api-summary.html": render_api_summary(),
    }
    written: list[Path] = []
    for name, contents in pages.items():
        target = output_dir / name
        target.write_text(contents, encoding="utf-8")
        written.append(target)
    return written
