import re

class ScriptParser:
	@staticmethod
	def clean_and_normalize(text: str) -> list[str]:
		"""Chuẩn hóa dấu câu và bóc tách văn bản thô theo từng dòng sạch"""
		# Thay thế các dạng dấu ngoặc kép thông minh thành dấu ngoặc tiêu chuẩn
		normalized_text = text.replace("“", '"').replace("”", '"')
		lines = [line.strip() for line in normalized_text.split("\n") if line.strip()]
		return lines
