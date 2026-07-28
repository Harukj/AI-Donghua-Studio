import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.ai.scene_intelligence import SceneIntelligence

class TestSceneIntelligencev08(unittest.TestCase):
	def test_yaml_data_structural_mapping(self):
		"""Ca kiểm thử nghiệm thu: Xác thực cỗ máy bóc tách đúng cấu trúc file YAML 6 tầng của ChatGPT"""
		# Giả lập chính xác 100% dữ liệu từ hình ảnh hộp thoại YAML trên trình duyệt của bạn
		mock_chatgpt_yaml = {
			"Scene": {
				"title": "Gặp nhau tại học viện"
			},
			"Characters": ["Tô Mộc", "Lâm Uyển"],
			"Environment": "Học viện Long Dạng",
			"Action": ["Đi vào", "Nhìn nhau"],
			"Emotion": ["Bình tĩnh", "Mong chờ"],
			"Suggested_camera": ["Establishing Shot", "Medium Shot", "Close Up"]
		}
		
		intel_engine = SceneIntelligence()
		result = intel_engine.parse_cinematic_yaml_directives(mock_chatgpt_yaml)
		
		print("\n============ KẾT QUẢ NGHIỆM THU STRUCTURAL YAML MAPPING ============")
		print(f" Cảnh quay:  \"{result['scene_title']}\"")
		print(f" Nhân vật:  {result['characters_list']}")
		print(f" Hành động: \"{result['action_tags']}\"")
		print(f" Cảm xúc:   \"{result['emotion_tags']}\"")
		print(f" Góc máy:   {result['cameras_list']}")
		print("====================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng dữ liệu
		self.assertEqual(result["scene_title"], "Gặp nhau tại học viện")
		self.assertEqual(len(result["characters_list"]), 2)
		self.assertIn("Establishing Shot", result["cameras_list"])
		self.assertEqual(len(result["cameras_list"]), 3) # Bắt buộc phải có 3 cú máy bẻ nhỏ

if __name__ == "__main__":
	unittest.main()
