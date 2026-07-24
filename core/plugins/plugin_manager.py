from core.plugins.base_plugin import BasePlugin
from core.logger import studio_logger

class PluginManager:
	def __init__(self):
		"""Khởi tạo kho chứa danh bạ đăng ký các Plugin hệ thống"""
		self._plugins: dict[str, BasePlugin] = {}

	def register_plugin(self, plugin: BasePlugin):
		"""Đăng ký một nền tảng công cụ AI mới vào dây chuyền phần mềm"""
		name = plugin.get_plugin_name()
		self._plugins[name] = plugin
		studio_logger.logger.info(f"[PLUGIN MANAGER] Đã tích hợp thành công Plugin: '{name}' vào hệ thống.")

	def unregister_plugin(self, plugin_name: str):
		"""Gỡ bỏ Plugin ra khỏi danh sách quản lý"""
		if plugin_name in self._plugins:
			del self._plugins[plugin_name]
			studio_logger.logger.info(f"[PLUGIN MANAGER] Đã gỡ bỏ Plugin: '{plugin_name}'")

	def execute_plugin(self, plugin_name: str, data: dict) -> dict:
		"""Kích hoạt chạy tác vụ xử lý độc lập của một Plugin cụ thể"""
		if plugin_name not in self._plugins:
			raise KeyError(f"Không tìm thấy Plugin mang định danh '{plugin_name}' trong hệ thống!")
			
		plugin = self._plugins[plugin_name]
		# Thực thi tác vụ xử lý khép kín của Plugin
		return plugin.execute(data)

	def get_all_registered_plugins(self) -> list[str]:
		"""Lấy danh sách toàn bộ các Plugin AI đang sẵn sàng hoạt động"""
		return list(self._plugins.keys())

# Khởi tạo một thực thể điều phối duy nhất dùng chung cho toàn bộ dự án Studio (Singleton Pattern)
plugin_registry = PluginManager()
