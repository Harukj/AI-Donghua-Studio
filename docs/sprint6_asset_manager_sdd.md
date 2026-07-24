# SOFTWARE DESIGN DOCUMENT (SDD) - SPRINT 6: ASSET MANAGER
**Hệ thống quản lý tài nguyên tập trung và phân lớp sâu - AI Donghua Studio v1.0**

---

## 1. SPRINT
- **Mục tiêu**: Xây dựng module quản lý, phân loại, đồng bộ hóa và ghim phiên bản tài nguyên (Asset & Version Manager) tập trung cho toàn bộ dự án hoạt hình 3D Donghua.
- **Phạm vi**: Cô lập tài nguyên vật lý theo từng Project, kiểm soát vòng đời tệp tin, triệt tiêu sự ngẫu nhiên khi sinh câu lệnh Prompt.

## 2. YÊU CẦU (REQUIREMENTS)
- **Hệ thống tệp tin độc lập**: Khi tạo Project, tự động sinh 5 thư mục con viết thường (`characters`, `environment`, `props`, `audio`, `fx`) bên trong thư mục `assets`.
- **Bình thường hóa dữ liệu**: Mọi tệp tin vật lý phải được đăng ký tập trung vào một bảng duy nhất để tránh trùng lặp.
- **Ghim phiên bản (Version Locking)**: Cho phép một Asset sở hữu nhiều phiên bản (v1.0, v2.0). Khi ghim phiên bản nào, Prompt Engine bắt buộc phải dùng đúng mã Seed và Prompt của phiên bản đó để sinh video, đảm bảo tính nhất quán (Consistency).

## 3. DATABASE SCHEMA
Hệ thống sử dụng cơ sở dữ liệu SQLite/SQLAlchemy với bảng trung tâm `assets` và bảng lịch sử tiến hóa `asset_versions`:

### Bảng `assets`
- `id` (Integer, Primary Key, Autoincrement)
- `project_id` (String, Not Null) - Định danh dự án để cô lập tài nguyên.
- `type` (String, Not Null) - Phân loại: 'characters', 'environment', 'props', 'audio', 'fx'.
- `name` (String, Not Null) - Tên tệp tin (Ví dụ: tomoc.png).
- `path` (String, Not Null) - Đường dẫn vật lý đến file cứng trong thư mục dự án.
- `created_at` (DateTime, Default: UTC Now)

### Bảng `asset_versions`
- `id` (Integer, Primary Key, Autoincrement)
- `asset_id` (Integer, Foreign Key) - Trỏ về bảng `assets`.
- `version_number` (String, Not Null) - Số hiệu (v1.0, v2.0).
- `prompt_tags` (Text, Not Null) - Câu lệnh prompt cố định của phiên bản.
- `seed` (String) - Mã hạt giống không gian đóng băng.
- `created_at` (DateTime)

## 4. CLASS DIAGRAM (OOP MAPPING)
- `AssetModel`: Lớp ánh xạ cấu trúc bảng `assets`.
- `AssetVersionModel`: Lớp ánh xạ cấu trúc bảng `asset_versions`.
- `AssetRepository(BaseRepository[AssetModel])`: Lớp chuyên trách thực thi các câu lệnh truy vấn SQL nâng cao (lọc theo loại tài nguyên, kiểm tra tệp tin trùng lặp).
- `AssetVersionRepository`: Lớp chuyên trách truy vấn lịch sử hoặc ghim phiên bản render.

## 5. GUI LAYOUT
Giao diện phân hệ quản lý tài nguyên tập trung được bóc tách lớp thành 3 phân khu chính:
- **Left Panel (Folder Tree)**: Cây thư mục lề trái hiển thị dạng cuộn chứa 5 thư mục con viết thường.
- **Center Panel (Content Browser)**: Lưới hiển thị danh sách các icon file tài nguyên có trong thư mục đang chọn (Giống Unity/Unreal Engine).
- **Right Panel (Asset Inspector)**: Biểu mẫu hiển thị chi tiết thuộc tính của file đang chọn, tích hợp menu thả xuống `Version Manager` để ghim phiên bản.

## 6. API DATA FORMAT (JSON/DICT)
Khi người dùng nhấp đúp chuột chọn một tệp tài nguyên, module `Content Browser` sẽ phát tín hiệu truyền đi một gói cấu trúc dữ liệu sạch dạng Dictionary sang cho `Asset Inspector` nạp hiển thị:
```json
{
    "asset_name": "Tô Mộc",
    "folder_type": "characters",
    "portrait_path": "projects/ToanDanTaoPhong/assets/characters/tomoc.png",
    "prompt": "Masterpiece, Chinese Donghua style, character Tô Mộc, 3D render",
    "seed": "23561",
    "active_version": "v1.0 - Academy Uniform"
}
```

## 7. CODE SPECIFICATION
- Mã nguồn viết bằng ngôn ngữ Python, sử dụng thư viện CustomTkinter cho giao diện UI và SQLAlchemy cho tầng dữ liệu.
- Căn chỉnh nấc lề đầu dòng nghiêm ngặt bằng **phím Tab** (Tab Size: 4), không trộn lẫn khoảng trắng.
- Tách biệt hoàn toàn phần giao diện (GUI) khỏi tầng logic dữ liệu (Repositories) theo mô hình MVC phân lớp sạch.

## 8. TEST PLAN (INTEGRATION TEST)
- **Kịch bản 1**: Khởi chạy `ProjectManager`, xác nhận hệ thống tự động sinh đúng 5 thư mục con viết thường của kho assets.
- **Kịch bản 2**: Nạp một tệp ảnh chân dung nhân vật, xác nhận file vật lý được nhân bản vào đúng thư mục dự án và bản ghi metadata được lưu thành công vào bảng `assets`.
- **Kịch bản 3**: Thử nghiệm chuyển đổi phiên bản trên `Version Manager`, xác nhận hệ thống trích xuất đúng mã Seed đóng băng tương ứng.

## 9. RELEASE
- Đóng gói mã nguồn sạch lỗi, dọn dẹp các khối lệnh trùng lặp.
- Thực hiện commit và gắn thẻ phiên bản trên Git Terminal:
  ```bash
  git tag -a v1.0.0-sprint6 -m "Release Sprint 6: Completed Asset Manager with full SDD compliance"
  ```
