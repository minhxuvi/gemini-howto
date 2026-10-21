# Mục Lục Tra Cứu Toàn Diện (A–Z & Theo Tình Huống Thực Tế)

[English](../INDEX.md) | **Tiếng Việt**

Sử dụng mục lục này để tra cứu nhanh bất kỳ khái niệm, tên file, lệnh slash, cờ CLI hoặc giải pháp cho tình huống thực tế nào trong **Google Antigravity & Gemini**.

---

## Phần 1: Tra Cứu Theo Tình Huống Thực Tế ("Tôi Muốn...")

| Tình Huống / Vấn Đề Của Bạn | Giải Pháp Khuyến Nghị | Module Tham Chiếu |
| :--- | :--- | :--- |
| *"Tôi muốn kiểm tra trình độ hiện tại và nhận lộ trình học riêng"* | Chạy lệnh `/self-assessment` trong Antigravity App hoặc `agy` CLI | [`.agents/skills/self-assessment/`](../.agents/skills/self-assessment/README.md) |
| *"Tôi vừa đọc xong một bài và muốn làm trắc nghiệm 5 câu hỏi"* | Chạy `/lesson-quiz 01` (hoặc số module từ `01` đến `10`) | [`.agents/skills/lesson-quiz/`](../.agents/skills/lesson-quiz/README.md) |
| *"Tôi muốn agent hỏi ngược lại tôi để làm rõ thiết kế trước khi code"* | Dùng lệnh `/grill-me` hoặc `/plan` | [Module 01](01-slash-commands/README.md) |
| *"Tôi muốn hỏi một câu phụ nhanh mà không làm loãng luồng làm việc chính"* | Dùng lệnh `/btw <câu hỏi>` | [Module 01](01-slash-commands/README.md) |
| *"Tôi muốn agent tự động chạy đến khi toàn bộ test xanh mới dừng"* | Dùng lệnh `/goal <mục tiêu>` hoặc tạo `Stop` hook kiểm tra test | [Module 01](01-slash-commands/README.md), [Module 06](06-hooks/README.md) |
| *"Tôi muốn lưu lại quy tắc vừa dạy cho agent thành file cấu hình lâu dài"* | Dùng lệnh `/learn` để tạo `learning_proposal.md` | [Module 01](01-slash-commands/README.md), [Module 02](02-memory/README.md) |
| *"File `GEMINI.md` của nhóm quá dài và tốn nhiều token ngữ cảnh"* | Giữ `GEMINI.md` dưới 2.000 token; tách phần chuyên biệt sang `.agents/rules/*.md` với `trigger: model_decision` hoặc `glob` | [Module 02](02-memory/README.md) |
| *"Tôi muốn tạo một lệnh `/deploy` hoặc `/review` dùng chung cho cả nhóm"* | Tạo file `.agents/skills/<name>/SKILL.md` kèm thư mục `scripts/` và `references/` | [Module 01](01-slash-commands/README.md), [Module 03](03-skills/README.md) |
| *"Tôi muốn tìm kiếm trên 50 file mà không làm đầy cửa sổ ngữ cảnh chính"* | Ủy quyền cho subagent `research` qua công cụ `invoke_subagent` | [Module 04](04-subagents/README.md) |
| *"Tôi muốn chạy 2 phương án code song song mà không đè lên file của nhau"* | Gọi `invoke_subagent` với `Workspace: "branch"` hoặc `Workspace: "share"` | [Module 04](04-subagents/README.md) |
| *"Tôi muốn kết nối agent với PostgreSQL hoặc GitHub PR trực tiếp"* | Cấu hình `~/.gemini/config/mcp_config.json` (Stdio hoặc Streamable HTTP) | [Module 05](05-mcp/README.md) |
| *"MCP server bị lỗi khi khởi động và tôi không rõ nguyên nhân"* | Mở `/mcp` và nhấn nút **Fix with Agent** để agent tự chẩn đoán và sửa cấu hình | [Module 05](05-mcp/README.md) |
| *"Tôi muốn chặn tuyệt đối việc agent đọc file `.env` hoặc chạy `rm -rf`"* | Thiết lập quy tắc `Deny` trong `/permissions` kết hợp `PreToolUse` hook trong `.agents/hooks.json` | [Module 06](06-hooks/README.md), [Module 09](09-advanced-features/README.md) |
| *"Tôi muốn tự động chạy `prettier`/`ruff` mỗi khi agent sửa xong một file"* | Tạo `PostToolUse` hook bắt sự kiện `write_to_file\|replace_file_content` trong `.agents/hooks.json` | [Module 06](06-hooks/README.md) |
| *"Tôi muốn đóng gói toàn bộ skills, agents, hooks và MCP cho 20 repo của công ty"* | Tạo gói Native Plugin với `plugin.json` và kiểm định bằng `agy plugin validate --strict` | [Module 07](07-plugins/README.md) |
| *"Agent vừa sửa sai hướng, tôi muốn quay lại 3 bước trước hoặc rẽ nhánh thử cách khác"* | Dùng `/rewind` (`/undo`) để hoàn tác, hoặc `/fork` (`/branch`) để rẽ nhánh song song | [Module 08](08-checkpoints/README.md) |
| *"Tôi muốn hiển thị biểu đồ tương tác hoặc bảng lọc dữ liệu ngay trong khung chat"* | Yêu cầu agent tạo widget Generative UI bằng thẻ `<agent-embed>` và `tailwindcss.min.js` | [Module 08](08-checkpoints/README.md) |
| *"Tôi đang gặp một lỗi race condition cực khó hoặc bài toán tối ưu phức tạp"* | Chạy `/boost <mô tả bài toán>` để kích hoạt quy trình 3 giai đoạn với `DeepCoder` và `DeepInvestigator` | [Module 09](09-advanced-features/README.md) |
| *"Tôi muốn xây dựng một phân hệ lớn có các tác nhân tự phản biện và kiểm toán chéo"* | Chạy `/teamwork-preview <nhiệm vụ>` để huy động `Sentinel`, `Critic`, `Challenger` và `Auditor` | [Module 09](09-advanced-features/README.md) |
| *"Tôi muốn tích hợp Antigravity vào GitHub Actions CI/CD hoặc gọi từ dịch vụ Python"* | Dùng `agy -p ... --mode auto --output-format json` hoặc thư viện Python `google-antigravity` | [Module 10](10-cli/README.md) |

---

## Phần 2: Tra Cứu Theo Bảng Chữ Cái (A–Z)

### A
- **`AGENTS.md`**: Chuẩn mở đa tác nhân được Antigravity nạp tự động theo phân cấp thư mục cùng với `GEMINI.md` — [Module 02](02-memory/README.md)
- **`<agent-embed>`**: Thẻ HTML dùng để nhúng widget Generative UI tương tác trực tiếp vào luồng chat — [Module 08](08-checkpoints/README.md)
- **`agy` CLI**: Công cụ dòng lệnh chính thức của Google Antigravity (hỗ trợ TUI tương tác và `-p` headless) — [Module 10](10-cli/README.md)
- **`agy plugin validate`**: Lệnh kiểm tra tính hợp lệ của `plugin.json`, `hooks.json`, `mcp_config.json` và các thành phần trong plugin — [Module 07](07-plugins/README.md)
- **`agy remote-control`**: Khởi chạy kết nối điều khiển phiên cục bộ từ xa qua trình duyệt — [Module 09](09-advanced-features/README.md)
- **`always_on` (Trigger)**: Chế độ nạp quy tắc trong `.agents/rules/*.md` vào mọi lượt hội thoại (nằm trong ngân sách 20.000 token) — [Module 02](02-memory/README.md)
- **`ask_question` (Tool)**: Công cụ hiển thị hộp thoại câu hỏi trắc nghiệm tương tác cho người dùng — [Module 03](03-skills/README.md)

### B
- **`/boost`**: Chế độ suy luận sâu 3 giai đoạn sử dụng `Orchestrator`, `DeepCoder` và `DeepInvestigator` trên các worktree cô lập — [Module 09](09-advanced-features/README.md)
- **`/browser`**: Lệnh ủy quyền các tác vụ tương tác trình duyệt cho subagent trình duyệt — [Module 01](01-slash-commands/README.md), [Module 04](04-subagents/README.md)
- **`/btw`**: Đặt câu hỏi phụ nhanh trong lớp phủ tạm thời mà không làm thay đổi lịch sử hội thoại chính — [Module 01](01-slash-commands/README.md)

### C
- **Checkpoints (`/rewind`, `/undo`)**: Hệ thống lưu ảnh chụp trạng thái hội thoại và mã nguồn tự động ở mỗi lượt — [Module 08](08-checkpoints/README.md)
- **`CRON_TZ`**: Tiền tố khai báo múi giờ cho biểu thức cron trong `/schedule` và `sidecar.json` — [Module 08](08-checkpoints/README.md)
- **`Ctrl+J` / `Ctrl+K`**: Phím tắt TUI trong `agy` giúp nhảy nhanh tới subagent đang chờ duyệt quyền và phê duyệt nhanh — [Module 10](10-cli/README.md)

### D
- **`defaultRulesBudget` (20.000 token / 24 KB)**: Ngưỡng ngân sách ngữ cảnh dành cho các chỉ dẫn `always_on` — [Module 02](02-memory/README.md)
- **`define_subagent`**: Công cụ định nghĩa một loại subagent mới ngay trong phiên hội thoại hiện tại — [Module 04](04-subagents/README.md)
- **`Deny > Ask > Allow`**: Thứ tự ưu tiên bất biến khi đánh giá quy tắc phân quyền công cụ — [Module 09](09-advanced-features/README.md)

### F
- **Fix with Agent**: Nút chẩn đoán và sửa lỗi cấu hình MCP server tự động trong giao diện `/mcp` — [Module 05](05-mcp/README.md)
- **`/fork` (`/branch`)**: Nhân bản phiên hội thoại hiện tại thành một nhánh độc lập để thử nghiệm song song — [Module 08](08-checkpoints/README.md)
- **`fullyIdle`**: Trường boolean trong payload sự kiện `Stop` cho biết mọi subagent và tác vụ nền đã hoàn tất hay chưa — [Module 06](06-hooks/README.md)

### G
- **`GEMINI.md`**: File bộ nhớ chỉ dẫn cốt lõi của dự án hoặc cá nhân (`~/.gemini/GEMINI.md`) — [Module 02](02-memory/README.md), [`GEMINI.md`](GEMINI.md)
- **Gemini 4 Argon & Gemini 3.8 Flash**: Bộ đôi mô hình tiên phong cho suy luận kiến trúc sâu (Argon) và thực thi tốc độ cao (Flash) — [Module 09](09-advanced-features/README.md)
- **`glob` (Trigger)**: Chế độ kích hoạt quy tắc trong `.agents/rules/*.md` dựa trên mẫu đường dẫn file (`globs`) — [Module 02](02-memory/README.md)
- **`/goal`**: Chế độ thực thi tự hành bền bỉ cho đến khi đạt được mục tiêu đề ra — [Module 01](01-slash-commands/README.md)
- **`google-antigravity` (Python SDK)**: Thư viện Python chính thức để khởi tạo `Agent` và định nghĩa `@beta.workflows.define` — [Module 10](10-cli/README.md)
- **`/grill-me`**: Lệnh khởi chạy phiên phỏng vấn làm rõ thiết kế và các trường hợp biên trước khi code — [Module 01](01-slash-commands/README.md)

### H
- **`hooks.json`**: File cấu hình các sự kiện vòng đời tại `.agents/hooks.json`, `~/.gemini/config/hooks.json` hoặc gốc plugin — [Module 06](06-hooks/README.md)

### I
- **Implementation Plan**: Artifact kế hoạch triển khai hỗ trợ bình luận trực tiếp trên từng dòng trước khi nhấn **Proceed** — [Module 08](08-checkpoints/README.md)
- **`injectSteps`**: Trường JSON đầu ra của hook dùng để tiêm thêm bước kiểm tra hoặc thông điệp vào luồng của agent — [Module 06](06-hooks/README.md)
- **`invoke_subagent`**: Công cụ khởi chạy một hoặc nhiều subagent chạy nền đồng thời — [Module 04](04-subagents/README.md)

### L
- **`/learn`**: Lệnh đúc kết kinh nghiệm vừa giải quyết trong phiên thành rule hoặc skill lâu dài — [Module 01](01-slash-commands/README.md), [Module 02](02-memory/README.md)
- **`LiteRTAgentConfig`**: Cấu hình chạy mô hình cục bộ trên thiết bị (như Gemma 4) trong Python SDK — [Module 10](10-cli/README.md)

### M
- **`mcp_config.json`**: File cấu hình máy chủ Model Context Protocol (Stdio và Streamable HTTP) — [Module 05](05-mcp/README.md)
- **`model_decision` (Trigger)**: Chế độ nạp quy tắc tự động khi bộ định tuyến ngữ nghĩa thấy `description` khớp với yêu cầu hiện tại — [Module 02](02-memory/README.md)

### O
- **`overwrite`**: Trường JSON đầu ra của `PreToolUse` hook cho phép viết lại tham số đầu vào của công cụ trước khi thực thi — [Module 06](06-hooks/README.md)

### P
- **`plugin.json`**: File manifest định nghĩa gói plugin tại thư mục gốc của plugin — [Module 07](07-plugins/README.md)
- **`PreToolUse` / `PostToolUse` / `PreInvocation` / `PostInvocation`**: Các sự kiện vòng đời trong `hooks.json` — [Module 06](06-hooks/README.md)
- **Progressive Disclosure (Tiết lộ tăng dần 3 giai đoạn)**: Kiến trúc nạp siêu dữ liệu → `SKILL.md` → `references/` & `scripts/` giúp tiết kiệm tối đa token — [Module 03](03-skills/README.md)

### S
- **Sandbox (Seatbelt / `nsjail` / `AppContainer`)**: Cơ chế cô lập tiến trình cấp nhân hệ điều hành cho các lệnh shell — [Module 09](09-advanced-features/README.md)
- **`/schedule`**: Lệnh tạo hẹn giờ một lần hoặc tác vụ cron định kỳ — [Module 08](08-checkpoints/README.md)
- **`send_message`**: Công cụ giao tiếp phản ứng giữa subagent và tác nhân cha — [Module 04](04-subagents/README.md)
- **`sidecar.json` & `sidecar://`**: Cấu hình tiến trình/bảng điều khiển tương tác chạy song hành (như trình xem cấu trúc phân tử 3D) — [Module 08](08-checkpoints/README.md)
- **`SKILL.md`**: File định nghĩa kỹ năng trong `.agents/skills/<name>/SKILL.md` — [Module 03](03-skills/README.md)

### T
- **`/teamwork-preview`**: Chế độ điều phối đội ngũ đa tác nhân 2 giai đoạn với các vai trò kiểm định đối kháng (`Sentinel`, `Critic`, `Challenger`, `Auditor`) — [Module 09](09-advanced-features/README.md)

### W
- **`Workspace: "inherit" | "branch" | "share"`**: Ba chế độ cô lập không gian làm việc khi gọi `invoke_subagent` — [Module 04](04-subagents/README.md)
