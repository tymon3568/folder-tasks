<!-- Example of how you can add to your user_rules -->
<rule name="task_management_workflow">
    <description>Rules for AI agents when working with the Markdown task system.</description>
    <guideline>When requested to work with a task in the Markdown task system (structure Version/Phase/task-NN.md):</guideline>
    <guideline>1.  **Receive Task:** Only work on tasks that are directly assigned or 'Todo' tasks that match the USER's search request. Always check and respect the 'Assignee' field.</guideline>
    <guideline>2.  **Check Dependencies:** Before starting, verify that all tasks in the 'Dependencies' section of the task file are in 'Done' status. If not, notify the USER and do not proceed unless otherwise instructed.</guideline>
    <guideline>3.  **Update Status:** As soon as starting a task, suggest updating the task file status to 'InProgress_By_[AI_Agent_Name]' and log in 'AI Agent Log'.</guideline>
    <guideline>4.  **Execute Sub-tasks:** Handle sub-tasks sequentially. After each sub-task is completed, suggest marking the checkbox and logging details in 'AI Agent Log'.</guideline>
    <guideline>5.  **Code Management (If applicable):** Always `git pull` before starting code. Suggest `git commit` frequently with clear messages (including TaskID). Suggest `git push` when completing the code portion of the task.</guideline>
    <guideline>6.  **Handle Blockers:** If encountering issues, suggest updating task status to 'Blocked_By_[Reason]', log details and immediately notify the USER.</guideline>
    <guideline>7.  **Complete Task:** When all sub-tasks and completion criteria are met, suggest updating task status to 'NeedsReview' (or 'Done' if appropriate) and notify the USER.</guideline>
    <guideline>8.  **Update Task File:** All changes to task file (status, checkbox, log) must be done by suggesting content updates for USER to apply (e.g., via `propose_code` tool).</guideline>
    <guideline>9.  **Communication:** Frequently notify the USER about progress, encountered issues, and when task is completed or needs review.</guideline>
    <guideline>10. **Follow Task File:** Always get detailed information, completion criteria, and execution steps from the specified task file. Do not arbitrarily change task scope unless USER agrees and updates the task file.</guideline>
</rule>