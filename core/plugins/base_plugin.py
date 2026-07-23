from abc import ABC, abstractmethod

class BasePlugin(ABC):
	@abstractmethod
	def get_plugin_name(self) -> str:
		"""Trả về định danh tên của Plugin"""
		pass

	@abstractmethod
	def execute(self, data: dict) -> dict:
		"""Hàm lõi thực thi tác vụ xử lý của Plugin"""
		pass
