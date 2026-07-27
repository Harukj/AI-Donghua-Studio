import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.scene_intelligence import SceneIntelligence

class TestSceneIntelligencev08(unittest.TestCase):
	def test_yaml_data_structural_mapping(self):
		"""Ca kiểm thử nghiệm thu: Xác thực cỗ máy bóc tách đúng bộ tham số nhân vật và không gian trường ảnh"""
		# Giả lập cấu trúc gói dữ liệu YAML sạch xuất ra từ ảnh mẫu của ChatGPT
		mock_yaml_payload = {
			"characters": ["Tô Mộc", "Lâm Uyển"],
			"environment": "Học viện Long Dạng",
			"camera_setup": {
				"shot": "Medium Shot",
				"movement": "Characters staring at each other"
			}
		}
		
		intel_engine = SceneIntelligence()
		result_tokens = intel_engine.parse_cinematic_yaml_directives(mock_yaml_payload)
		
		print("\n============ KẾT QUẢ NGHIỆM THU PHASE 2 - SCENE INTELLIGENCE ============")
		print(f" 🎭 Token Nhân Vật: \"{result_tokens['character_core']}\"")
		print(f" 🗺️ Token Bối Cảnh: \"{result_tokens['environment_core']}\"")
		print(f" 📹 Token Góc Máy:  \"{result_tokens['camera_action']}\"")
		print("=========================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng dữ liệu
		self.assertIn("Tô Mộc", result_tokens["character_core"])
		self.assertEqual(result_tokens["environment_core"], "Học viện Long Dạng")
		self.assertTrue(result_tokens["camera_action"].startswith("Medium Shot"))

if __name__ == "__main__":
	unittest.main()
