import unittest
import os
import sys

# Đảm bảo Python nhận diện được đường dẫn root của dự án để thực hiện import chéo
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.ai.scene_splitter.scene import SceneObject
from src.ai.prompt_builder.builder import StaticPromptBuilder

class TestSprint7AICore(unittest.TestCase):
	def setUp(self):
		"""Thiết lập môi trường giả lập trước khi chạy từng ca kiểm thử"""
		self.builder = StaticPromptBuilder()

	def test_dialogue_context_prompt_generation(self):
		"""Ca kiểm thử 1: Xác thực hệ thống tự động nhận diện kịch bản thoại để nạp ltx_dialogue template"""
		# Khởi tạo một đối tượng phân cảnh chứa mảng kịch bản thoại thật
		mock_scene = SceneObject(
			id="SCENE_01_001",
			chapter=1,
			title="Cuộc trò chuyện",
			summary="Lâm Uyển nhìn Tô Mộc và nói: 'Cậu đến rồi à.'",
			characters=["Tô Mộc", "Lâm Uyển"],
			environments=["Học viện Long Dạng"]
		)
		mock_scene.dialogues = [{"speaker": "Lâm Uyển", "text": "Cậu đến rồi à."}]
		mock_scene.mood = "Mysterious"

		# Kích hoạt bộ sinh prompt tự động chọn template theo ngữ cảnh
		result = self.builder.generate_prompt_from_scene(mock_scene)
		
		# Khẳng định kiểm thử (Assertions)
		self.assertIn("character Tô Mộc, Lâm Uyển", result["positive"])
		self.assertIn("inside học viện long dạng", result["positive"])
		self.assertIn("mysterious atmosphere", result["positive"])
		self.assertIn("low quality", result["negative"]) # Đảm bảo negative prompt được nạp thành công từ file json

	def test_action_context_prompt_generation(self):
		"""Ca kiểm thử 2: Xác thực hệ thống tự động nhận diện từ khóa va chạm mạnh để nạp ltx_action template"""
		mock_scene = SceneObject(
			id="SCENE_01_002",
			chapter=1,
			title="Trận chiến",
			summary="Tô Mộc vung thần kiếm lao vào quyết đấu kịch liệt.",
			characters=["Tô Mộc"],
			environments=["Đấu trường"]
		)
		mock_scene.mood = "Epic"

		result = self.builder.generate_prompt_from_scene(mock_scene)
		
		# Khẳng định bộ trộn đã kích hoạt đúng các từ khóa chuyển động camera nhanh (combat presets) của action template
		self.assertIn("fast tracking dynamic panning shot", result["positive"])
		self.assertIn("epic atmosphere", result["positive"])

if __name__ == "__main__":
	unittest.main()
