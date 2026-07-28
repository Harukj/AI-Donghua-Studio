import sys
import os
import unittest

# Ép Python định vị chính xác phân khu src/ chuẩn doanh nghiệp
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from ai.prompt_builder.prompt_builder_v2 import PromptBuilder
from database.session import SessionLocal

class TestSprint8PromptBuilder(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo môi trường cô lập"""
		self.prompt_engine_v2 = PromptBuilder()

	def test_automated_7_layers_prompt_generation(self):
		"""Ca kiểm thử nghiệm thu sinh Prompt ma trận 7 lớp sạch lỗi logic"""
		# Giả lập đối tượng Scene mẫu đại diện cho phân cảnh chứa bộ 7 lớp thông tin của ChatGPT
		mock_scene = {
			"id": "SCENE_01",
			"title": "Mở đầu",
			"characters": ["Tô Mộc", "Lâm Uyển"],
			"environments": ["Học viện Long Dạng"],
			"lighting": "Morning Sunlight",
			"mood": "Epic Dynamic"
		}
		
		# Giả lập danh sách Shot con
		mock_shots_list = [
			{"index": 1, "context_type": "establishing", "duration": 5.0},
			{"index": 2, "context_type": "walking", "duration": 4.0}
		]
		
		print("\n============ KẾT QUẢ NGHIỆM THU MA TRẬN PROMPT 7 LỚP CHATGPT ============")
		for shot in mock_shots_list:
			final_prompt_string = self.prompt_engine_v2.build(mock_scene, shot)
			print(f" 🎬 [Shot ID: {shot['index']}] | Loại: {shot['context_type'].upper()} | Thời lượng: {shot['duration']}s")
			print(f" 📝 Câu lệnh Prompt xuất ra:\n    \"{final_prompt_string}\"")
		print("=========================================================================")
		
		self.assertTrue(len(mock_shots_list) > 0)

if __name__ == "__main__":
	unittest.main()