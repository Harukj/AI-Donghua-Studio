import os
import json
from core.logger import studio_logger

class AIDirectorEngine:
	def __init__(self, provider: str = "gemini"):
		"""Khởi tạo cỗ máy Tổng đạo diễn AI - AI Director Engine v1.0"""
		self.provider = provider.lower()
		self.api_key = os.getenv("AI_STUDIO_API_KEY", "MOCK_KEY_FOR_TESTING")

	def direct_scene_script(self, raw_novel_text: str, scene_index: int = 1) -> dict:
		"""
		[AI DIRECTOR ENGINE CORE PIPELINE]
		Đọc văn bản văn học truyện thô -> Tự động phân tích ngữ cảnh vĩ mô 
		-> Chỉ định thông số góc máy quay, ánh sáng, thời tiết và sắc thái điện ảnh.
		"""
		studio_logger.logger.info(f"[AI DIRECTOR] Đang phân tích chỉ đạo nghệ thuật cho Phân cảnh {scene_index:03d}...")

		# --- LUỒNG DỰ PHÒNG CHẠY OFFLINE (FALLBACK MOCK DATA CHUẨN KIẾN TRÚC) ---
		if self.api_key == "MOCK_KEY_FOR_TESTING":
			# Nếu đang chạy test hoặc chưa nạp API Key thật, tự động trả về gói chỉ thị điện ảnh chuẩn để dây chuyền không bị ngắt quãng
			mock_director_directives = {
				"scene_metadata": {
					"id": scene_index,
					"summary": "Tô Mộc vung thần kiếm đối đầu với kẻ địch tại đấu trường học viện dưới cơn mưa lớn."
				},
				"cinematic_directives": {
					"camera_preset": "Toàn cảnh",
					"lighting": "Dramatic Night Chiaroscuro",
					"weather": "Heavy Rain with Thunder Sparks",
					"mood": "Epic High-Arousal Combat"
				}
			}
			return mock_director_directives

		# --- LUỒNG KẾT NỐI API LLM NETWORK THỰC TẾ TRÊN MẠNG ---
		system_instruction = (
			"You are a professional 3D Donghua Movie Director. Analyze the input novel text and generate "
			"cinematic directives. You MUST return a valid JSON object matching this schema exactly: "
			"{'scene_metadata': {'id': int, 'summary': string}, "
			"'cinematic_directives': {'camera_preset': string, 'lighting': string, 'weather': string, 'mood': string}}"
		)

		try:
			if self.provider == "gemini":
				import google.generativeai as genai
				genai.configure(api_key=self.api_key)
				model = genai.GenerativeModel('gemini-pro')
				response = model.generate_content(f"{system_instruction}\n\nNovel Text:\n{raw_novel_text}")
				return json.loads(response.text)
				
			elif self.provider == "openai":
				from openai import OpenAI
				client = OpenAI(api_key=self.api_key)
				response = client.chat.completions.create(
					model="gpt-4-turbo",
					messages=[
						{"role": "system", "content": system_instruction},
						{"role": "user", "content": raw_novel_text}
					],
					response_format={"type": "json_object"}
				)
				return json.loads(response.choices.message.content)
				
		except Exception as e:
			studio_logger.logger.error(f"AI Director lỗi kết nối mạng API: {e}. Tự động kích hoạt luồng dự phòng an toàn.")
			return {
				"scene_metadata": {"id": scene_index, "summary": "Hành động mặc định"},
				"cinematic_directives": {"camera_preset": "Toàn cảnh", "lighting": "Morning", "weather": "Sunny", "mood": "Epic"}
			}
