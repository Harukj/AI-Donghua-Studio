from core.logger import studio_logger

class AssetDetector:
	def __init__(self, scene_content: str):
		"""Khởi tạo bộ quét thực thể tài nguyên phụ trợ cho phân cảnh"""
		self.text = scene_content.strip().lower()

	def detect_props_and_costumes(self) -> dict:
		"""
		[ASSET DETECTOR CORE LOGIC]
		Tự động quét văn bản phân cảnh để trích xuất vũ khí (Props) và phục trang (Costumes).
		"""
		studio_logger.logger.info("Asset Detector: Đang quét văn bản phân cảnh để trích xuất vật phẩm phụ trợ...")
		
		detected_assets = {
			"props": [],
			"costumes": []
		}

		# Thuật toán quét và bóc tách từ khóa vũ khí/pháp bảo thương mại
		if any(kw in self.text for kw in ["kiếm", "đao", "thần binh"]):
			detected_assets["props"].append("Thần kiếm")
		if any(kw in self.text for kw in ["pháp bảo", "gương", "bảo vật"]):
			detected_assets["props"].append("Pháp bảo")

		# Thuật toán quét và bóc tách từ khóa trang phục nhân vật hoạt hình
		if any(kw in self.text for kw in ["đồng phục", "học viện", "áo khoác"]):
			detected_assets["costumes"].append("Academy Uniform")
		if any(kw in self.text for kw in ["giáp trụ", "chiến giáp", "áo giáp"]):
			detected_assets["costumes"].append("Battle Armor")

		return detected_assets
