This is documentation about how to create task management following directory structure, Jira-like style to manage project progress and workload for AIs working together.
Task follows directory structure Version/Phase/task-NN.md Directory Structure and Files:
/project_root
├── docs/
│   ├── TASKS_OVERVIEW.md  <-- High-level overview file
│   │
│   ├── V1_MVP/  <-- Version 1: Minimum Viable Product
│   │   ├── 00_Project_Setup_And_Environment/  <-- Phase 0
│   │   │   ├── task_00.01_rust_axum_backend_setup.md
│   │   │   ├── task_00.02_sveltekit_frontend_setup.md
│   │   │   ├── task_00.03_surrealdb_local_setup.md
│   │   │   └── task_00.04_docker_configuration_dev.md
│   │   │
│   │   ├── 01_Database_Schema_And_Seed_Data/  <-- Phase 1
│   │   │   ├── task_01.01_define_core_schemas.md
│   │   │   ├── task_01.02_create_seed_data_files.md
│   │   │   └── task_01.03_implement_seeding_script.md
│   │   │
│   │   ├── 02_Backend_Core_Features/  <-- Phase 2
│   │   │   ├── 02.01_Authentication/
│   │   │   │   ├── task_02.01.01_user_registration_endpoint.md
│   │   │   │   ├── task_02.01.02_user_login_endpoint.md
│   │   │   │   └── task_02.01.03_token_management.md
│   │   │   ├── 02.02_User_Profile_Management/
│   │   │   │   ├── task_02.02.01_create_update_profile_endpoints.md
│   │   │   │   └── task_02.02.02_get_profile_endpoint.md
│   │   │   ├── 02.03_Couple_Profile_Logic/
│   │   │   │   └── ...
│   │   │   └── ...
│   │   │
│   │   ├── 03_Frontend_Core_UI/  <-- Phase 3
│   │   │   ├── 03.01_Authentication_Pages/
│   │   │   │   ├── task_03.01.01_login_page.md
│   │   │   │   └── task_03.01.02_registration_page.md
│   │   │   ├── 03.02_User_Dashboard/
│   │   │   │   └── ...
│   │   │   └── ...
│   │   │
│   │   ├── 04_Initial_Testing/
│   │   │   └── ...
│   │   │
│   │   └── 05_MVP_Deployment_Prep/
│   │       └── ...
│   │
│   ├── V1.1_Post_Launch_Enhancements/  <-- Version 1.1
│   │   ├── 01_Bug_Fixes_From_V1.0/
│   │   │   └── task_01.01_fix_login_issue_xyz.md
│   │   └── 02_New_Feature_ABC/
│   │       ├── task_02.01_backend_for_feature_abc.md
│   │       └── task_02.02_frontend_for_feature_abc.md

│   │

└── src/
    └── ... (mã nguồn dự án)

Below is how you can implement and points to note:

### 1. Task Assignment

#### Assignee Field

In each `task_XX.YY.ZZ_ten_task.md` file, the Assignee field becomes very important.
You (or a "project manager" AI if available) will assign a specific task to a specific AI agent. For example: Assignee: AI_Agent_Alpha or Assignee: AI_Agent_Beta.
An AI agent should only work on tasks that have been assigned to them.
Convention: An AI agent is not allowed to edit a task that has status InProgress_By_Another_Agent.

### 3. Dependency Management

#### Dependencies Field
AI agent must carefully check the Dependencies field in the task file.
A task should only be started when all its dependent tasks have status Done.
This ensures work is performed in the correct order.

### 4. Working with Shared Codebase

#### Version Control (Git)
This is mandatory.
Each AI agent (or you on behalf of the AI) needs to commit changes related to their task.
Before starting a code-related task, the AI agent needs to git pull to get the latest changes from other agents.

#### Handling Merge Conflicts
This is the complex part.
Ideally, tasks are divided small and independent enough to minimize conflicts.
If conflicts occur, your intervention may be needed to resolve them. Or, an AI agent can pause, mark the task as Blocked_By_Merge_Conflict and notify you.

#### Commit Frequency
Encourage small, frequent commits for each completed sub-task portion.

### 5. Communication & Synchronization

#### Through Task Files
Task files are the main communication channel. AI agents update status and log work in AI Agent Log.
TASKS_OVERVIEW.md: This file helps all agents (and you) have an overview of overall progress.

#### Notify You
When an AI agent completes an important task, encounters issues, or needs review, it should notify you.

### 6. Your Role (Orchestrator)

#### Initial Assignment
You will be the one to decide which task is assigned to which agent, or set up rules for agents to pick tasks themselves.

#### Monitor Progress
Based on TASKS_OVERVIEW.md and status of task files.

#### Resolve Conflicts
Intervene when there are issues (merge conflicts, task blocked for too long, misunderstanding requirements).

#### Review Work
Check tasks that have been marked NeedsReview or Done.

#### How an AI Agent Can Operate in This Environment

Check Assigned Tasks: "Cascade, do I have any tasks assigned to me?" or "Cascade, find a Todo task in phase 02_Backend_Core_Features that I can do."
Receive Task: If there is a suitable task that no one is working on (or assigned to them):
Read the task file carefully.
Check Dependencies. If not completed, report back and wait.
Update Status to InProgress_By_MyName.
Execute Task:
Perform each sub-task.
If code-related: git pull, code, test, git commit, git push.
Update sub-task checkboxes.
Complete Task:
Update Status to Done (or NeedsReview).
Log final entry in AI Agent Log.
Notify you.
Repeat: Find new task.

#### Example Assignment

Agent Alpha: Primarily responsible for Phase 02_Backend_Core_Features. It will sequentially work on tasks in that directory.
Agent Beta: Primarily responsible for Phase 03_Frontend_Core_UI.
Agent Gamma (or you): Handle tasks in 00_Project_Setup and 01_Database_Schema, as these are foundational.

#### Challenges

Ensure AI Understands Context Correctly: Each AI agent may have "memory" or separate context. Having task files contain complete information and links to related documentation is very important.
Handle Errors and Unexpected Situations: Need mechanisms for AI to report when they encounter difficulties they cannot resolve themselves.

----------------------------------------------------------------------------------------

Outline of AI Agent Workflow with Markdown Task System

Phase 0: Initial Setup (Perform once or when major changes occur)

Understand Task Structure:
AI agent is provided with information about the directory structure (Version/Phase/task-NN.md) and sample content of a detailed task file.
AI agent knows about the existence and purpose of TASKS_OVERVIEW.md.
Tools: AI agent understands that updating .md files (marking checkboxes, changing status, logging) will be done through proposing content changes (e.g., using the propose_code tool in my "chat mode", you will be the one applying the changes).

Phase 1: Receive and Initialize Task

Find Task to Do:
Priority 1 (Direct Assignment): USER requests AI agent to do a specific task by specifying the task file path (e.g., "Cascade, please do task V1_MVP/02_Backend_Core_Features/.../task_A.md").
Priority 2 (Self-find Task): If no direct assignment, USER can request: "Cascade, find a Todo task in phase [Phase Name] of version [Version Name] that no one is working on or assigned to you."
AI agent will scan task files in the specified directory, check Status and Assignee fields.
Can prioritize by task file number order or Priority field in the file.

Read and Understand Task:
Open and carefully read the entire content of the selected task file: Detailed Description, Completion Criteria, Specific Sub-tasks, Related Documentation, Dependencies.

Check Dependencies:
Review the Dependencies section. For each dependency:
Check the corresponding task file to see if Status is Done.
If any dependency is not Done, AI agent reports back to USER, updates current task Status to Blocked_By_Dependency_[Dependent_Task_ID] and may find another task.

"Receive" Task and Update Status:
If all dependencies are Done (or none exist):
AI agent suggests updating the current task file:
Change Status: to InProgress_By_[AI_Agent_Name] (e.g., InProgress_By_Cascade).
Update Last Updated: to current date.
Add a line to AI Agent Log: noting the start of task (e.g., "[YYYY-MM-DD HH:MM]: Started processing task. Checked dependencies.").

Prepare Environment (If task involves code):
Perform git pull on main branch (e.g., main or develop) to ensure latest code.
If task requires creating a new branch, AI agent will suggest branch creation command.

Phase 2: Execute Task

Process Sub-tasks Sequentially:
AI agent goes through each item in Specific Sub-tasks.
For each sub-task:
Understand sub-task requirements.
Perform necessary actions:
If writing code: Draft code, following project rules and coding conventions.
If updating documentation: Draft update content.
If running commands: Suggest required commands.
Use appropriate tools (e.g., propose_code to suggest code or file content changes, view_file to view files, grep_search to search).

Update Sub-task Progress:
After completing a sub-task, AI agent suggests updating the task file:
Mark the sub-task checkbox as completed: [x].
Add detailed log to AI Agent Log: about the completed sub-task (e.g., "[YYYY-MM-DD HH:MM]: Completed sub-task 2.1: Defined Request struct. Proposed code.").

Commit Code Frequently (If task involves code):
After completing one or a few meaningful sub-tasks, AI agent suggests git add, git commit -m "TaskID: Commit description" (e.g., git commit -m "task_02.01.01: Implement request validation for user registration").

Handle Emerging Issues (Blockers):
If encountering issues that cannot be resolved independently (e.g., missing information, unresolvable code conflicts, external API not working):
AI agent suggests updating task file:
Change Status: to Blocked_By_[Brief_Description_Of_Block_Reason].
Log the issue clearly in AI Agent Log.
Notify USER about the blocked status and reason.
AI agent may pause that task and wait for USER to resolve, or ask USER if they should switch to another task.

Phase 3: Complete and Suggest Task Review

Check Entire Task:
After all sub-tasks are marked [x]:
AI agent reviews the entire Completion Criteria to ensure all have been met.

Update Completion Status:
AI agent suggests updating task file:
Change Status: to NeedsReview (if USER review needed) or Done (if task doesn't need review or AI is allowed to self-mark Done).
Update Last Updated.
Add final log to AI Agent Log: (e.g., "[YYYY-MM-DD HH:MM]: All sub-tasks completed. Task status changed to NeedsReview.").

Finalize Code (If task involves code):
Ensure all code changes are committed.
Suggest git push for the working branch.
If process requires Pull Request (PR), AI agent can suggest creating PR (with clear title and description based on task information).

Notify USER:
AI agent notifies USER that task is completed and ready for review (or Done), including path to task file and PR (if any).

Phase 4: After Review (If applicable)

Receive Feedback:
USER reviews task (and code if any) and provides feedback (can be written directly in Notes/Discussion section of task file or via chat).

Handle Feedback:
If changes are requested:
AI agent suggests updating task Status back to InProgress_By_[AI_Agent_Name].
Implement changes according to feedback (can be treated as new sub-tasks or redoing old sub-tasks).
Repeat steps in Phase 2 and 3 until USER approves.

Close Task:
When USER approves, ensure Status in task file is Done.
If there is a PR, USER or AI agent (if permitted) will merge the PR.