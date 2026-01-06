#!/usr/bin/env python3
"""folder-tasks minimal orchestrator (router + prompt generator).

This script is intentionally minimal:
- Scans for task_*.md files
- Parses a small header subset (Status, Assignee, Dependencies)
- Picks the next actionable task
- Chooses a role prompt template
- Emits a runnable prompt file for a Ralph-style loop runner

It does NOT run any LLM by itself.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import os
import re
from pathlib import Path
from typing import Iterable

ROOT_DEFAULT = Path(__file__).resolve().parents[1]

STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$")
ASSIGNEE_RE = re.compile(r"^\*\*Assignee(?:\s*\(If any\))?:\*\*\s*(.*)\s*$")
SUGGESTED_ROLE_RE = re.compile(r"^\*\*Suggested Role:\*\*\s*(.*)\s*$")
GATES_RE = re.compile(r"^\*\*Gates:\*\*\s*(.*)\s*$")
DEPS_START_RE = re.compile(r"^##\s+Dependencies", re.IGNORECASE)
TASK_ID_RE = re.compile(r"^\*\*Task ID:\*\*\s*`([^`]+)`\s*$")

ALLOWED_STATUSES = {
    "Todo",
    "NeedsReview",
    "Done",
}


def is_allowed_dynamic_status(status: str) -> bool:
    return status.startswith("InProgress_By_") or status.startswith("Blocked_By_")


@dataclasses.dataclass(frozen=True)
class Task:
    path: Path
    task_id: str | None
    status: str | None
    assignee: str | None
    suggested_role: str | None
    gates: list[str]
    dependencies: list[str]


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def parse_task(path: Path) -> Task:
    lines = read_lines(path)

    task_id: str | None = None
    status: str | None = None
    assignee: str | None = None
    suggested_role: str | None = None
    gates: list[str] = []
    dependencies: list[str] = []

    in_deps = False
    for raw in lines:
        line = raw.rstrip("\n")

        if not in_deps:
            m = TASK_ID_RE.match(line)
            if m:
                task_id = m.group(1).strip()
                continue

            m = STATUS_RE.match(line)
            if m:
                status = m.group(1).strip()
                continue

            m = ASSIGNEE_RE.match(line)
            if m:
                assignee = m.group(1).strip() or None
                continue

            m = SUGGESTED_ROLE_RE.match(line)
            if m:
                suggested_role = m.group(1).strip() or None
                continue

            m = GATES_RE.match(line)
            if m:
                raw_gates = (m.group(1) or "").strip()
                if raw_gates:
                    gates = [g.strip() for g in re.split(r"[,;]", raw_gates) if g.strip()]
                continue

            if DEPS_START_RE.match(line):
                in_deps = True
                continue
        else:
            # Stop deps block on next heading
            if line.startswith("## ") and not DEPS_START_RE.match(line):
                in_deps = False
                continue

            dep = line.strip()
            if dep.startswith("-"):
                dep = dep.lstrip("-").strip()
            dep = dep.strip("` ")
            if dep and "task_" in dep:
                dependencies.append(dep)

    return Task(
        path=path,
        task_id=task_id,
        status=status,
        assignee=assignee,
        suggested_role=suggested_role,
        gates=gates,
        dependencies=dependencies,
    )


def find_tasks(root: Path) -> list[Task]:
    tasks: list[Task] = []
    for path in root.rglob("task_*.md"):
        # Ignore this repo's own template file
        if path.name == "task_XX.YY.ZZ_taskName.md":
            continue
        tasks.append(parse_task(path))
    return sorted(tasks, key=lambda t: str(t.path))


def status_ok(status: str | None) -> bool:
    if not status:
        return False
    if status in ALLOWED_STATUSES:
        return True
    return is_allowed_dynamic_status(status)


def build_task_index(tasks: Iterable[Task], root: Path) -> dict[str, Task]:
    index: dict[str, Task] = {}
    for task in tasks:
        if task.task_id:
            index[task.task_id] = task
        # Also allow lookup by relative path string (common in Dependencies)
        rel = str(task.path.relative_to(root))
        index[rel] = task
    return index


def deps_done(task: Task, index: dict[str, Task]) -> bool:
    for dep in task.dependencies:
        dep_task = index.get(dep)
        if not dep_task:
            return False
        if (dep_task.status or "").strip() != "Done":
            return False
    return True


def is_actionable(task: Task, agent_name: str, index: dict[str, Task]) -> bool:
    if not status_ok(task.status):
        return False
    if task.assignee and task.assignee != agent_name:
        return False
    # Actionable statuses:
    # - NeedsReview: reviewer flow
    # - Blocked: PM/Architect flow
    # - Todo (deps done): developer flow
    if task.status == "NeedsReview":
        return True
    if (task.status or "").startswith("Blocked_By_"):
        return True
    if task.status == "Todo":
        return deps_done(task, index)
    return False


def choose_role(task: Task) -> str:
    # Status-based routing first
    if task.status == "NeedsReview":
        return "reviewer"
    if (task.status or "").startswith("Blocked_By_"):
        reason = (task.status or "").removeprefix("Blocked_By_").lower()
        if "unclear" in reason or "require" in reason or "spec" in reason:
            return "pm"
        return "architect"

    # Suggested Role override (if present)
    if task.suggested_role:
        normalized = task.suggested_role.strip().lower().replace("-", "_").replace(" ", "_")
        mapping = {
            "frontend_dev": "frontend_dev_sveltekit",
            "frontend_dev_sveltekit": "frontend_dev_sveltekit",
            "backend_dev": "backend_dev",
            "devops": "devops",
            "qa": "qa",
            "reviewer": "reviewer",
            "pm": "pm",
            "architect": "architect",
            "chief_architect": "architect",
        }
        if normalized in mapping:
            return mapping[normalized]

    # Heuristic routing by task id / path
    phase_hint = task.task_id or task.path.as_posix()
    hay = phase_hint.lower()
    if "frontend" in hay or "svelte" in hay or "ui" in hay:
        return "frontend_dev_sveltekit"
    if "backend" in hay or "auth" in hay or "api" in hay:
        return "backend_dev"
    if "deploy" in hay or "docker" in hay or "ci" in hay or "production" in hay:
        return "devops"
    return "architect"


def task_rank(task: Task) -> tuple[int, str]:
    # Lower is higher priority.
    status = (task.status or "").strip()
    if status == "NeedsReview":
        return (0, str(task.path))
    if status.startswith("Blocked_By_"):
        return (1, str(task.path))
    if status == "Todo":
        return (2, str(task.path))
    return (9, str(task.path))


def render_prompt(agent_name: str, task_path: Path, role_prompt: str, completion_promise: str) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    return "\n".join(
        [
            f"You are {agent_name}.",
            f"Current time: {now}.",
            "", 
            "Follow the repository rules in AI_WORKFLOW_INTEGRATION.md.",
            "Before any code work, claim the task by updating its Status/Assignee/Last Updated and adding an AI Agent Log entry.",
            "", 
            f"Task file to work on: {task_path.as_posix()}",
            "", 
            "Role prompt to follow:",
            role_prompt.strip(),
            "", 
            "Completion promise:",
            f"- Output exactly: {completion_promise}",
            "", 
            "Escape hatch:",
            "- If stuck, set Status to Blocked_By_[Reason] and log what you tried and what is needed.",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT_DEFAULT), help="Repo root (default: scripts/..)")
    parser.add_argument("--agent", required=True, help="Agent name, e.g. Frontend_Dev_Alpha")
    parser.add_argument("--out", default=".ft/prompt.md", help="Prompt output path (relative to root)")
    parser.add_argument("--completion-promise", default="<promise>DONE</promise>")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    tasks = find_tasks(root)
    index = build_task_index(tasks, root)

    actionable = [t for t in tasks if is_actionable(t, args.agent, index)]
    if not actionable:
        # Project-level readiness is defined by tasks marked with Gates: ProductionReady
        gating = [t for t in tasks if any(g.lower() == "productionready" for g in t.gates)]
        if gating and all((t.status or "").strip() == "Done" for t in gating):
            print("All gating tasks are Done.")
            print("<promise>PROJECT_PRODUCTION_READY</promise>")
            return 0

        print("No actionable tasks found (NeedsReview/Blocked/Todo+depsDone + assignee match).")
        return 2

    task = sorted(actionable, key=task_rank)[0]
    role = choose_role(task)

    role_prompt_path = root / "prompts" / f"{role}.md"
    if not role_prompt_path.exists():
        print(f"Missing role prompt: {role_prompt_path}")
        return 3

    role_prompt = role_prompt_path.read_text(encoding="utf-8")

    prompt = render_prompt(
        agent_name=args.agent,
        task_path=task.path,
        role_prompt=role_prompt,
        completion_promise=args.completion_promise,
    )

    out_path = (root / args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(prompt, encoding="utf-8")

    rel_out = out_path.relative_to(root)
    print(f"Selected task: {task.path.relative_to(root)}")
    print(f"Selected role: {role}")
    print(f"Wrote prompt: {rel_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
