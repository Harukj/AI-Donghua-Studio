## [0.6.0-Sprint8] - 2026-07-24
### Added
- Khởi động **Version 0.6 - Production Engine** chuyên trách dây chuyền sản xuất phim hoạt hình dài tập.
- Thiết lập phân hệ cốt lõi **Sprint 8: Shot Manager** phục vụ bẻ nhỏ phân cảnh (Scene) thành các cú máy (Shots) điện ảnh độc lập.
- Khởi tạo bảng cơ sở dữ liệu `shots` và cấu hình mối quan hệ khóa ngoại (Foreign Key) nối sang bảng `scenes`.
- Phát triển lớp kho lưu trữ dữ liệu `ShotRepository` chuyên trách quản lý vòng đời cú máy render.
## [1.0.0-Sprint10] - 2026-07-24
### Added
- Kích hoạt phân hệ tối thượng **AI Director Engine v1.0** chuyên trách điều phối kịch bản vĩ mô.
- Phát triển bộ lõi điều phối `AIDirectorEngine` kết nối API Trí tuệ nhân tạo để tự động hóa khâu chỉ định thông số điện ảnh.
- Thiết lập tệp tin kiểm thử tích hợp toàn diện `tests/test_sprint10_ai_director.py` phục vụ nghiệm thu Milestone.
