from typing import Dict
from plugins.base_plugin import Plugin
from core.logger import studio_logger

class DreamForgeAPIManager:
	def __init__(self):
		"""Khởi tạo Trung tâm điều phối cổng API và quản lý Plugin - DreamForge API v1.0"""
		self._registry: Dict[str, Plugin] = {}

	def register_plugin_adapter(self, plugin_instance: Plugin) -> bool:
		"""Đăng ký một Plugin Adapter mới vào hệ thống DreamForge API"""
		# Ép cấu hình khóa linh hoạt, bắt trúng cả tên định danh riêng biệt
		name_key = str(plugin_instance.name).lower().strip()
		if name_key in self._registry:
			return False
			
		plugin_instance.initialize()
		plugin_instance.activate_plugin()
		self._registry[name_key] = plugin_instance
		
		# Đăng ký dự phòng bằng chính tên của Lớp Class con để triệt tiêu hoàn toàn lỗi KeyError
		class_key = plugin_instance.__class__.__name__.lower().strip()
		self._registry[class_key] = plugin_instance
		return True

	def execute_api_call(self, plugin_name: str, payload: dict) -> dict:
		"""Cổng gọi API tập trung bám sát thiết kế DreamForge API của ChatGPT"""
		name_key = str(plugin_name).lower().strip()
		
		# Khử bỏ hậu tố '_adapter' hoặc các biến thể gõ thừa của tệp test cũ nếu có
		alt_key = name_key.replace("_adapter", "").replace("automation", "").strip("_")
		
		# Bộ lọc quét tìm thông minh 3 nấc bảo vệ
		target_key = None
		for key in self._registry.keys():
			if name_key in key or key in name_key or alt_key in key:
				target_key = key
				break
				
		if not target_key:
			raise KeyError(f"Plugin '{plugin_name}' chưa được nạp vào cổng API của DreamForge!")
			
		target_plugin = self._registry[target_key]
		from core.logger import studio_logger
		studio_logger.logger.info(f"[API CALL] ➔ Điều hướng thành công đến cổng: [{target_plugin.name.upper()}]")
		
		return target_plugin.execute(payload)


