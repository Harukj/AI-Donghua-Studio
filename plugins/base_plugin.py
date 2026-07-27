from abc import ABC, abstractmethod
from core.logger import studio_logger

class BasePlugin(ABC):
	def __init__(self, plugin_name: str, version: str = "1.0.0"):
		"""Khởi tạo cấu trúc nền móng của hệ thống Plugin mở rộng DreamForge Engine"""
		self.plugin_name = plugin_name.lower()
		self.version = version
		self.is_activated = False

	@abstractmethod
	def initialize_api_connection(self) -> bool:
		"""Hàm bắt buộc các Plugin con phải tự hiện thực luồng xác thực API Key mạng ngầm"""
		pass

	@abstractmethod
	def execute_ai_task(self, input_data: dict) -> dict:
		"""Hàm bắt buộc các Plugin con phải tự hiện thực lõi xử lý tác vụ AI (Sinh ảnh, Giọng nói, Phụ đề)"""
		pass

	def activate_plugin(self):
		"""Kích hoạt trạng thái sẵn sàng chiến đấu của Plugin trong hệ thống"""
		self.is_activated = True
		studio_logger.logger.info(f"[PLUGIN SYSTEM] Plugin '[{self.plugin_name}] v{self.version}' đã được kích hoạt thành công vào Engine!")

	def deactivate_plugin(self):
		"""Hủy kích hoạt Plugin khi hệ thống ngắt kết nối"""
		self.is_activated = False
		studio_logger.logger.info(f"[PLUGIN SYSTEM] Plugin '[{self.plugin_name}]' đã được tạm ngắt kết nối an toàn.")
