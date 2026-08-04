import os
import json
from src.core.logger import studio_logger

class TemplateManager:
	def __init__(self):
		"""Khởi tạo trình quản lý danh mục mẫu câu lệnh Template Manager"""
		self.base_dir = os.path.dirname(os.path.abspath(__file__))
		self.templates_dir = os.path.join(self.base_dir, "templates")
		
		if not os.path.exists(self.templates_dir):
			os.makedirs(self.templates_dir)

	def get_available_templates(self) -> list[str]:
		"""Quét thư mục hệ thống để trả về danh sách các file template đang sẵn có"""
		try:
			files = os.listdir(self.templates_dir)
			# Chỉ lấy các tệp cấu hình dạng .json
			return [f.replace(".json", "") for f in files if f.endswith(".json")]
		except Exception as e:
			studio_logger.logger.error(f"TemplateManager: Lỗi quét thư mục mẫu: {e}")
			return ["ltx_default"]

	def load_template_config(self, template_name: str) -> dict:
		"""Đọc nội dung tệp tin JSON cấu hình nghệ thuật cụ thể"""
		file_path = os.path.join(self.templates_dir, f"{template_name}.json")
		
		# Luồng dự phòng nếu file bị xóa hoặc không tìm thấy
		if not os.path.exists(file_path):
			studio_logger.logger.warning(f"TemplateManager: Không tìm thấy mẫu '{template_name}'. Tự động dùng mẫu mặc định.")
			file_path = os.path.join(self.templates_dir, "ltx_default.json")
			
		try:
			with open(file_path, "r", encoding="utf-8") as f:
				return json.load(f)
		except Exception as e:
			studio_logger.logger.error(f"TemplateManager: Lỗi đọc file cấu hình: {e}")
			return {}
