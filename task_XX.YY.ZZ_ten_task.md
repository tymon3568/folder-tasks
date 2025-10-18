Nội dung Mẫu cho một file task_XX.YY.ZZ_ten_task.md:
# Task: User Registration Endpoint

**ID Task:** `V1_MVP/02_Backend_Core_Features/02.01_Authentication/task_02.01.01_user_registration_endpoint.md`
**Version:** V1_MVP
**Giai đoạn:** 02_Backend_Core_Features
**Module:** 02.01_Authentication
**Ưu tiên:** Cao
**Trạng thái:** Todo <!-- Todo, InProgress, Blocked, NeedsReview, Done -->
**Người thực hiện (Nếu có):**
**Ngày tạo:** 2025-06-05
**Ngày cập nhật cuối:** 2025-06-05

## Mô tả chi tiết:
Tạo endpoint API cho phép người dùng mới đăng ký tài khoản. Endpoint cần nhận thông tin người dùng (email, password, tên), xác thực đầu vào, hash mật khẩu, và lưu thông tin vào database.

## Tiêu chí hoàn thành (Acceptance Criteria):
- [ ] Endpoint `POST /api/v1/auth/register` được tạo.
- [ ] Nhận đầu vào: `email`, `password`, `full_name`.
- [ ] Validate email (định dạng, không trùng lặp).
- [ ] Validate password (độ dài tối thiểu, độ phức tạp cơ bản).
- [ ] Hash mật khẩu bằng Argon2 (hoặc bcrypt) trước khi lưu.
- [ ] Lưu thông tin user mới vào bảng `users` trong SurrealDB.
- [ ] Trả về thông tin user (không bao gồm password hash) và token JWT nếu đăng ký thành công.
- [ ] Trả về lỗi phù hợp nếu validate thất bại hoặc có lỗi server.
- [ ] Có unit tests cho logic đăng ký.
- [ ] Cập nhật `API_SPEC.yaml` với định nghĩa endpoint mới.

## Các công việc con cụ thể (Sub-tasks):
- [ ] 1. Định nghĩa struct Request và Response cho API trong Rust.
    - [ ] 1.1. `RegisterUserRequest { email: String, password: String, full_name: String }`
    - [ ] 1.2. `UserResponse { id: RecordId, email: String, full_name: String, created_at: Datetime }` (hoặc tương tự)
    - [ ] 1.3. `AuthResponse { user: UserResponse, token: String }`
- [ ] 2. Viết logic validate cho `email` (sử dụng regex, kiểm tra tồn tại trong DB).
- [ ] 3. Viết logic validate cho `password` (ví dụ: ít nhất 8 ký tự).
- [ ] 4. Tích hợp thư viện hashing mật khẩu (ví dụ: `argon2`).
- [ ] 5. Viết hàm xử lý (handler) cho endpoint trong Axum.
    - [ ] 5.1. Nhận và deserialize request.
    - [ ] 5.2. Gọi các hàm validate.
    - [ ] 5.3. Hash password.
    - [ ] 5.4. Tạo câu lệnh SurrealQL để `INSERT` user mới.
    - [ ] 5.5. Thực thi câu lệnh SurrealQL.
    - [ ] 5.6. Tạo JWT token.
    - [ ] 5.7. Serialize và trả về response thành công hoặc lỗi.
- [ ] 6. Đăng ký route trong Axum.
- [ ] 7. Viết Unit Tests:
    - [ ] 7.1. Test đăng ký thành công.
    - [ ] 7.2. Test đăng ký với email đã tồn tại.
    - [ ] 7.3. Test đăng ký với email không hợp lệ.
    - [ ] 7.4. Test đăng ký với password không hợp lệ.
- [ ] 8. Cập nhật file `API_SPEC.yaml`.
- [ ] 9. (AI Agent) Xem xét lại code và đảm bảo tuân thủ các quy tắc dự án.

## Tài liệu liên quan:
- `docs/prd-en.md` (Phần User Stories liên quan đến Đăng ký)
- `docs/SCHEMA.surql` (Bảng `users`)
- `docs/API_SPEC.yaml`
- `docs/TECHNICAL_SPEC.md` (Phần Authentication)

## Dependencies (Các task cần hoàn thành trước):
- `V1_MVP/01_Database_Schema_And_Seed_Data/task_01.01_define_core_schemas.md` (Đã định nghĩa bảng `users`)

## Ghi chú / Thảo luận:
- Cân nhắc sử dụng thư viện `validator` cho việc validate struct.
- Quyết định về thời gian hết hạn của JWT token.

---
## AI Agent Log (Dành cho AI cập nhật):
*   *2025-06-05 10:30: Bắt đầu xử lý task. Đã xem xét `SCHEMA.surql`.*
*   *2025-06-05 11:00: Đề xuất struct Request/Response cho sub-task 1.*
---