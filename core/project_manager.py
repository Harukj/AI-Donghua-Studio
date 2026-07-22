import os
import json
from datetime import datetime

class ProjectManager:
    def __init__(self, base_dir="projects"):
        """
        Khởi tạo thư mục gốc chứa tất cả các dự án (mặc định là thư mục 'projects')
        """
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def create_project(self, project_name: str, author: str = "Harukj") -> str:
        """
        Tự động tạo cấu trúc thư mục và file cấu hình cho một dự án mới.
        """
        # 1. Chuẩn hóa tên thư mục (Xóa khoảng trắng thừa, thay khoảng trắng bằng dấu gạch dưới hoặc giữ nguyên)
        # Ví dụ: "Toan Dan Tao Phong" -> "Toan_Dan_Tao_Phong" hoặc giữ nguyên tùy bạn chọn
        folder_name = project_name.replace(" ", "_")
        project_path = os.path.join(self.base_dir, folder_name)

        if os.path.exists(project_path):
            raise FileExistsError(f"Dự án '{project_name}' đã tồn tại!")

        # 2. Danh sách các thư mục con cần tự động sinh ra theo sơ đồ
        sub_folders = [
            "characters",
            "environment",
            "storyboard",
            "episodes",
            "audio",
            "video",
            "exports",
            "cache"
        ]

        # 3. Tiến hành tạo các thư mục
        os.makedirs(project_path)
        for folder in sub_folders:
            os.makedirs(os.path.join(project_path, folder))

        # 4. Khởi tạo nội dung mặc định cho file project.json
        project_metadata = {
            "project_name": project_name,
            "folder_name": folder_name,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "author": author,
            "version": "1.0.0",
            "status": "In Progress",
            "settings": {
                "resolution": "1920x1080",
                "fps": 24
            }
        }

        # 5. Ghi dữ liệu vào file project.json
        json_path = os.path.join(project_path, "project.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(project_metadata, f, ensure_ascii=False, indent=4)

        print(f" Đã khởi tạo thành công cấu trúc dự án tại: {project_path}")
        return project_path
