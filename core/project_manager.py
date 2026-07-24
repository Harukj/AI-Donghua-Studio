import os
import json
from datetime import datetime

class ProjectManager:
	def __init__(self, base_dir="projects"):
		"""Khởi tạo thư mục gốc chứa toàn bộ các dự án phim hoạt hình"""
		self.base_dir = base_dir
		if not os.path.exists(self.base_dir):
			os.makedirs(self.base_dir)

	def create_project(self, project_name: str, author: str = "Harukj") -> str:
		"""
		[AI DONGHUA STUDIO v0.5 - CORE ENGINE]
		Tự động khởi tạo cấu trúc cây thư mục độc lập cô lập tài nguyên.
		Khớp chính xác 100% theo sơ đồ khối cấu trúc mới của ChatGPT.
		"""
		# Chuẩn hóa tên thư mục viết liền không dấu gạch ngang/khoảng trắng
		folder_name = project_name.replace(" ", "_")
		project_path = os.path.join(self.base_dir, folder_name)

		if os.path.exists(project_path):
			raise FileExistsError(f"Dự án phim '{project_name}' đã tồn tại sẵn trong Engine!")

		# 1. TẠO PHÂN TẦNG 1: THƯ MỤC NOVEL (Chứa tệp truyện chữ kịch bản gốc)
		os.makedirs(os.path.join(project_path, "Novel"))

		# 2. TẠO PHÂN TẦNG 2: THƯ MỤC ASSETS GỐC & CÁC THƯ MỤC CON BIỆT LẬP
		assets_base_path = os.path.join(project_path, "Assets")
		os.makedirs(assets_base_path)

		engine_assets_dirs = [
			"Characters",
			"Environments",
			"Props",
			"Audio"
		]

		for sub_folder in engine_assets_dirs:
			os.makedirs(os.path.join(assets_base_path, sub_folder))

		# 3. KHỞI TẠO FILE ĐỊNH DANH CẤU HÌNH META-DATA (project.json)
		project_metadata = {
			"project_name": project_name,
			"folder_name": folder_name,
			"created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"author": author,
			"engine_version": "v0.5",
			"pipeline_status": "Ready"
		}

		json_config_path = os.path.join(project_path, "project.json")
		with open(json_config_path, "w", encoding="utf-8") as f:
			json.dump(project_metadata, f, ensure_ascii=False, indent=4)

		print(f"[ENGINE SUCCESS] Đã sinh hạ tầng cô lập dự án tại: {project_path}")
		return project_path

	def get_asset_path(self, project_name: str, asset_category: str) -> str:
		"""Hàm tiện ích giúp các module khác lấy nhanh đường dẫn thư mục lưu file cứng"""
		folder_name = project_name.replace(" ", "_")
		# asset_category nhận các giá trị: 'Characters', 'Environments', 'Props', 'Audio', 'Novel'
		if asset_category == "Novel":
			return os.path.join(self.base_dir, folder_name, "Novel")
		return os.path.join(self.base_dir, folder_name, "Assets", asset_category)
