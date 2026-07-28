import os
import json
from datetime import datetime

class ProjectManager:
	def __init__(self, base_dir="projects"):
		"""Khởi tạo thư mục gốc chứa tất cả các dự án (mặc định là thư mục 'projects')"""
		self.base_dir = base_dir
		if not os.path.exists(self.base_dir):
			os.makedirs(self.base_dir)

	def create_project(self, project_name: str, author: str = "Harukj") -> str:
		"""
		[AI DONGHUA STUDIO v1.0]
		Tự động tạo cấu trúc thư mục độc lập cô lập tài nguyên cho từng dự án phim.
		Đồng bộ chính xác 100% theo sơ đồ cây viết thường (lowercase) của ChatGPT.
		"""
		# Chuẩn hóa tên thư mục dự án viết liền cách nhau bằng dấu gạch dưới
		folder_name = project_name.replace(" ", "_")
		project_path = os.path.join(self.base_dir, folder_name)

		if os.path.exists(project_path):
			raise FileExistsError(f"Dự án '{project_name}' đã tồn tại sẵn trong hệ thống!")

		# 1. TẠO CÁC PHÂN KHU LOGIC SẢN XUẤT CẤP CAO (NOVEL, STORYBOARD, CACHE, EXPORTS)
		production_dirs = ["novel", "storyboard", "cache", "exports"]
		for p_dir in production_dirs:
			os.makedirs(os.path.join(project_path, p_dir))

		# 2. TẠO THƯ MỤC ASSETS GỐC VÀ CÁC PHÂN KHU TÀI NGUYÊN CON VIẾT THƯỜNG
		assets_base_path = os.path.join(project_path, "assets")
		os.makedirs(assets_base_path)

		lowercase_assets = [
			"characters",
			"environment",
			"props",
			"audio",
			"fx"
		]
		for a_dir in lowercase_assets:
			os.makedirs(os.path.join(assets_base_path, a_dir))

		# 3. KHỞI TẠO NỘI DUNG FILE CẤU HÌNH META-DATA (project.json)
		project_metadata = {
			"project_name": project_name,
			"folder_name": folder_name,
			"created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"author": author,
			"version": "1.0.0",
			"status": "In Production"
		}

		json_path = os.path.join(project_path, "project.json")
		with open(json_path, "w", encoding="utf-8") as f:
			json.dump(project_metadata, f, ensure_ascii=False, indent=4)

		print(f"Hệ thống Engine: Đã sinh hạ tầng dự án thương mại sạch tại: {project_path}")
		return project_path

	def get_production_path(self, project_name: str, module_name: str) -> str:
		"""Hàm tiện ích lấy nhanh đường dẫn của các phân khu: 'novel', 'storyboard', 'cache', 'exports'"""
		folder_name = project_name.replace(" ", "_")
		return os.path.join(self.base_dir, folder_name, module_name.lower())

	def get_asset_path(self, project_name: str, asset_type: str) -> str:
		"""Hàm tiện ích lấy nhanh đường dẫn của kho assets: 'characters', 'environment', 'props', 'audio', 'fx'"""
		folder_name = project_name.replace(" ", "_")
		return os.path.join(self.base_dir, folder_name, "assets", asset_type.lower())
