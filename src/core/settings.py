import os

# Đường dẫn gốc của toàn bộ dự án phần mềm
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Định vị thư mục lưu trữ các bộ phim hoạt hình
PROJECTS_DIR = os.path.join(BASE_DIR, "projects")

# Các thông số cấu hình mặc định cho mô hình AI
DEFAULT_DURATION = 5.0
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_STYLE = "Chinese Donghua 3D animation style"
