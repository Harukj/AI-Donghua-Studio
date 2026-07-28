from abc import ABC, abstractmethod
from core.logger import studio_logger

class Plugin(ABC):
	def __init__(self, plugin_name: str):
		"""Khởi tạo cấu trúc nền móng DreamForge SDK v1.0 (Dùng chung API)"""
		self.name = plugin_name
		self.is_active = False

	@abstractmethod
	def initialize(self) -> bool:
		"""Phương thức ép buộc khởi tạo kết nối thông số kỹ thuật hoặc API mạng"""
		pass

	@abstractmethod
	def execute(self, payload: dict) -> dict:
		"""Phương thức ép buộc thực thi tác vụ xử lý lõi của Plugin"""
		pass

	def activate_plugin(self):
		"""Kích hoạt trạng thái sẵn sàng cắm rút của Module"""
		self.is_active = True
		studio_logger.logger.info(f"[SDK ENGINE] Plugin [{self.name.upper()}] đã được kích hoạt trên hệ thống.")
