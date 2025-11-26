# AI Agent & Folder Tasks Integration Guide

This document defines how the **AI Agent System** (defined in `AI_agents.md`) operates within the **Folder Tasks Workflow** (defined in `README.md`).

## 1. The Core Concept

*   **The "Who"**: `AI_agents.md` defines the workforce (PM, Architect, Developers, QA).
*   **The "What"**: `folder-tasks` defines the work units (Task Files, Directory Structure).
*   **The "How"**: Agents communicate and coordinate *exclusively* through the state of these task files.

## 2. Role-to-Task Mapping

| Agent Role | Folder-Tasks Responsibility | Key Actions |
| :--- | :--- | :--- |
| **Product Manager (PM)** | **Task Creator** (Phase 0/1) | Creates `TASKS_OVERVIEW.md`, defines Phases, writes high-level specs in `docs/`. |
| **Chief Architect** | **Structure Owner** | Creates directory structure (`V1/Phase_01/...`), creates `task_XX.md` files, defines Dependencies. |
| **Developer (Front/Back)** | **Task Executor** | Reads assigned `task_XX.md`, changes status to `InProgress`, writes code, marks checkboxes `[x]`. |
| **Reviewer** | **Task Reviewer** | Monitors `NeedsReview` status, comments in "Notes" section, changes status to `Done` or `InProgress` (if changes needed). |
| **QA Agent** | **Verifier** | Picks up `Done` tasks for integration testing, logs results in "AI Agent Log". |

## 3. The Integrated Workflow

### Step 1: Planning (PM & Architect)
1.  **PM** updates `TASKS_OVERVIEW.md` with a new Phase.
2.  **Architect** creates the folder `V1_MVP/02_New_Feature`.
3.  **Architect** generates `task_02.01_feature_setup.md` and `task_02.02_feature_impl.md`.
    *   *Crucial*: Architect sets `Assignee: Frontend_Dev_Alpha` or leaves it open.
    *   *Crucial*: Architect sets `Dependencies` in `task_02.02` pointing to `task_02.01`.

### Step 2: Execution (Developers)
1.  **Developer** scans for tasks where `Status: Todo` AND `Dependencies: [All Done]`.
2.  **Developer** claims task:
    *   Updates `Status: InProgress_By_DevName`.
    *   Updates `Assignee: DevName`.
3.  **Developer** works:
    *   Reads `Detailed Description`.
    *   Executes sub-tasks.
    *   Updates checkboxes `[x]` as they go.
    *   *Self-Correction*: If a sub-task is impossible, updates `Notes` and notifies Architect.

### Step 3: Review (Reviewer)
1.  **Developer** finishes all sub-tasks and sets `Status: NeedsReview`.
2.  **Reviewer** detects `NeedsReview` task.
3.  **Reviewer** checks code (PR) and Task Completion Criteria.
4.  **Reviewer** updates file:
    *   *Pass*: Sets `Status: Done`.
    *   *Fail*: Sets `Status: InProgress` and adds feedback in `Notes`.

## 4. Agent "Context Protocol"

When an agent "wakes up", it should run this routine:

1.  **Identify Self**: "I am a Backend Developer Agent."
2.  **Locate Context**: Read `TASKS_OVERVIEW.md` to see the big picture.
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
2.  **Update Task**: Set `Status: Blocked_By_[Reason]`.
3.  **Log**: Add entry to "AI Agent Log" at bottom of file.
4.  **Notify**: Use `notify_user` or tag the PM Agent in the `Notes` section.
