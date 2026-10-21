# GEMINI.md — Chỉ Dẫn Repository Cho Google Antigravity & Gemini

[English](../GEMINI.md) | **Tiếng Việt**

File này cung cấp ngữ cảnh không gian làm việc xuyên suốt và các quy ước biên soạn cho các tác nhân AI khi làm việc trong repository **gemini-howto**.

## Tổng Quan Dự Án

**gemini-howto** là bộ tài liệu hướng dẫn trực quan, thực chiến giúp làm chủ **Google Antigravity** (App v2.24+, CLI `agy` v1.4+, Python SDK `google-antigravity` v0.1.22+ và các tiện ích mở rộng IDE) được vận hành bởi các mô hình **Gemini** tiên phong (Gemini 4 Argon, Gemini 3.8 Flash, Gemini 3.1 Pro, Nano Banana 2).

Repository được tổ chức thành chương trình học 10 module tăng dần (`01-` đến `10-`), đi kèm các template mẫu có thể sao chép ngay vào dự án thực tế, bộ kỹ năng tự đánh giá tương tác (`.agents/skills/`) và phiên bản tiếng Việt hoàn chỉnh (`vi/`).

## Cấu Trúc Thư Mục Repository

```text
gemini-howto/
├── README.md                    # Trang chủ tiếng Anh, ma trận tính năng và hướng dẫn bắt đầu nhanh
├── GEMINI.md                    # Chỉ dẫn workspace cho Gemini / Antigravity
├── AGENTS.md                    # Chỉ dẫn theo chuẩn mở đa tác nhân (nhúng GEMINI.md)
├── LEARNING-ROADMAP.md          # Lộ trình học tập theo vai trò từ Cơ bản đến Kiến trúc sư
├── QUICK_REFERENCE.md           # Bảng tra cứu nhanh 1 trang cho mọi lệnh & cấu hình
├── CATALOG.md                   # Danh mục toàn bộ các template có sẵn
├── INDEX.md                     # Mục lục tra cứu theo chủ đề A-Z và tình huống thực tế
├── gemini_concepts_guide.md     # Cẩm nang kiến trúc chuyên sâu & mô hình tư duy
├── STYLE_GUIDE.md               # Tiêu chuẩn biên soạn tài liệu & sơ đồ Mermaid
├── clean-code-rules.md          # Bộ quy tắc kỹ thuật Clean Code mẫu
├── CHANGELOG.md                 # Lịch sử cập nhật giáo trình & phiên bản Antigravity
├── .agents/skills/              # Hai kỹ năng tương tác (/self-assessment, /lesson-quiz)
├── 01-slash-commands/           # Lệnh slash tích hợp sẵn & lệnh tùy chỉnh dựa trên skill
├── 02-memory/                   # GEMINI.md, AGENTS.md, .agents/rules/*.md & /learn
├── 03-skills/                   # Agent Skills (.agents/skills/<name>/SKILL.md)
├── 04-subagents/                # Subagents (.agents/agents/*.md, worktree branch/share)
├── 05-mcp/                      # Model Context Protocol (mcp_config.json, Stdio & HTTP)
├── 06-hooks/                    # Lifecycle Hooks (hooks.json, 6 sự kiện, hợp đồng JSON)
├── 07-plugins/                  # Native Antigravity Plugins (plugin.json, agy plugin CLI)
├── 08-checkpoints/              # Checkpoints, Artifacts, Generative UI & Sidecars
├── 09-advanced-features/        # /boost, /teamwork-preview, Permissions, Sandbox, Remote Control
├── 10-cli/                      # Antigravity CLI (agy) & Python SDK (google-antigravity)
└── vi/                          # Bản dịch tiếng Việt hoàn chỉnh của toàn bộ chương trình
```

## Các Quy Ước Kỹ Thuật Bắt Buộc

Khi bổ sung hoặc cập nhật bài hướng dẫn, template hoặc câu hỏi trắc nghiệm trong repository này, hãy tuân thủ nghiêm ngặt các đặc tả kỹ thuật chuẩn của Antigravity dưới đây:

1. **Đường Dẫn Tùy Biến (Customization Paths)**:
   - Tùy biến cấp workspace nằm trong `.agents/` (`.agents/rules/`, `.agents/skills/`, `.agents/agents/`, `.agents/plugins/`, `.agents/hooks.json`).
   - Tùy biến toàn cục của người dùng nằm trong `~/.gemini/config/` (`rules/`, `skills/`, `agents/`, `plugins/`, `sidecars/`, `mcp_config.json`, `hooks.json`) và `~/.gemini/antigravity-cli/settings.json`.
   - Tuyệt đối không sử dụng đường dẫn `.claude/` trong các ví dụ của Antigravity.

2. **Rules & Memory (`02-memory/`)**:
   - Các file `GEMINI.md` và `AGENTS.md` độc lập sử dụng Markdown thuần túy (không yêu cầu YAML frontmatter) và được nạp phân cấp từ thư mục gốc của workspace xuống các thư mục con.
   - Các file quy tắc mô-đun trong `.agents/rules/*.md` **bắt buộc** có YAML frontmatter khai báo `trigger: always_on | model_decision | glob | manual`.
   - Sử dụng cú pháp `@[nhãn](relative/path.md)` để nhúng trực tiếp nội dung file tham chiếu (tự động lược bỏ frontmatter) hoặc `@relative/path.md` cho tham chiếu con trỏ đường dẫn.
   - Tuân thủ giới hạn **24 KB** mỗi file và tổng ngân sách **20.000 token** (`defaultRulesBudget`).

3. **Skills & Lệnh Slash Tùy Chỉnh (`01-slash-commands/` & `03-skills/`)**:
   - Thư mục cũ `.agents/workflows/*.md` đã ngừng khuyến nghị (được chuyển đổi qua `/migrate-workflows`).
   - Mỗi skill trong `.agents/skills/<name>/SKILL.md` vừa được tự động khám phá theo ngữ nghĩa, vừa có thể gọi trực tiếp bằng lệnh `/<name>`.

4. **Hợp Đồng Hooks (`06-hooks/`)**:
   - Hooks được cấu hình tại `.agents/hooks.json`, `~/.gemini/config/hooks.json` hoặc `<plugin-root>/hooks.json`.
   - 6 sự kiện được hỗ trợ: `SessionStart`, `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`, `Stop`.
   - Luôn sử dụng các khóa JSON dạng **camelCase** (`conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`, `modelName`, `toolName`, `toolInput`, `injectSteps`, `permissionOverrides`, `fullyIdle`, `terminationReason`).

5. **Plugins (`07-plugins/`)**:
   - File manifest là `<plugin-root>/plugin.json`.
   - Hai file `hooks.json` và `mcp_config.json` phải nằm ngay tại **thư mục gốc của plugin**, không đặt bên trong thư mục con `hooks/`.

6. **Tiêu Chuẩn Tài Liệu & Sơ Đồ Mermaid**:
   - Tuân thủ `STYLE_GUIDE.md` về cấu trúc Markdown, cú pháp sơ đồ Mermaid (luôn đặt nhãn nút chứa dấu ngoặc đơn hoặc ký tự đặc biệt trong dấu ngoặc kép `"..."`) và thanh điều hướng cuối mỗi module.
   - Giữ bản tiếng Anh (`./`) và bản tiếng Việt (`./vi/`) đồng bộ khi cập nhật các khái niệm cốt lõi.
