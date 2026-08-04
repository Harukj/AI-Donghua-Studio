from src.core.logger import logger

class StudioException(Exception):
	"""Lớp ngoại lệ cơ sở cho toàn bộ ứng dụng AI Donghua Studio"""
	def __init__(self, message):
		super().__init__(message)
		logger.error(f"Hệ thống phát hiện lỗi: {message}")

class ProjectNotFoundError(StudioException):
	"""Lỗi xuất hiện khi truy cập vào một dự án không tồn tại"""
	pass

class PipelineExecutionError(StudioException):
	"""Lỗi xuất hiện khi luồng phân tích kịch bản Pipeline 9 bước gặp sự cố"""
	pass
