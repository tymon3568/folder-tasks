Sample Content for a task_XX.YY.ZZ_ten_task.md:
# Task: User Registration Endpoint

**Task ID:** `V1_MVP/02_Backend_Core_Features/02.01_Authentication/task_02.01.01_user_registration_endpoint.md`
**Version:** V1_MVP
**Phase:** 02_Backend_Core_Features
**Module:** 02.01_Authentication
**Priority:** High
**Status:** Todo <!-- Todo, InProgress, Blocked, NeedsReview, Done -->
**Assignee (If any):**
**Created Date:** 2025-06-05
**Last Updated:** 2025-06-05

## Detailed Description:
Create API endpoint that allows new users to register an account. The endpoint needs to receive user information (email, password, name), validate input, hash password, and save information to database.

## Completion Criteria (Acceptance Criteria):
- [ ] Endpoint `POST /api/v1/auth/register` is created.
- [ ] Receives input: `email`, `password`, `full_name`.
- [ ] Validate email (format, no duplicates).
- [ ] Validate password (minimum length, basic complexity).
- [ ] Hash password using Argon2 (or bcrypt) before saving.
- [ ] Save new user information to `users` table in SurrealDB.
- [ ] Return user information (excluding password hash) and JWT token if registration is successful.
- [ ] Return appropriate error if validation fails or server error occurs.
- [ ] Have unit tests for registration logic.
- [ ] Update `API_SPEC.yaml` with new endpoint definition.

## Specific Sub-tasks:
- [ ] 1. Define Request and Response structs for API in Rust.
    - [ ] 1.1. `RegisterUserRequest { email: String, password: String, full_name: String }`
    - [ ] 1.2. `UserResponse { id: RecordId, email: String, full_name: String, created_at: Datetime }` (or similar)
    - [ ] 1.3. `AuthResponse { user: UserResponse, token: String }`
- [ ] 2. Write validation logic for `email` (use regex, check existence in DB).
- [ ] 3. Write validation logic for `password` (e.g., at least 8 characters).
- [ ] 4. Integrate password hashing library (e.g., `argon2`).
- [ ] 5. Write handler function for endpoint in Axum.
    - [ ] 5.1. Receive and deserialize request.
    - [ ] 5.2. Call validation functions.
    - [ ] 5.3. Hash password.
    - [ ] 5.4. Create SurrealQL statement to `INSERT` new user.
    - [ ] 5.5. Execute SurrealQL statement.
    - [ ] 5.6. Generate JWT token.
    - [ ] 5.7. Serialize and return success response or error.
- [ ] 6. Register route in Axum.
- [ ] 7. Write Unit Tests:
    - [ ] 7.1. Test successful registration.
    - [ ] 7.2. Test registration with existing email.
    - [ ] 7.3. Test registration with invalid email.
    - [ ] 7.4. Test registration with invalid password.
- [ ] 8. Update `API_SPEC.yaml` file.
- [ ] 9. (AI Agent) Review code and ensure compliance with project rules.

## Related Documentation:
- `docs/prd-en.md` (Registration related User Stories section)
- `docs/SCHEMA.surql` (Users table)
- `docs/API_SPEC.yaml`
- `docs/TECHNICAL_SPEC.md` (Authentication section)

## Dependencies (Tasks that need to be completed first):
- `V1_MVP/01_Database_Schema_And_Seed_Data/task_01.01_define_core_schemas.md` (Users table has been defined)

## Notes / Discussion:
- Consider using `validator` library for struct validation.
- Decision on JWT token expiration time.

---
## AI Agent Log (For AI updates):
*   *2025-06-05 10:30: Started processing task. Reviewed `SCHEMA.surql`.*
*   *2025-06-05 11:00: Proposed Request/Response structs for sub-task 1.*
---