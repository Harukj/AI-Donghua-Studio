# CHANGELOG - AI DONGHUA STUDIO

Tất cả các thay đổi và tiến độ nâng cấp kiến trúc của dự án sẽ được ghi nhận chi tiết tại đây.

---

## [1.0.0-Sprint7] - 2026-07-24
### Added
- Khởi động **Phase 2: Giai đoạn AI thật sự** kết hợp kiểm soát cấu trúc chặt chẽ.
- Tích hợp lớp đối tượng cấu trúc điện ảnh nâng cao sử dụng `Dataclass` (`SceneObject`).
- Phát triển hệ thống quản lý mẫu câu lệnh tập trung `TemplateManager` hỗ trợ nạp cấu hình `.json` độc lập.
- Nâng cấp `StaticPromptBuilder` tự động điều phối từ khóa và lắp ghép chuỗi token theo ngữ cảnh kịch bản (`ltx_dialogue`, `ltx_action`, `ltx_cinematic`).
- Khởi tạo hạ tầng cây thư mục hệ thống mở rộng linh hoạt `plugins/` (`ltx`, `elevenlabs`, `capcut`, `comfyui`, `youtube`).
- Bổ sung tài liệu đặc tả kỹ thuật thiết kế phần mềm `docs/sprint7_ai_scene_analyzer_sdd.md`.

### Fixed
- Vá dứt điểm lỗi import đường dẫn lớp lưu trữ cơ sở và dọn dẹp các khối lệnh trùng lặp trong luồng Pipeline.
- Chuẩn hóa toàn bộ cây thư mục lưu tệp vật lý của Project về định dạng chữ viết thường (`lowercase`) để triệt tiêu lỗi nhận diện đường dẫn trên các hệ điều hành khác nhau.
