from ai.scene_splitter.shot import Shot
from core.logger import studio_logger

class ShotBuilder:
	def __init__(self, scene_id: int, raw_scene_text: str):
		"""Khởi tạo bộ bẻ cú máy ảo chuyên sâu cho phân cảnh"""
		self.scene_id = scene_id
		self.raw_text = raw_scene_text.strip()

	def build_shots_from_scene(self, default_seed: str = "23561") -> list[Shot]:
		"""
		[SHOT BUILDER CORE PIPELINE]
		Tự động đọc nội dung văn bản phân cảnh thô, tách lớp theo từng câu hành động ngắn
		để chuyển hóa trực tiếp thành danh sách các thực thể Shot Object điện ảnh.
		"""
		studio_logger.logger.info(f"Shot Builder: Đang phân rã Phân cảnh ID [{self.scene_id}] thành các cú máy (Shots)...")

		# Tách nhỏ văn bản phân cảnh dựa trên dấu ngắt dòng hoặc dấu chấm câu văn học
		raw_lines = [line.strip() for line in self.text_split_cleaner(self.raw_text) if line.strip()]
		
		shot_objects_list = []
		
		# Duyệt qua từng câu hành động ngắn để thiết lập thông số góc máy virtual camera tự động
		for idx, action_line in enumerate(raw_lines, start=1):
			shot_db_id = int(f"{self.scene_id}{idx:02d}") # Khởi tạo ID duy nhất cho shot quay
			
			# CẤU HÌNH THUẬT TOÁN ĐIỀU PHỐI GÓC MÁY TỰ ĐỘNG (CINEMATIC AUTOMATION)
			camera_preset = "Medium Shot"
			lens_preset = "Standard 50mm"
			movement_preset = "Static"
			lighting_preset = "Morning"
			
			action_lower = action_line.lower()
			
			# Tự động gán góc máy cận cảnh (Close-Up) nếu câu văn đặc tả biểu cảm ánh mắt nhân vật
			if any(kw in action_lower for kw in ["nhìn", "ánh mắt", "khuôn mặt", "mở mắt"]):
				camera_preset = "Close-Up Shot"
				lens_preset = "Telephoto 85mm"
			
			# Tự động gán chuyển động camera tiến vào nếu nhân vật di chuyển bước đi
			if any(kw in action_lower for kw in ["bước vào", "lao đến", "chạy"]):
				movement_preset = "Slow Zoom In"
				
			# Khởi tạo thực thể Class Shot Object sạch khớp 100% bộ khung thuộc tính của ChatGPT
			shot_obj = Shot(
				id=shot_db_id,
				scene_id=self.scene_id,
				index=idx,
				camera=camera_preset,
				lens=lens_preset,
				movement=movement_preset,
				duration=3.5, # Mặc định thời lượng mỗi cú máy AI dài 3.5 giây kịch tính
				lighting=lighting_preset,
				seed=default_seed, # Ghim mã hạt giống cố định để bảo vệ tính nhất quán nhân vật
				prompt=f"3D Chinese Donghua animation style, {camera_preset.lower()}, character action: {action_line.lower()}",
				video_path=f"projects/exports/cache/shot_{shot_db_id}.mp4"
			)
			
			shot_objects_list.append(shot_obj)
			
		studio_logger.logger.info(f" -> Tự động bẻ tách thành công {len(shot_objects_list)} cú máy cho Phân cảnh [{self.scene_id}].")
		return shot_objects_list

	def text_split_cleaner(self, text: str) -> list[str]:
		"""
		[FIXED SENTENCE-LEVEL TOKENIZER]
		Thuật toán bóc tách và ngắt dòng kịch bản chuẩn hóa theo câu văn học tiếng Việt.
		Loại bỏ triệt để lỗi bẻ vụn chữ cái đơn lẻ (Character-level splitting).
		"""
		import re
		# Bước 1: Thay thế các ký tự ngắt dòng \n phức tạp thành dấu chấm để chuẩn hóa cấu trúc
		cleaned_text = text.replace("\n", ". ")
		
		# Bước 2: Tách chuỗi dựa theo dấu chấm câu một cách an toàn
		raw_sentences = re.split(r'\.\s*', cleaned_text)
		
		# Bước 3: Lọc bỏ các khoảng trắng thừa và loại bỏ các chuỗi rỗng/dấu câu rác phát sinh
		final_sentences = [s.strip() for s in raw_sentences if s.strip() and len(s.strip()) > 1]
		
		return final_sentences
