import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_director_service import AIDirectorService

class TestAIDirectorSprint10Subsystem(unittest.TestCase):
	def setUp(self):
		self.director = AIDirectorService()

	def test_automated_6_layers_cinematic_extraction(self):
		"""Ca kiểm thử nghiệm thu: Xác thực bộ não đạo diễn tự động bóc tách đúng 6 thông số điện ảnh của ChatGPT"""
		# Lấy chính xác 100% câu văn văn học thô trên màn hình trình duyệt của bạn làm đầu vào
		raw_novel_paragraph = "Tô Mộc nhìn lên bầu trời."
		
		# Kích hoạt luồng xử lý tự trị của Tổng đạo diễn AI
		directives_output = self.director.analyze_novel_text_directives(raw_novel_paragraph, shot_index=1)
		cinematic = directives_output["cinematic_directives"]

		print("\n============ KẾT QUẢ NGHIỆM THU AI DIRECTOR v1.0 [SIÊU PHẨM] ============")
		print(f" 📖 Đoạn truyện chữ đầu vào: \"{directives_output['shot_metadata']['input_text']}\"")
		print(f" 📹 Loại khung hình (Shot):  {cinematic['shot'].upper()}")
		print(f" 🔎 Ống kính điện ảnh (Lens): {cinematic['camera']}")
		print(f" ⚙️ Chuyển động ảo (Movement): {cinematic['movement']}")
		print(f" ☀️ Bộ lọc ánh sáng (Lighting): {cinematic['lighting']}")
		print(f" ⏳ Thời lượng kết xuất (Time): {cinematic['duration']} giây")
		print(f" 🎭 Biểu cảm nhân vật (Emotion): {cinematic['emotion']}")
		print("=========================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng dữ liệu
		self.assertEqual(cinematic["shot"], "Wide Shot")
		self.assertEqual(cinematic["camera"], "24mm lens")
		self.assertEqual(cinematic["movement"], "Slow Push")
		self.assertEqual(cinematic["lighting"], "Golden Hour setup")
		self.assertEqual(cinematic["duration"], 4.0) # Khóa cứng mốc thời gian 4 giây của ChatGPT
		self.assertEqual(cinematic["emotion"], "Hopeful facial expression")

if __name__ == "__main__":
	unittest.main()
