import re

def slugify_string(text: str) -> str:
	"""Chuyển đổi chuỗi chữ có dấu thành chuỗi không dấu phục vụ tạo tên thư mục dự án"""
	text = text.strip().lower()
	# Thay thế các ký tự tiếng Việt phổ biến
	text = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', text)
	text = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', text)
	text = re.sub(r'[ìíịỉĩ]', 'i', text)
	text = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', text)
	text = re.sub(r'[ùúụủũưừứựửữ]', 'u', text)
	text = re.sub(r'[ỳýỵỷỹ]', 'y', text)
	text = re.sub(r'[đ]', 'd', text)
	# Thay khoảng trắng thành dấu gạch dưới
	text = re.sub(r'\s+', '_', text)
	return text
