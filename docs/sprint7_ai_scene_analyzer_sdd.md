# SOFTWARE DESIGN DOCUMENT (SDD) - SPRINT 7: AI SCENE ANALYZER
**Bộ lõi đạo diễn AI bóc tách thực thể điện ảnh và phân rã kịch bản - AI Donghua Studio v1.0**

---

## 1. SPRINT
- **Mục tiêu**: Xây dựng module phân tích ngữ cảnh thông minh (AI Scene Analyzer), tích hợp API mô hình ngôn ngữ lớn (LLM) thực tế để tự động bẻ tách chương truyện chữ thô thành các phân cảnh kịch bản điện ảnh cấu trúc sạch.
- **Phạm vi**: Kết nối API bên ngoài, xử lý làm mịn Token đầu vào, tự động bóc tách thực thể (Characters, Environments, Props) và tự sinh chuỗi Prompt nghệ thuật gộp.

## 2. YÊU CẦU (REQUIREMENTS)
- **Zero Human Entry**: Người dùng chỉ cần nạp file `.docx` kịch bản văn học, cỗ máy AI bắt buộc phải tự động phân rã mạch truyện thành các phân cảnh hành động ngắn độc lập.
- **Entity Extraction (Trích xuất thực thể)**: Quét sâu đoạn văn để phân tích sắc thái cảm xúc, nhận diện chính xác danh tính nhân vật, địa điểm không gian bối cảnh và vũ khí sử dụng.
- **Tương thích ngược**: Kết quả trích xuất của AI phải tự động ép kiểu về dạng mô hình Class hoặc Dataclass để nạp đồng bộ xuống cơ sở dữ liệu.

## 3. DATABASE SCHEMA
Module này sẽ trực tiếp cập nhật và ghi nhận dữ liệu xuống bảng `scenes` đã chuẩn hóa ở các chặng trước:
- `generated_prompt` (Text): Lưu chuỗi Prompt nghệ thuật được lắp ghép tự động sau khi AI trích xuất thực thể.
- `camera` / `mood` / `characters` / `environments` (Text): Chứa bộ tham số điện ảnh sạch do AI chỉ định để chuẩn bị chuyển giao cho hàng đợi Render Queue.

## 4. CLASS DIAGRAM (OOP MAPPING)
- `AIAnalysisEngine`: Lớp điều phối trung tâm kết nối với các thư viện mạng API (`google-generativeai` hoặc `openai`).
- `PromptTemplateMixer`: Lớp bộ lọc đóng vai trò máy trộn cơ học, nhận thực thể sạch từ lớp AIAnalysisEngine để lắp ghép chuỗi token điện ảnh cố định theo template của Studio.

## 5. GUI LAYOUT
Tích hợp trực tiếp vào phân hệ **`Novel Workspace`** và **`Storyboard Workspace`**:
- Bổ sung thanh tiến trình trạng thái chạy ngầm: `[AI Đạo diễn đang phân tích ngữ cảnh... 45%]` khi hệ thống gửi gói tin qua mạng API để tránh làm đơ hoặc treo giao diện người dùng CustomTkinter.

## 6. API DATA FORMAT (JSON COMPLIANCE)
Hệ thống sử dụng kỹ thuật cấu trúc hóa Prompt hệ thống (System Prompt Function Calling) để ép API AI bắt buộc phải trả về gói dữ liệu sạch định dạng JSON với cấu trúc bắt buộc:
```json
{
    "scene_index": 1,
    "action_summary": "Tô Mộc ngước mắt nhìn lên bầu trời sao rực rỡ phía trên học viện.",
    "detected_entities": {
        "characters": ["Tô Mộc"],
        "environments": ["Học viện Long Dạng"],
        "props": []
    },
    "cinematic_directives": {
        "emotion": "Wonder",
        "camera_angle": "Over Shoulder, Low Angle Shot",
        "lighting": "Night Dynamic Starlight"
    }
}
```

## 7. CODE SPECIFICATION
- Toàn bộ luồng kết nối API mạng phải được bao bọc bên trong khối lệnh `try...except` chặt chẽ để bắt lỗi mất kết nối mạng hoặc hết hạn gói Key API (`APIKeyError`, `TimeoutError`).
- Căn chỉnh nấc lề đầu dòng nghiêm ngặt bằng **phím Tab** (Tab Size: 4).

## 8. TEST PLAN (UNIT TESTING)
- **Kịch bản 1**: Giả lập ngắt kết nối Internet mạng, xác nhận hệ thống tự động kích hoạt chế độ dự phòng (Fallback Mock Data) để bảo vệ phần mềm không bị crash sập ứng dụng.
- **Kịch bản 2**: Kiểm tra tính hợp lệ của chuỗi JSON trả về từ API, xác nhận các trường `characters` và `environments` được bóc tách đúng, không bị lẫn tạp từ văn học gốc.

## 9. RELEASE
- Đóng gói mã nguồn, cập nhật file cài đặt `requirements.txt` đầy đủ các package kết nối API.
- Gắn thẻ phiên bản Git: `git tag -a v1.1.0-sprint7 -m "Launch Phase 2: Completed AI Scene Analyzer SDD Specification"`.
