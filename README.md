Đây là tài liệu về cách tạo task management theo cấu trúc thư mục, phong cách giống jira nhằm quản lý tiến độ dự án và khối lượng công việc cho các AI cùng nhau làm việc.
Task theo cấu trúc thư mục Version/Phase/task-NN.md Cấu trúc Thư mục và file:
/project_root
├── docs/
│   ├── TASKS_OVERVIEW.md  <-- File tổng quan cấp cao
│   │
│   ├── V1_MVP/  <-- Version 1: Minimum Viable Product
│   │   ├── 00_Project_Setup_And_Environment/  <-- Giai đoạn 0
│   │   │   ├── task_00.01_rust_axum_backend_setup.md
│   │   │   ├── task_00.02_sveltekit_frontend_setup.md
│   │   │   ├── task_00.03_surrealdb_local_setup.md
│   │   │   └── task_00.04_docker_configuration_dev.md
│   │   │
│   │   ├── 01_Database_Schema_And_Seed_Data/  <-- Giai đoạn 1
│   │   │   ├── task_01.01_define_core_schemas.md
│   │   │   ├── task_01.02_create_seed_data_files.md
│   │   │   └── task_01.03_implement_seeding_script.md
│   │   │
│   │   ├── 02_Backend_Core_Features/  <-- Giai đoạn 2
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
│   │   ├── 03_Frontend_Core_UI/  <-- Giai đoạn 3
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
│   └── ARCHIVED_TASKS/
│       └── V1_MVP_COMPLETED/ (Khi một version hoàn thành, có thể di chuyển thư mục version đó vào đây)
│
└── src/
    └── ... (mã nguồn dự án)

Dưới đây là cách bạn có thể triển khai và những điểm cần lưu ý:

1. Phân công Công việc (Task Assignment):

Trường Người thực hiện: Trong mỗi file task_XX.YY.ZZ_ten_task.md, trường Người thực hiện trở nên cực kỳ quan trọng.
Bạn (hoặc một AI "quản lý dự án" nếu có) sẽ gán một task cụ thể cho một AI agent cụ thể. Ví dụ: Người thực hiện: AI_Agent_Alpha hoặc Người thực hiện: AI_Agent_Beta.
Một AI agent chỉ nên làm việc trên các task đã được gán cho mình.
Hàng đợi Task (Task Queue):
Bạn có thể duy trì một danh sách các task "Sẵn sàng để làm" (ví dụ, trong TASKS_OVERVIEW.md hoặc một file riêng READY_TASKS.md).
Khi một AI agent hoàn thành task hiện tại, nó có thể "nhận" một task mới từ hàng đợi này, hoặc bạn sẽ gán task tiếp theo cho nó.
2. Trạng thái Task và "Khóa" (Task Status & Locking):

Cập nhật Trạng thái ngay lập tức:
Khi một AI agent bắt đầu làm một task, nó phải cập nhật ngay trường Trạng thái trong file task đó thành một cái gì đó như InProgress_By_Agent_Alpha. Điều này hoạt động như một cơ chế "khóa mềm" (soft lock), báo cho các agent khác biết task này đang được xử lý.
Các trạng thái khác có thể là: Todo (chưa ai làm), Blocked (bị chặn bởi task khác), NeedsReview (cần bạn xem lại), Done.
Quy ước: Một AI agent không được phép chỉnh sửa một task đang có trạng thái InProgress_By_Another_Agent.
3. Quản lý Phụ thuộc (Dependency Management):

Trường Dependencies: AI agent phải kiểm tra kỹ trường Dependencies trong file task.
Một task chỉ nên được bắt đầu khi tất cả các task phụ thuộc của nó đã có trạng thái Done.
Điều này đảm bảo công việc được thực hiện theo đúng thứ tự.
4. Làm việc với Mã nguồn Chung (Shared Codebase):

Version Control (Git): Đây là điều bắt buộc.
Mỗi AI agent (hoặc bạn thay mặt AI) cần commit các thay đổi liên quan đến task của mình.
Trước khi bắt đầu một task liên quan đến code, AI agent cần git pull để lấy những thay đổi mới nhất từ các agent khác.
Xử lý Xung đột (Merge Conflicts): Đây là phần phức tạp.
Lý tưởng nhất là các task được chia đủ nhỏ và độc lập để giảm thiểu xung đột.
Nếu xung đột xảy ra, có thể cần sự can thiệp của bạn để giải quyết. Hoặc, một AI agent có thể tạm dừng, đánh dấu task là Blocked_By_Merge_Conflict và thông báo cho bạn.
Tần suất Commit: Khuyến khích các commit nhỏ, thường xuyên cho từng phần nhỏ của sub-task hoàn thành.
5. Giao tiếp và Đồng bộ (Communication & Synchronization):

Thông qua File Task: Các file task chính là kênh giao tiếp chính. AI agent cập nhật trạng thái, log công việc vào AI Agent Log.
TASKS_OVERVIEW.md: File này giúp tất cả các agent (và bạn) có cái nhìn tổng quan về tiến độ chung.
Thông báo cho Bạn: Khi một AI agent hoàn thành một task quan trọng, gặp vấn đề, hoặc cần review, nó nên thông báo cho bạn.
6. Vai trò của Bạn (Người Điều phối - Orchestrator):

Phân công ban đầu: Bạn sẽ là người quyết định task nào giao cho agent nào, hoặc thiết lập các quy tắc để agent tự nhận task.
Theo dõi tiến độ: Dựa vào TASKS_OVERVIEW.md và trạng thái của các file task.
Giải quyết xung đột: Can thiệp khi có vấn đề (merge conflict, task bị block lâu, hiểu sai yêu cầu).
Review công việc: Kiểm tra các task đã được đánh dấu NeedsReview hoặc Done.
Cách một AI Agent có thể hoạt động trong môi trường này:

Kiểm tra Task được giao: "Cascade, có task nào được gán cho tôi không?" hoặc "Cascade, hãy tìm một task Todo trong giai đoạn 02_Backend_Core_Features mà tôi có thể làm."
Nhận Task: Nếu có task phù hợp và chưa ai làm (hoặc được gán cho mình):
Đọc kỹ file task.
Kiểm tra Dependencies. Nếu chưa xong, báo lại và chờ.
Cập nhật Trạng thái thành InProgress_By_MyName.
Thực hiện Task:
Thực hiện từng sub-task.
Nếu liên quan đến code: git pull, code, test, git commit, git push.
Cập nhật checkbox của sub-task.
Hoàn thành Task:
Cập nhật Trạng thái thành Done (hoặc NeedsReview).
Ghi log cuối cùng vào AI Agent Log.
Thông báo cho bạn.
Lặp lại: Tìm task mới.
Ví dụ về phân công:

Agent Alpha: Chịu trách nhiệm chính cho Giai đoạn 02_Backend_Core_Features. Nó sẽ tuần tự làm các task trong thư mục đó.
Agent Beta: Chịu trách nhiệm chính cho Giai đoạn 03_Frontend_Core_UI.
Agent Gamma (hoặc bạn): Xử lý các task trong 00_Project_Setup và 01_Database_Schema, vì đây là nền tảng.
Thách thức:

Đảm bảo AI hiểu đúng ngữ cảnh: Mỗi AI agent có thể có "bộ nhớ" hoặc ngữ cảnh riêng. Việc các file task chứa đầy đủ thông tin và link đến tài liệu liên quan là rất quan trọng.
Xử lý lỗi và tình huống bất ngờ: Cần có cơ chế để AI báo cáo khi gặp khó khăn không tự giải quyết được.

----------------------------------------------------------------------------------------

Phác thảo Quy trình Làm việc của AI Agent với Hệ thống Task Markdown

Giai đoạn 0: Thiết lập Ban đầu (Thực hiện một lần hoặc khi có thay đổi lớn)

Hiểu Cấu Trúc Task:
AI agent được cung cấp thông tin về cấu trúc thư mục (Version/Phase/task-NN.md) và nội dung mẫu của một file task chi tiết.
AI agent biết về sự tồn tại và mục đích của TASKS_OVERVIEW.md.
Công cụ: AI agent nhận biết rằng việc cập nhật file .md (đánh dấu checkbox, thay đổi trạng thái, ghi log) sẽ được thực hiện thông qua việc đề xuất thay đổi nội dung file (ví dụ, sử dụng công cụ propose_code trong "chat mode" của tôi, bạn sẽ là người áp dụng thay đổi đó).
Giai đoạn 1: Nhận và Khởi tạo Task

Tìm Task để Làm:
Ưu tiên 1 (Giao việc trực tiếp): USER yêu cầu AI agent làm một task cụ thể bằng cách chỉ rõ đường dẫn file task (ví dụ: "Cascade, hãy làm task V1_MVP/02_Backend_Core_Features/.../task_A.md").
Ưu tiên 2 (Tự tìm task): Nếu không có giao việc trực tiếp, USER có thể yêu cầu: "Cascade, hãy tìm một task Todo trong giai đoạn [Tên Giai Đoạn] thuộc version [Tên Version] mà chưa ai thực hiện hoặc được gán cho bạn."
AI agent sẽ quét các file task trong thư mục chỉ định, kiểm tra trường Trạng thái và Người thực hiện.
Có thể ưu tiên theo số thứ tự file task hoặc trường Ưu tiên trong file.
Đọc và Hiểu Task:
Mở và đọc kỹ toàn bộ nội dung file task được chọn: Mô tả chi tiết, Tiêu chí hoàn thành, Các công việc con cụ thể, Tài liệu liên quan, Dependencies.
Kiểm tra Dependencies:
Xem xét mục Dependencies. Đối với mỗi dependency:
Kiểm tra file task tương ứng xem Trạng thái có phải là Done không.
Nếu bất kỳ dependency nào chưa Done, AI agent báo lại cho USER, cập nhật Trạng thái của task hiện tại thành Blocked_By_Dependency_[ID_Task_Phụ_Thuộc] và có thể tìm task khác.
"Nhận" Task và Cập nhật Trạng thái:
Nếu tất cả dependencies đã Done (hoặc không có):
AI agent đề xuất cập nhật file task hiện tại:
Thay đổi Trạng thái: thành InProgress_By_[Tên_AI_Agent] (ví dụ: InProgress_By_Cascade).
Cập nhật Ngày cập nhật cuối: thành ngày hiện tại.
Thêm một dòng vào AI Agent Log: ghi nhận việc bắt đầu task (ví dụ: "[YYYY-MM-DD HH:MM]: Bắt đầu xử lý task. Đã kiểm tra dependencies.").
Chuẩn bị Môi trường (Nếu task liên quan đến code):
Thực hiện git pull trên nhánh chính (ví dụ: main hoặc develop) để đảm bảo có code mới nhất.
Nếu task yêu cầu tạo nhánh mới, AI agent sẽ đề xuất lệnh tạo nhánh.
Giai đoạn 2: Thực hiện Task

Xử lý Tuần tự các Công việc Con (Sub-tasks):
AI agent đi qua từng mục trong Các công việc con cụ thể.
Đối với mỗi sub-task:
Hiểu rõ yêu cầu của sub-task.
Thực hiện hành động cần thiết:
Nếu là viết code: Soạn thảo code, tuân thủ các quy tắc và coding convention của dự án.
Nếu là cập nhật tài liệu: Soạn thảo nội dung cập nhật.
Nếu là chạy lệnh: Đề xuất lệnh cần chạy.
Sử dụng các công cụ phù hợp (ví dụ: propose_code để đề xuất thay đổi code hoặc nội dung file, view_file để xem file, grep_search để tìm kiếm).
Cập nhật Tiến độ Sub-task:
Sau khi hoàn thành một sub-task, AI agent đề xuất cập nhật file task:
Đánh dấu checkbox của sub-task đó là hoàn thành: [x].
Thêm log chi tiết vào AI Agent Log: về sub-task vừa hoàn thành (ví dụ: "[YYYY-MM-DD HH:MM]: Hoàn thành sub-task 2.1: Định nghĩa struct Request. Đã đề xuất code.").
Commit Code Thường Xuyên (Nếu task liên quan đến code):
Sau khi hoàn thành một hoặc một vài sub-task có ý nghĩa, AI agent đề xuất các lệnh git add, git commit -m "TaskID: Mô tả commit" (ví dụ: git commit -m "task_02.01.01: Implement request validation for user registration").
Xử lý Vấn đề Phát sinh (Blockers):
Nếu gặp vấn đề không tự giải quyết được (ví dụ: thiếu thông tin, xung đột code không tự giải quyết, một API bên ngoài không hoạt động):
AI agent đề xuất cập nhật file task:
Thay đổi Trạng thái: thành Blocked_By_[Mô_Tả_Ngắn_Về_Lý_Do_Block].
Ghi rõ vấn đề vào AI Agent Log:.
Thông báo cho USER về tình trạng bị block và lý do.
AI agent có thể dừng task đó và chờ USER giải quyết, hoặc hỏi USER xem có nên chuyển sang task khác không.
Giai đoạn 3: Hoàn thành và Đề xuất Review Task

Kiểm tra Toàn bộ Task:
Sau khi tất cả các sub-task được đánh dấu [x]:
AI agent rà soát lại toàn bộ Tiêu chí hoàn thành để đảm bảo tất cả đã được đáp ứng.
Cập nhật Trạng thái Hoàn thành:
AI agent đề xuất cập nhật file task:
Thay đổi Trạng thái: thành NeedsReview (nếu cần USER xem lại) hoặc Done (nếu task không cần review hoặc AI được phép tự đánh dấu Done).
Cập nhật Ngày cập nhật cuối:.
Thêm log cuối cùng vào AI Agent Log: (ví dụ: "[YYYY-MM-DD HH:MM]: Tất cả sub-tasks hoàn thành. Task chuyển trạng thái NeedsReview.").
Finalize Code (Nếu task liên quan đến code):
Đảm bảo tất cả thay đổi code đã được commit.
Đề xuất git push cho nhánh làm việc.
Nếu quy trình yêu cầu Pull Request (PR), AI agent có thể đề xuất tạo PR (nêu rõ tiêu đề, mô tả dựa trên thông tin task).
Thông báo cho USER:
AI agent thông báo cho USER rằng task đã hoàn thành và sẵn sàng để review (hoặc đã Done), kèm theo đường dẫn đến file task và PR (nếu có).
Giai đoạn 4: Sau Review (Nếu có)

Nhận Phản hồi:
USER review task (và code nếu có) và cung cấp phản hồi (có thể ghi trực tiếp vào mục Ghi chú / Thảo luận của file task hoặc qua chat).
Xử lý Phản hồi:
Nếu có yêu cầu thay đổi:
AI agent đề xuất cập nhật Trạng thái: của task về lại InProgress_By_[Tên_AI_Agent].
Thực hiện các thay đổi theo phản hồi (có thể coi như các sub-task mới hoặc làm lại sub-task cũ).
Lặp lại các bước ở Giai đoạn 2 và 3 cho đến khi USER chấp thuận.
Đóng Task:
Khi USER chấp thuận, đảm bảo Trạng thái: trong file task là Done.
Nếu có PR, USER hoặc AI agent (nếu được phép) sẽ merge PR.