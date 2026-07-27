import os
import json
from core.logger import studio_logger

class AIDirectorEngine:
	def __init__(self, provider: str = "gemini"):
		"""Khởi tạo cỗ máy Tổng đạo diễn AI - AI Director Engine v0.8"""
		self.provider = provider.lower()
		self.api_key = os.getenv("AI_STUDIO_API_KEY", "MOCK_KEY_FOR_TESTING")

	def direct_scene_script(self, raw_novel_text: str, scene_index: int = 1) -> dict:
		"""
		[AI DIRECTOR PIPELINE v0.8]
		Đọc văn bản văn học thô -> Tự động đưa ra 5 quyết định điện ảnh:
		Góc máy, Ống kính, Ánh sáng, Âm nhạc (Nhạc), Chuyển cảnh.
		"""
		studio_logger.logger.info(f"[AI DIRECTOR] Đang bóc tách chỉ đạo nghệ thuật cho Phân cảnh {scene_index:03d}...")

		# --- LUỒNG DỰ PHÒNG CHẠY OFFLINE (FALLBACK MOCK DATA CHUẨN KIẾN TRÚC CHATGPT) ---
		if self.api_key == "MOCK_KEY_FOR_TESTING":
			return {
				"scene_metadata": {
					"id": scene_index,
					"raw_text": raw_novel_text
				},
				"cinematic_directives": {
					"camera_preset": "Establishing Shot", # Nên quay từ đâu?
					"lens": "24mm Wide-Angle",          # Ống kính gì?
					"lighting": "Volumetric Morning",    # Ánh sáng?
					"music_mood": "Epic Orchestral",     # Nhạc?
					"transition": "Fade In"              # Chuyển cảnh?
				}
			}

		# --- LUỒNG KẾT NỐI API LLM THỰC TẾ TRÊN MẠNG ---
		system_instruction = (
			"You are an expert 3D Donghua Movie Director. Analyze the input novel text and generate "
			"cinematic directives. You MUST return a valid JSON object matching this schema exactly: "
			"{'scene_metadata': {'id': int, 'raw_text': string}, "
			"'cinematic_directives': {'camera_preset': string, 'lens': string, 'lighting': string, 'music_mood': string, 'transition': string}}"
		)

		try:
			if self.provider == "gemini":
				import google.generativeai as genai
				genai.configure(api_key=self.api_key)
				model = genai.GenerativeModel('gemini-pro')
				response = model.generate_content(f"{system_instruction}\n\nNovel Text:\n{raw_novel_text}")
				return json.loads(response.text)
		except Exception as e:
			studio_logger.logger.error(f"AI Director lỗi kết nối API: {e}. Kích hoạt luồng dự phòng.")
			return {
				"scene_metadata": {"id": scene_index, "raw_text": raw_novel_text},
				"cinematic_directives": {"camera_preset": "Wide", "lens": "35mm", "lighting": "Standard", "music_mood": "None", "transition": "Cut"}
			}
