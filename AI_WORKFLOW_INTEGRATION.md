# AI Agent & Folder Tasks Integration Guide

This document defines how the **AI Agent System** (defined in `AI_agents.md`) operates within the **Folder Tasks Workflow** (defined in `README.md`).

**Repo note:** This repo uses `Task_over_view.md` as the overview file (instead of `TASKS_OVERVIEW.md`).

## 0. Non-Negotiables (Multi-Agent Safety)

This repository runs **multiple agents in parallel**. Coordination happens **only** through task files.

### 0.1 Single Source of Truth
- Task files (`PROJECT_TRACKING/**/task_*.md`) are the only source of truth for work state.
- Agents MUST update the task file **before** any code work to avoid race conditions.

## 0.2 Strict Status Adherence (ONLY these 5 statuses are valid)
| Status | Meaning |
|---|---|
| `Todo` | Ready to be claimed |
| `InProgress_By_[AgentName]` | Claimed and actively being worked |
| `Blocked_By_[Reason]` | Cannot proceed; must include reason |
| `NeedsReview` | Work complete; awaiting review |
| `Done` | Reviewed and approved |

❌ Invalid examples (never use): `InProgress`, `InProgress_By` (missing agent name), `Completed`, `Pending`, `Waiting`, `Done_By_AI`, etc.

### 0.3 Quality Gates Before `NeedsReview`
If a task involves code changes, the agent MUST run and pass:
- Typecheck
- Lint
- Tests (unit/integration/E2E as applicable)

(Frontend baseline: prefer `bun run ...` when available.)

### 0.4 Ownership & No-Interference Rule
- If `Assignee` is not you, do not claim unless explicitly reassigned.
- If `Status` is `InProgress_By_Another_Agent`, do not edit the task or code for it.

## 1. The Core Concept

*   **The "Who"**: `AI_agents.md` defines the workforce (PM, Architect, Developers, QA).
*   **The "What"**: `folder-tasks` defines the work units (Task Files, Directory Structure).
*   **The "How"**: Agents communicate and coordinate *exclusively* through the state of these task files.

## 2. Role-to-Task Mapping

| Agent Role | Folder-Tasks Responsibility | Key Actions |
| :--- | :--- | :--- |
| **Product Manager (PM)** | **Task Creator** (Phase 0/1) | Creates `Task_over_view.md`, defines Phases, writes high-level specs in `docs/`. |
| **Chief Architect** | **Structure Owner** | Creates directory structure (`V1/Phase_01/...`), creates `task_XX.md` files, defines Dependencies. |
| **Developer (Front/Back)** | **Task Executor** | Reads assigned `task_XX.md`, changes status to `InProgress_By_[AgentName]`, writes code, marks checkboxes `[x]`. |
| **Reviewer** | **Task Reviewer** | Monitors `NeedsReview` status, comments in "Notes" section, changes status to `Done` or back to `InProgress_By_[AgentName]` (with a clear assignee) if changes are needed. |
| **QA Agent** | **Verifier** | Picks up `Done` tasks for integration testing, logs results in "AI Agent Log". |

## 3. The Integrated Workflow

### Note on repo structure
In this repository, the overview file is named `Task_over_view.md` (not `TASKS_OVERVIEW.md`). All references below should use `Task_over_view.md`.

### Step 1: Planning (PM & Architect)
1.  **PM** updates `Task_over_view.md` with a new Phase.
2.  **Architect** creates the folder `V1_MVP/02_New_Feature`.
3.  **Architect** generates `task_02.01_feature_setup.md` and `task_02.02_feature_impl.md`.
    *   *Crucial*: Architect sets `Assignee: Frontend_Dev_Alpha` or leaves it open.
    *   *Crucial*: Architect sets `Dependencies` in `task_02.02` pointing to `task_02.01`.

### Step 2: Execution (Developers)
1.  **Developer** scans for tasks where `Status: Todo` AND `Dependencies: [All Done]` AND (Assignee is empty OR Assignee is you).
2.  **Developer** claims task (atomic update in the task file first):
    *   Updates `Status: InProgress_By_[AgentName]`.
    *   Updates `Assignee: [AgentName]`.
    *   Updates `Last Updated` to today.
    *   Adds an initial entry to `AI Agent Log` stating dependencies were checked.
3.  **Developer** works:
    *   Reads `Detailed Description`.
    *   Executes sub-tasks in order.
    *   Updates checkboxes `[x]` immediately after each sub-task completes.
    *   Keeps commits small and tied to the task ID.
    *   *Self-Correction*: If a sub-task is impossible, updates `Notes`, sets `Status: Blocked_By_[Reason]`, and notifies the orchestrator/user.

4.  **Mandatory quality gates (code tasks) before `NeedsReview`:**
    *   Run typecheck
    *   Run lint
    *   Run tests (at least unit tests; add E2E for critical flows when applicable)

### Step 3: Review (Reviewer)
1.  **Developer** finishes all sub-tasks and sets `Status: NeedsReview` (only after quality gates pass for code tasks).
2.  **Reviewer** detects `NeedsReview` task.
3.  **Reviewer** checks:
    * Task Completion Criteria
    * Code diff / PR
    * That quality gates were executed (or CI is green once enabled)
4.  **Reviewer** updates file:
    *   *Pass*: Sets `Status: Done`.
    *   *Changes requested*: Sets `Status: InProgress_By_[AgentName]` (explicitly assigns ownership) and adds actionable feedback in `Notes`.

## 4. Agent "Context Protocol"

When an agent "wakes up", it should run this routine:

1.  **Identify Self**: "I am a Backend Developer Agent."
2.  **Locate Context**: Read `Task_over_view.md` to see the big picture.
3.  **Find Work**:
    *   Run `find` or `ls` in active Phase directories.
    *   Grep for `Status: Todo` or `Status: InProgress_By_Me`.
4.  **Update State**: NEVER work without updating the task file first. This prevents race conditions with other agents.

## 5. Example: Architect Creating a Task

The Architect Agent should generate files with this exact header to ensure parsability:

```markdown
# Task: Implement Login API

**Task ID:** `V1_MVP/02_Auth/task_02.01_login.md`
**Status:** Todo
**Assignee:** Backend_Agent_01
**Dependencies:**
- `V1_MVP/01_Database/task_01.01_users_table.md`
```

## 6. Handling Blockers

If an agent is stuck:
1.  **Do NOT** just stop.
2.  **Update Task**: Set `Status: Blocked_By_[Reason]` (be specific, e.g. `Blocked_By_Merge_Conflict_in_src/routes/(app)/...`).
3.  **Log**: Add an entry to `AI Agent Log` including:
    - what you attempted
    - why it failed/blocked (include key error text)
    - what is needed to unblock (decision, access, dependency, clarification)
4.  **Notify**: Notify the orchestrator/user immediately and stop further work on this task.

### 6.1 Merge Conflicts
- If a `git pull` causes conflicts:
  - Attempt simple resolution only if it is clearly safe.
  - If not clearly resolvable, set `Status: Blocked_By_Merge_Conflict_in_[FileName]`, log details, and notify.

### 6.2 Dependency Not Done
- If any dependency is not `Done`:
  - Set `Status: Blocked_By_Dependency_[TaskID]`
  - Log which dependency blocks progress
  - Do not start implementation work

## 7. CI Alignment (GitHub Actions)

This project will use GitHub Actions to enforce quality gates.
Minimum CI expectations for code tasks:
- install deps (prefer `bun install`)
- typecheck
- lint
- test

Agents should assume CI will be strict and must not set tasks to `NeedsReview` unless local checks pass.
