from __future__ import annotations

import json
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class CurriculumGraphService:
    source_path: Path

    def load(self) -> dict[str, Any]:
        return json.loads(self.source_path.read_text(encoding="utf-8"))

    def _graph(self) -> tuple[dict[str, Any], dict[str, list[str]], dict[str, list[str]]]:
        data = self.load()
        courses = {course["course_id"]: course for course in data["graph"]["courses"]}
        forward: dict[str, list[str]] = defaultdict(list)
        reverse: dict[str, list[str]] = defaultdict(list)
        for edge in data["graph"]["prerequisites"]:
            forward[edge["source"]].append(edge["target"])
            reverse[edge["target"]].append(edge["source"])
        return courses, forward, reverse

    def pathway(self, start: str, goal: str) -> list[str]:
        courses, forward, _reverse = self._graph()
        queue: deque[tuple[str, list[str]]] = deque([(start, [start])])
        seen = {start}
        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path
            for neighbor in forward.get(current, []):
                if neighbor not in seen and neighbor in courses:
                    seen.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []

    def course_nodes(self) -> list[dict[str, Any]]:
        courses, forward, reverse = self._graph()
        nodes = []
        for course_id, course in courses.items():
            out_degree = len(forward.get(course_id, []))
            in_degree = len(reverse.get(course_id, []))
            bottleneck_score = in_degree * 18 + out_degree * 12 + len(course["skills"]) * 6
            nodes.append(
                {
                    "courseId": course_id,
                    "title": course["title"],
                    "term": course["term"],
                    "credits": course["credits"],
                    "skills": course["skills"],
                    "outcomes": course["outcomes"],
                    "prerequisiteCount": in_degree,
                    "unlocksCount": out_degree,
                    "bottleneckScore": bottleneck_score,
                }
            )
        return sorted(nodes, key=lambda item: (-item["bottleneckScore"], item["courseId"]))

    def skill_map(self) -> list[dict[str, Any]]:
        data = self.load()
        courses, _forward, _reverse = self._graph()
        skills_to_courses: dict[str, list[str]] = defaultdict(list)
        for course_id, course in courses.items():
            for skill in course["skills"]:
                skills_to_courses[skill].append(course_id)

        return [
            {
                "skill": skill_dep["skill"],
                "dependsOn": skill_dep["depends_on"],
                "taughtIn": skills_to_courses.get(skill_dep["skill"], []),
            }
            for skill_dep in data["graph"]["skill_dependencies"]
        ]

    def summary(self) -> dict[str, Any]:
        data = self.load()
        courses = self.course_nodes()
        highest_bottleneck = courses[0]
        capstone_path = self.pathway("IS-101", "IS-410")
        return {
            "institution": data["institution"],
            "program": data["program"],
            "courseCount": len(courses),
            "skillDependencyCount": len(self.skill_map()),
            "highestBottleneckCourse": highest_bottleneck["courseId"],
            "capstonePathLength": len(capstone_path),
            "leadRecommendation": (
                "Protect Data Systems and Workflow Automation because both are structural bottlenecks feeding the capstone pathway."
            ),
        }

    def bottlenecks(self) -> list[dict[str, Any]]:
        nodes = self.course_nodes()
        return nodes[:4]

    def sample_payload(self) -> dict[str, Any]:
        return {
            "dashboard": self.summary(),
            "bottlenecks": [
                {
                    "courseId": course["courseId"],
                    "title": course["title"],
                    "bottleneckScore": course["bottleneckScore"],
                    "unlocksCount": course["unlocksCount"],
                }
                for course in self.bottlenecks()
            ],
            "capstonePath": self.pathway("IS-101", "IS-410"),
        }

    def course(self, course_id: str) -> dict[str, Any] | None:
        for course in self.course_nodes():
            if course["courseId"] == course_id:
                return course
        return None


def build_service(root: Path | None = None) -> CurriculumGraphService:
    base = root or Path(__file__).resolve().parents[2]
    return CurriculumGraphService(base / "app" / "data" / "sample_curriculum.json")
