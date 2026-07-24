import unittest
import json
from ai.ai_director import AIDirectorEngine
import sys
import os
# Ép Python đưa thư mục gốc của dự án DreamForge Engine vào danh sách tìm kiếm module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Bây giờ dòng import này sẽ chạy hoàn toàn mượt mà, không sợ lỗi ModuleNotFoundError
from ai.ai_director import AIDirectorEngine

class TestAIDirectorSprint10(unittest.TestCase):
	def test_ai_director_artistic_directives(self):
		"""Ca kiểm thử nghiệm thu: Xác thực cỗ máy AI xuất ra gói chỉ đạo nghệ thuật cấu trúc JSON sạch"""
		novel_paragraph = "Gió lạnh thổi qua đấu trường, Tô Mộc siết chặt chuôi thần kiếm trong tay, ánh mắt rực lửa chiến ý."
		
		# Khởi chạy động cơ đạo diễn trung tâm
		director = AIDirectorEngine()
		directives_output = director.direct_scene_script(novel_paragraph, scene_index=7)
		
		print("\n============ KẾT QUẢ NGHIỆM THU SPRINT 10 - AI DIRECTOR ENGINES ============")
		print(json.dumps(directives_output, ensure_ascii=False, indent=4))
		print("============================================================================")

		# Khẳng định kiểm thử tự động (Assertions) đạt chuẩn thương mại của DreamForge v1.0
		self.assertEqual(directives_output["scene_metadata"]["id"], 7)
		self.assertIn("camera_preset", directives_output["cinematic_directives"])
		self.assertIn("lighting", directives_output["cinematic_directives"])
		self.assertIn("mood", directives_output["cinematic_directives"])

if __name__ == "__main__":
	unittest.main()
