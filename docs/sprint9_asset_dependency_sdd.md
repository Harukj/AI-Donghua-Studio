# SOFTWARE DESIGN DOCUMENT (SDD) - SPRINT 9: ASSET DEPENDENCY SYSTEM
**Hệ thống quản lý phụ thuộc tài nguyên tự động - DreamForge Engine v1.0**

---

## 1. SPRINT & YÊU CẦU
- **Mục tiêu**: Xây dựng cơ chế tự động truy vết và liên kết chéo các tài nguyên phụ thuộc (Character → Asset, Voice, Props) dựa theo tư duy cấu trúc của Unreal Engine.
- **Yêu cầu nghiệp vụ**: Khi Prompt Builder hoặc LTX Queue gọi một thực thể nhân vật, hệ thống bắt buộc phải tự động nạp kèm hồ sơ mã Seed, giọng đọc AI và vũ khí tương ứng đã đóng băng trong Database để bảo vệ tính nhất quán tuyệt đối.

## 2. DATABASE RELATIONSHIP
Bổ sung cơ chế liên kết khóa ngoại (Foreign Keys) chặt chẽ giữa bảng `characters` và các bảng tài nguyên Assets trung tâm:
- `asset_id` (Integer) -> Liên kết bảng `assets` (Lưu trữ ảnh chân dung gốc).
- `voice_id` (Integer) -> Liên kết bảng `audios` (Lưu trữ tệp giọng đọc AI).
- `prop_id` (Integer) -> Liên kết bảng `props` (Lưu trữ thần binh, pháp bảo).

## 3. OOP MAPPING (CLASS DESIGN)
- `AssetDependencyResolver`: Bộ điều phối trung tâm chịu trách nhiệm quét cơ sở dữ liệu và đóng gói cây phụ thuộc (Dependency Tree) của thực thể dưới dạng một Dictionary sạch để cấp dữ liệu trực tiếp cho Prompt Builder 2.0.