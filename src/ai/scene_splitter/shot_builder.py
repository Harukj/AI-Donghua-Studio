from src.ai.scene_splitter.shot import Shot
from src.core.logger import studio_logger

class ShotBuilder:
	def __init__(self, scene_id: int, raw_scene_text: str):
		self.scene_id = scene_id
		self.raw_text = raw_scene_text.strip()

	def build_shots_from_scene(self, default_seed: str = "23561") -> list[Shot]:
		studio_logger.logger.info(f"Shot Builder: Đang bẻ phân cảnh ID [{self.scene_id}] theo phân lớp Studio...")

		# Sử dụng bộ Parser Sentence-level sạch lỗi đã sửa ở chặng trước
		raw_lines = self.text_split_cleaner(self.raw_text)
		shot_objects_list = []
		
		for idx, action_line in enumerate(raw_lines, start=1):
			shot_db_id = int(f"{self.scene_id}{idx:02d}")
			action_lower = action_line.lower()
			
			# 1. THUẬT TOÁN TỰ ĐỘNG PHÂN LỚP NGỮ CẢNH ĐIỆN ẢNH (STUDIO PIPELINE)
			context_preset = "action"
			camera_preset = "Medium Shot"
			lens_preset = "Standard 50mm"
			movement_preset = "Static"
			
			# Quy tắc 1: Nếu là cú máy đầu tiên của phân cảnh, tự động đặt làm cảnh toàn giới thiệu
			if idx == 1:
				context_preset = "establishing"
				camera_preset = "Wide Shot"
				movement_preset = "Slow Pan"
			# Quy tắc 2: Nếu câu văn tả biểu cảm phản ứng đơn lẻ của nhân vật phụ
			elif any(kw in action_lower for kw in ["nhìn cậu", "nhìn thấy", "ngoảnh lại"]):
				context_preset = "reaction"
				camera_preset = "Close-Up Shot"
				lens_preset = "Telephoto 85mm"
			# Quy tắc 3: Nếu câu văn tả sự tương tác qua lại hoặc chuẩn bị hội thoại
			elif any(kw in action_lower for kw in ["nhìn nhau", "nói", "gọi lớn"]):
				context_preset = "dialogue"
				camera_preset = "Over Shoulder Shot"

			# 2. KHỞI TẠO ĐỐI TƯỢNG SHOT ĐÃ PHÂN LỚP SẠCH
			shot_obj = Shot(
				id=shot_db_id,
				scene_id=self.scene_id,
				index=idx,
				context_type=context_preset, # Nạp nhãn ngữ cảnh chuẩn của ChatGPT
				camera=camera_preset,
				lens=lens_preset,
				movement=movement_preset,
				duration=3.5,
				lighting="Morning",
				seed=default_seed,
				prompt=f"3D Chinese Donghua style, {camera_preset.lower()}, {context_preset} shot, action: {action_lower}",
				video_path=f"projects/exports/cache/shot_{shot_db_id}.mp4"
			)
			shot_objects_list.append(shot_obj)
			
		return shot_objects_list

	def text_split_cleaner(self, text: str) -> list[str]:
		cleaned_text = text.replace("\n", ". ")
		return [s.strip() for s in cleaned_text.split(".") if s.strip() and len(s.strip()) > 1]
