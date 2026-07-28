class AIDirector:
	def __init__(self, raw_action_text: str):
		"""Khởi tạo với chuỗi văn bản mô tả hành động thô của phân cảnh"""
		self.text = raw_action_text.strip()
		self.text_lower = self.text.lower()

	def make_cinematic_decisions(self) -> dict:
		"""
		[AI DIRECTOR CORE LOGIC]
		Tự động phân tích ngữ cảnh của kịch bản chữ thô để đưa ra các quyết định điện ảnh độc quyền.
		Ánh xạ chính xác 100% theo mô hình 4 lớp thông số của ChatGPT trong ảnh.
		"""
		# 1. KHỞI TẠO CÁC GIÁ TRỊ CẤU HÌNH MẶC ĐỊNH (DEFAULT VALUES)
		decision = {
			"emotion": "Neutral",
			"camera": "Medium Shot",
			"lens": "Standard 50mm",
			"lighting": "Cinematic Three-Point"
		}

		# 2. XỬ LÝ LỚP 1: EMOTION (Tự động nhận diện sắc thái cảm xúc hành động)
		if any(kw in self.text_lower for kw in ["nhìn lên", "bầu trời", "vô tận", "ngước mắt"]):
			decision["emotion"] = "Wonder" # Ngỡ ngàng, kinh ngạc trước không gian lớn theo ảnh mẫu
		elif any(kw in self.text_lower for kw in ["gầm lên", "quát", "giết", "tức giận"]):
			decision["emotion"] = "Anger"
		elif any(kw in self.text_lower for kw in ["khóc", "rơi lệ", "đau thương", "u ám"]):
			decision["emotion"] = "Sadness"

		# 3. XỬ LÝ LỚP 2: CAMERA (Tự động tính toán góc máy và khung hình điện ảnh)
		if "nhìn lên bầu trời" in self.text_lower:
			decision["camera"] = "Over Shoulder, Low Angle Shot" # Quay qua vai kết hợp góc hất thấp chuẩn ảnh mẫu
		elif any(kw in self.text_lower for kw in ["toàn cảnh", "thành phố", "xa xa"]):
			decision["camera"] = "Wide Establishing Shot"
		elif any(kw in self.text_lower for kw in ["khuôn mặt", "biểu cảm", "ánh mắt"]):
			decision["camera"] = "Close-Up Shot"

		# 4. XỬ LÝ LỚP 3: LENS (Tự động chọn loại ống kính ảo cho camera AI)
		if "wide" in decision["camera"].lower() or "establishing" in decision["camera"].lower() or "low angle" in decision["camera"].lower():
			decision["lens"] = "Wide-Angle Lens (24mm)" # Ống kính góc rộng để bao quát cảnh lớn chuẩn ảnh mẫu
		elif "close-up" in decision["camera"].lower():
			decision["lens"] = "Telephoto Lens (85mm)"

		# 5. XỬ LÝ LỚP 4: LIGHTING (Tự động phối ánh sáng nghệ thuật theo thời gian và tâm trạng)
		if "bầu trời" in self.text_lower:
			decision["lighting"] = "Sunset / Golden Hour" # Ánh chiều tà rực rỡ chuẩn ảnh mẫu của bạn
		elif "đêm" in self.text_lower or "tối" in self.text_lower:
			decision["lighting"] = "Volumetric Neon Moon Light"
		elif decision["emotion"] == "Anger":
			decision["lighting"] = "High-Contrast Dramatic Chiaroscuro"

		return decision
