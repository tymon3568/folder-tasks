# Task: User Registration Endpoint (Example)

**Task ID:** `V1_MVP/02_Backend_Core_Features/02.01_Authentication/task_02.01.01_user_registration_endpoint.md`
**Version:** V1_MVP
**Phase:** 02_Backend_Core_Features
**Module:** 02.01_Authentication
**Priority:** High
**Status:** Todo <!-- Todo, InProgress, Blocked, NeedsReview, Done, Cancelled -->
**Assignee (If any):**
**Created Date:** 2025-06-05
**Last Updated:** 2025-06-05

## 1. Detailed Description
Create API endpoint that allows new users to register an account. The endpoint needs to receive user information (email, password, name), validate input, hash password, and save information to database.

## 2. UI/UX Specifications (If Frontend Task)
> *Note: Since this is a Backend task, this section serves as reference for API requirements.*
*   **Design:** [Figma Link Placeholder]
*   **Form Fields:** Email, Full Name, Password, Confirm Password.
*   **States:**
    *   Loading spinner during API call.
    *   Inline validation errors (Red text).
    *   Success toast on 201 Created.

## 3. Workflow / Interaction Flow
1.  **Client** sends `POST /api/v1/auth/register` with JSON payload.
2.  **Server (Axum)** receives request.
3.  **Validation Layer:**
    *   Check email format (Regex).
    *   Check password complexity (Min 8 chars).
    *   Check if email already exists in `users` table.
4.  **Processing:**
    *   Hash password using Argon2.
    *   Create `User` record in SurrealDB.
    *   Generate JWT Token.
5.  **Response:**
    *   Return 201 Created + User Data + Token.
    *   Or Return 400/409/500 with Error Code.

## 4. Technical Specifications
### 4.1. API & Data
*   **Endpoint:** `POST /api/v1/auth/register`
*   **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "SecretPassword123!",
      "full_name": "John Doe"
    }
    ```
*   **Response (Success):**
    ```json
    {
      "user": {
        "id": "users:ulid_string",
        "email": "user@example.com",
        "full_name": "John Doe",
        "created_at": "2025-06-05T10:00:00Z"
      },
      "token": "eyJhbGciOiJIUzI1Ni..."
    }
    ```

### 4.2. Error Mapping
| HTTP Code | Error Code | Message Key | Condition |
| :--- | :--- | :--- | :--- |
| 400 | `VAL_INVALID_EMAIL` | `auth.error.invalid_email` | Regex fail |
| 400 | `VAL_WEAK_PASSWORD` | `auth.error.weak_password` | < 8 chars |
| 409 | `AUTH_EMAIL_EXISTS` | `auth.error.email_exists` | Email found in DB |
| 500 | `SYS_INTERNAL_ERROR`| `common.error.internal` | DB connection fail |

## 5. Non-Functional Requirements (Constraints)
*   **Security:** NEVER log raw passwords.
*   **Performance:** Hashing (Argon2) should be tuned to take ~0.5s (balance security/speed).
*   **Code Quality:** Structs must use `validator` crate annotations.

## 6. Implementation Steps (Specific Sub-tasks)
- [ ] 1. Define Request and Response structs for API in Rust.
    - [ ] 1.1. `RegisterUserRequest { email, password, full_name }`
    - [ ] 1.2. `UserResponse` & `AuthResponse`
- [ ] 2. Write validation logic for `email` & `password`.
- [ ] 3. Integrate password hashing library (`argon2`).
- [ ] 4. Write handler function for endpoint in Axum.
    - [ ] 4.1. Receive and deserialize request.
    - [ ] 4.2. Call validation functions.
    - [ ] 4.3. Check DB for duplicate email.
    - [ ] 4.4. Hash password.
    - [ ] 4.5. Execute SurrealQL `INSERT`.
    - [ ] 4.6. Generate JWT.
- [ ] 5. Register route in Axum Router.
- [ ] 6. Write Unit/Integration Tests.
- [ ] 7. Update `API_SPEC.yaml`.
- [ ] 8. (AI Agent) Review code for best practices.

## 7. AI Context (Hints for Agent)
*   **Reference Files:**
    *   `src/models/user_model.rs` (Struct definitions)
    *   `src/web/routes_auth.rs` (Handler implementation)
    *   `docs/SCHEMA.surql` (Database Schema)

## 8. Completion Criteria
- [ ] Endpoint `POST /api/v1/auth/register` is accessible.
- [ ] Valid registration returns 201 + Token.
- [ ] Duplicate email returns 409.
- [ ] Invalid password returns 400.
- [ ] Passwords are stored as hashes (not plain text).
- [ ] Unit tests pass.

## Notes / Discussion:
- Consider using `validator` library for struct validation.
- Decision on JWT token expiration time.

---
## AI Agent Log (For AI updates):
*   *2025-06-05 10:30: Started processing task. Reviewed `SCHEMA.surql`.*