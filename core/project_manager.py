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
		Tự động tạo cấu trúc thư mục độc lập và các asset con chuẩn AI Donghua Studio.
		"""
		folder_name = project_name.replace(" ", "_")
		project_path = os.path.join(self.base_dir, folder_name)

		if os.path.exists(project_path):
			raise FileExistsError(f"Dự án '{project_name}' đã tồn tại!")

		# --- CẬP NHẬT CẤU TRÚC ASSET THƯƠNG MẠI CHUẨN THEO ẢNH ---
		# Tạo thư mục assets gốc trước
		assets_path = os.path.join(project_path, "assets")
		os.makedirs(assets_path)

		# Danh sách các thư mục tài nguyên con nằm bên trong thư mục assets/
		commercial_assets = [
			"characters",
			"environments",
			"props",
			"fx",
			"music",
			"sounds"
		]

		# Tự động quét và sinh hàng loạt các thư mục asset con
		for folder in commercial_assets:
			os.makedirs(os.path.join(assets_path, folder))
		# --------------------------------------------------------

		# Khởi tạo nội dung file cấu hình meta-data dự án
		project_metadata = {
			"project_name": project_name,
			"folder_name": folder_name,
			"created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"author": author,
			"version": "1.0.0",
			"status": "In Progress"
		}

		json_path = os.path.join(project_path, "project.json")
		with open(json_path, "w", encoding="utf-8") as f:
			json.dump(project_metadata, f, ensure_ascii=False, indent=4)

		print(f"Hệ thống: Đã khởi tạo cấu trúc Asset thương mại tại: {project_path}")
		return project_path
	
	def save_environment_image(self, current_project_name: str, source_image_path: str) -> str:
		"""
		Tự động sao chép file ảnh bối cảnh từ máy tính vào đúng thư mục assets/environments/ của dự án
		"""
		import shutil
		folder_name = current_project_name.replace(" ", "_")
		env_assets_dir = os.path.join(self.base_dir, folder_name, "assets", "environments")
		
		if not os.path.exists(env_assets_dir):
			os.makedirs(env_assets_dir)
			
		image_name = os.path.basename(source_image_path)
		destination_path = os.path.join(env_assets_dir, image_name)
		
		shutil.copy2(source_image_path, destination_path)
		return destination_path

