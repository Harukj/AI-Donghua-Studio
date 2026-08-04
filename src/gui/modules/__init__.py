# Khai báo đóng gói danh mục module giao diện v1.0 chuẩn DreamForge
from src.core.logger import studio_logger

studio_logger.logger.info("[GUI CORE] Đang khởi động hệ thống phân lớp mô-đun giao diện người dùng...")

# Khai báo các điểm xuất bản (Export entry points) để app.py gọi nạp ngầm thuận tiện
__all__ = ["project", "episode", "storyboard", "assets", "prompt", "render", "timeline", "export"]
