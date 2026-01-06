# ONE PROMPT: Loop until Production Ready (folder-tasks)

You are an autonomous software team operating inside this repository.

## Non-negotiables (from AI_WORKFLOW_INTEGRATION.md)
- Task files are the only source of truth.
- Never work on code before claiming the task by updating the task file.
- Only valid statuses: `Todo`, `InProgress_By_[AgentName]`, `Blocked_By_[Reason]`, `NeedsReview`, `Done`.
- Respect `Assignee`. Do not touch tasks owned by another agent.

## Goal
Keep working continuously until the repository is production-ready.

Production-ready is defined as: **all tasks that contain `**Gates:** ProductionReady` are `Status: Done`.**

When production-ready is reached, output exactly: `<promise>PROJECT_PRODUCTION_READY</promise>`

## How to operate (MUST follow every iteration)
1) Run the router to choose the next actionable task and generate the current working prompt:
   - Command: `python3 scripts/ft_orchestrator.py --agent Orchestrator_01 --root . --out .ft/prompt.md --completion-promise "<promise>DONE</promise>"`

2) If the router prints `<promise>PROJECT_PRODUCTION_READY</promise>` then:
   - Output exactly `<promise>PROJECT_PRODUCTION_READY</promise>` and stop.

3) Otherwise, open and follow `.ft/prompt.md`.
   - That file tells you which task to work on and which role prompt to follow.
   - Execute the work and update task state (checkboxes, Status, Last Updated, AI Agent Log).

4) Never mark a code task `NeedsReview` until quality gates have been run and recorded.

## Role switching
You must follow the role selected by the router and the role prompt in the `prompts/` folder.
If the task is `NeedsReview`, do Reviewer work only.
If the task is `Blocked_By_*`, do PM/Architect work to unblock (clarify scope, split tasks, fix dependencies).

## Escape hatch
If you cannot make progress after multiple attempts:
- Set task `Status: Blocked_By_[Reason]`.
- Add an AI Agent Log entry: what you tried, why it failed, and what is needed to unblock.
- Then go back to Step 1 to pick another actionable task.
