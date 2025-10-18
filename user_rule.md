<!-- Ví dụ cách bạn có thể thêm vào user_rules của mình -->
<rule name="task_management_workflow">
    <description>Quy tắc cho AI agent khi làm việc với hệ thống task Markdown.</description>
    <guideline>Khi được yêu cầu làm việc với một task trong hệ thống task Markdown (cấu trúc Version/Phase/task-NN.md):</guideline>
    <guideline>1.  **Nhận Task:** Chỉ làm việc trên task được giao trực tiếp hoặc task 'Todo' phù hợp với yêu cầu tìm kiếm của USER. Luôn kiểm tra và tôn trọng trường 'Người thực hiện'.</guideline>
    <guideline>2.  **Kiểm tra Dependencies:** Trước khi bắt đầu, xác minh tất cả các task trong mục 'Dependencies' của file task đã ở trạng thái 'Done'. Nếu chưa, thông báo cho USER và không tiến hành trừ khi được chỉ dẫn khác.</guideline>
    <guideline>3.  **Cập nhật Trạng thái:** Ngay khi bắt đầu một task, đề xuất cập nhật trạng thái của file task thành 'InProgress_By_[Tên_AI_Agent]' và ghi log vào 'AI Agent Log'.</guideline>
    <guideline>4.  **Thực hiện Sub-tasks:** Xử lý tuần tự các công việc con. Sau mỗi sub-task hoàn thành, đề xuất đánh dấu checkbox và ghi log chi tiết vào 'AI Agent Log'.</guideline>
    <guideline>5.  **Quản lý Code (Nếu có):** Luôn `git pull` trước khi bắt đầu code. Đề xuất `git commit` thường xuyên với message rõ ràng (bao gồm TaskID). Đề xuất `git push` khi hoàn thành phần code của task.</guideline>
    <guideline>6.  **Xử lý Blockers:** Nếu gặp vấn đề, đề xuất cập nhật trạng thái task thành 'Blocked_By_[Lý_Do]', ghi log chi tiết và thông báo ngay cho USER.</guideline>
    <guideline>7.  **Hoàn thành Task:** Khi tất cả sub-tasks và tiêu chí hoàn thành được đáp ứng, đề xuất cập nhật trạng thái task thành 'NeedsReview' (hoặc 'Done' nếu phù hợp) và thông báo cho USER.</guideline>
    <guideline>8.  **Cập nhật File Task:** Mọi thay đổi đối với file task (trạng thái, checkbox, log) phải được thực hiện bằng cách đề xuất nội dung cập nhật cho USER áp dụng (ví dụ: qua công cụ `propose_code`).</guideline>
    <guideline>9.  **Giao tiếp:** Thường xuyên thông báo cho USER về tiến độ, các vấn đề gặp phải, và khi task hoàn thành hoặc cần review.</guideline>
    <guideline>10. **Bám sát file task:** Luôn lấy thông tin chi tiết, tiêu chí hoàn thành, và các bước thực hiện từ file task được chỉ định. Không tự ý thay đổi phạm vi task trừ khi được USER đồng ý và cập nhật vào file task.</guideline>
</rule>