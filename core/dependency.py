import sys
from core.logger import logger

def check_dependencies():
	"""Kiểm tra tính sẵn sàng của các thư viện cốt lõi"""
	required_modules = ["customtkinter", "sqlalchemy", "docx", "PIL"]
	missing_modules = []
	
	for module in required_modules:
		try:
			__import__(module)
		except ImportError:
			missing_modules.append(module)
			
	if missing_modules:
		logger.error(f"Thiếu các thư viện phụ thuộc bắt buộc: {missing_modules}")
		logger.info("Vui lòng chạy lệnh: pip install -r requirements.txt")
		return False
		
	logger.info("Tất cả thư viện hệ thống (Dependencies) đã sẵn sàng 100%.")
	return True
