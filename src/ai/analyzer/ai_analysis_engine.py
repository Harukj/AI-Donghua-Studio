import os
import json
from src.core.logger import studio_logger

class AIAnalysisEngine:
	def __init__(self, provider: str = "gemini"):
		"""Khởi tạo cấu hình kết nối API AI (Mặc định chọn Gemini hoặc OpenAI)"""
		self.provider = provider.lower()
		self.api_key = os.getenv("AI_STUDIO_API_KEY", "MOCK_KEY_FOR_TESTING")

	def analyze_scene_text(self, raw_scene_text: str) -> dict:
		"""
		[AI ANALYSIS ENGINE CORE PIPELINE]
		Gửi văn bản truyện chữ sang LLM API để bóc tách tự động ra cấu trúc 
		Nhân vật, Bối cảnh, Góc máy và Prompt nghệ thuật theo đúng sơ đồ Phase 2.
		"""
		studio_logger.logger.info(f"AI Engine: Đang gửi phân cảnh sang {self.provider.upper()} API để bóc tách ngữ cảnh...")

		# Câu lệnh Prompt System nghiêm ngặt ép AI phải trả về định dạng cấu trúc JSON
		system_prompt = (
			"You are an AI Movie Director for a 3D Donghua Studio. Analyze the given novel scene paragraph "
			"and extract cinematic elements. You MUST return a valid JSON object with the exact keys: "
			"'characters' (list of strings), 'environment' (string), 'camera' (string), and 'prompt_tags' (list of strings description)."
		)

		# --- LUỒNG TRƯỜNG HỢP 1: NẾU CHƯA CÓ API KEY THẬT (CHẠY GIẢ LẬP MOCK DATA ĐỂ TEST SẠCH LỖI) ---
		if self.api_key == "MOCK_KEY_FOR_TESTING":
			# Giả lập phản hồi cấu trúc JSON sạch từ API AI để Pipeline v1.0 không bị ngắt quãng
			mock_response = {
				"characters": ["Tô Mộc"],
				"environment": "Học viện Long Dạng",
				"camera": "Over Shoulder, Low Angle Shot",
				"prompt_tags": ["masterpiece", "cinematic lighting", "sunset sky", "wonder expression"]
			}
			return mock_response

		# --- LUỒNG TRƯỜNG HỢP 2: KẾT NỐI API THỰC TẾ (SẴN SÀNG KHI CÓ KEY) ---
		try:
			if self.provider == "gemini":
				import google.generativeai as genai
				genai.configure(api_key=self.api_key)
				model = genai.GenerativeModel('gemini-pro')
				response = model.generate_content(f"{system_prompt}\n\nNovel Text:\n{raw_scene_text}")
				return json.loads(response.text)
				
			elif self.provider == "openai":
				from openai import OpenAI
				client = OpenAI(api_key=self.api_key)
				response = client.chat.completions.create(
					model="gpt-4-turbo",
					messages=[
						{"role": "system", "content": system_prompt},
						{"role": "user", "content": raw_scene_text}
					],
					response_format={"type": "json_object"}
				)
				return json.loads(response.choices[0].message.content)
				
		except Exception as e:
			studio_logger.logger.error(f"AI Engine lỗi kết nối API: {e}. Tự động chuyển sang chế độ dự phòng.")
			return {"characters": ["Quần chúng"], "environment": "Mặc định", "camera": "Medium Shot", "prompt_tags": ["cinematic"]}
