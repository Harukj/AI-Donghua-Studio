import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugins.plugin_manager import DreamForgeAPIManager

class TestDreamForgeAPIRegistry(unittest.TestCase):
	def setUp(self):
		self.api = DreamForgeAPIManager()

	def test_chatgpt_5_sequential_api_calls(self):
		"""Ca kiểm thử tối vĩ đại: Xác thực chuỗi kịch bản lập trình tự trị 5 nấc khép kín của Version 1.0"""
		
		# 1. api.open_project()
		self.api.open_project(project_id="ToanDanTaoPhong")
		self.assertEqual(self.api.active_project_id, "ToanDanTaoPhong")

		# 2. api.current_scene()
		self.api.current_scene(scene_id=1501)
		self.assertEqual(self.api.active_scene_id, 1501)

		# 3. api.get_character()
		char_token = self.api.get_character(char_name="To Moc")
		self.assertIn("character profile: to moc", char_token)

		# 4. api.build_prompt()
		full_prompt = self.api.build_prompt(style="3d chinese donghua style", char_token=char_token)
		self.assertIn("unreal engine 5", full_prompt)

		# 5. api.render()
		render_report = self.api.render(compiled_prompt=full_prompt)
		
		print("\n============ KẾT QUẢ NGHIỆM THU CHUYÊN SÂU - VERSION 1.0 THẬT SỰ ============")
		print(f" 🎬 [Bước 1 & 2]: Khai hỏa Dự án phim: {self.api.active_project_id} | Cảnh số: {self.api.active_scene_id}")
		print(f" ⚙️ [Bước 3 & 4]: Chuỗi Prompt ma trận kết xuất: \"{full_prompt[:50]}...\"")
		print(f" 🎥 [Bước 5]:     Đường dẫn file Asset xuất xưởng: {render_report['video_path']}")
		print("=============================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng dữ liệu
		self.assertEqual(render_report["status"], "success")
		self.assertTrue(render_report["video_path"].endswith("shot_1501.mp4"))

if __name__ == "__main__":
	unittest.main()
