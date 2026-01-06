# Ralph-loop + Role Router Integration for folder-tasks

**Mục tiêu:** áp dụng ý tưởng của plugin `ralph-wiggum` (lặp liên tục tới khi đạt “completion promise”) vào workflow `folder-tasks`, đồng thời cho phép **một agent tự động đổi vai trò** (PM/Architect/Dev/Reviewer/QA/DevOps) dựa trên **trạng thái task files**.

Tài liệu này không phụ thuộc Claude Code; bạn có thể dùng với bất kỳ runner nào (Claude Code, Cursor, VS Code + agent, API runner tự viết). Nếu bạn dùng Claude Code, có thể map trực tiếp với `/ralph-loop`.

---

## 1) Ý tưởng cốt lõi: 2 vòng lặp

### 1.1 Inner loop (Ralph-style) = hoàn thành *một task*
- Input: **một task file** `task_*.md` + prompt template theo role.
- Cơ chế: lặp nhiều lần (có `--max-iterations`/giới hạn) cho đến khi:
  - Task đạt tiêu chí hoàn thành và chuyển `Status: NeedsReview`, **hoặc**
  - Task bị chặn và chuyển `Status: Blocked_By_[Reason]`.

### 1.2 Outer loop (Project loop) = hoàn thành *toàn dự án*
- Input: `Task_over_view.md` + toàn bộ task files.
- Mỗi iteration:
  1. Chọn **next actionable task** (Todo + deps Done + đúng assignee).
  2. Chọn **role** phù hợp theo “Role Router”.
  3. Chạy Inner loop cho task đó.
- Dừng khi mọi task quan trọng cho release đều `Done` và checklist production-ready đạt.

---

## 2) Role Router (tự đổi vai trò) — luật quyết định

### 2.1 Rule ưu tiên theo Status
1. `NeedsReview` → **Reviewer**
2. `Blocked_By_[Reason]` → **PM/Architect** (tùy blocker) để làm rõ yêu cầu/thiết kế hoặc tách task
3. `Todo` (deps Done) → **Developer** (FE/BE/DevOps tùy Phase/Module)
4. `Done` → **QA** (nếu có task QA/verification riêng hoặc cần chứng nhận)

### 2.2 Rule chọn “Developer subtype” theo Phase/Module
Gợi ý routing đơn giản (không thêm field mới vẫn chạy được):
- `Phase` chứa `Frontend` hoặc Module chứa `UI`/`SvelteKit` → Frontend Dev
- `Phase` chứa `Backend`/`API`/`Auth` → Backend Dev
- `Phase` chứa `Deployment`/`Docker`/`CI` → DevOps
- Nếu không chắc → Architect quyết định và cập nhật `Assignee`/Notes

### 2.3 Rule chuyển vai trò ngay trong lúc làm
Trong một task, agent có thể phải đổi vai trò theo tình hình:
- Thiếu spec/acceptance criteria → chuyển **PM** để bổ sung spec ngay trong task file
- Cần tách nhỏ hoặc thêm dependency → chuyển **Architect** để cập nhật cấu trúc task/deps
- Code xong nhưng chưa đủ quality gates → giữ **Developer** cho tới khi pass
- Đã pass gates và đủ criteria → chuyển **Reviewer** để review và set `Done`

Điểm mấu chốt: **Role switching dựa trên “state” trong markdown** (Status/Notes/checkboxes), không dựa trên trí nhớ hội thoại.

---

## 3) Chuẩn hoá task file để “router” hoạt động ổn định

### 3.1 Status hợp lệ (non-negotiable)
Chỉ dùng đúng 5 status như trong `AI_WORKFLOW_INTEGRATION.md`:
- `Todo`
- `InProgress_By_[AgentName]`
- `Blocked_By_[Reason]`
- `NeedsReview`
- `Done`

### 3.2 Khuyến nghị thêm 2 block (optional nhưng rất đáng)
Bạn có thể thêm vào template task (không bắt buộc nhưng giúp loop “production ready” hơn):

**A) Quality Gates**
```markdown
## Quality Gates (must pass before NeedsReview)
- [ ] Typecheck: `<command>`
- [ ] Lint: `<command>`
- [ ] Tests: `<command>`

## Quality Gate Evidence
- Typecheck output (summary): ...
- Lint output (summary): ...
- Tests output (summary): ...
```

**B) Role Hint (router override)**
```markdown
**Suggested Role:** Backend_Dev | Frontend_Dev | Architect | PM | Reviewer | QA | DevOps
```
Nếu field này có mặt, router có thể ưu tiên nó (override) thay vì suy đoán theo Phase.

---

## 4) Cách dùng với Claude Code + ralph-wiggum

### 4.1 Prompt file (đề xuất)
Tạo một prompt file (ví dụ `.ft/prompt.md`) theo format:
- Nhận dạng agent name
- Luật status/assignee/deps
- Chỉ làm *một việc* trong iteration
- Có “escape hatch” sau N vòng: chuyển Blocked và log rõ
- Completion promise: dùng một token duy nhất, ví dụ `<promise>DONE</promise>`

Sau đó chạy:
```bash
/ralph-loop "$(cat .ft/prompt.md)" --completion-promise "<promise>DONE</promise>" --max-iterations 40
```

### 4.3 “One prompt” chạy tới production-ready
Nếu bạn muốn chỉ chạy **1 prompt duy nhất** và để agent tự chọn task/role liên tục:
- Dùng prompt: [prompts/project_production_ready_loop.md](../prompts/project_production_ready_loop.md)
- Chạy:
```bash
/ralph-loop "$(cat prompts/project_production_ready_loop.md)" --completion-promise "<promise>PROJECT_PRODUCTION_READY</promise>" --max-iterations 500
```

Prompt này sẽ tự gọi `scripts/ft_orchestrator.py` mỗi iteration để tạo `.ft/prompt.md` rồi làm theo.

### 4.2 Vì sao hợp với folder-tasks
- Ralph loop = tự động “retry/fix” cho đến khi pass tests/criteria.
- Task files = state; nên mỗi iteration Claude nhìn thấy thay đổi và tự điều chỉnh.
- Stop hook giữ agent “không thoát” khi chưa đạt promise.

---

## 5) Định nghĩa “Project Production Ready” (để outer loop biết khi nào dừng)

Gợi ý: tạo 1 task hoặc checklist release (Phase Deployment/Release) và coi nó là “gating task”.

Khuyến nghị thêm field máy-đọc được để orchestrator không phải hardcode theo tên file:
```markdown
**Gates:** ProductionReady
```

**Production-ready tối thiểu** (tuỳ stack):
- [ ] CI chạy được: install + typecheck + lint + tests
- [ ] Secrets/env vars documented
- [ ] Health checks / basic monitoring hooks
- [ ] Migration/seed strategy documented
- [ ] Security baseline (CSP/trusted origins/input validation)
- [ ] Deployment instructions + rollback notes

Outer loop chỉ được output `<promise>PROJECT_PRODUCTION_READY</promise>` khi **tất cả tasks có `Gates: ProductionReady`** đều `Done`.

---

## 6) Thực thi an toàn trong môi trường multi-agent

Vì repo này có thể chạy nhiều agent song song:
- Mỗi agent chỉ claim task bằng cách **update task file trước** (Status + Assignee + Last Updated + AI Agent Log)
- Không đụng vào task đang `InProgress_By_Another_Agent`
- Nếu cần re-assign: làm qua task file (Notes + đổi Assignee) để tránh race

---

## 7) Next step đề xuất
Nếu bạn muốn mình “đóng gói” đầy đủ:
- Tạo prompt templates theo role trong `prompts/`
- Tạo script router/orchestrator trong `scripts/` để:
  - scan tasks
  - chọn next task
  - chọn role
  - generate prompt file

Mình đã scaffold sẵn các phần này trong các bước tiếp theo.
