import unittest
import sys
import os
import pyperclip

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugins.ltx.ltx_automation import LTXAutomationAdapter

class TestLTXAutomationWorkflow(unittest.TestCase):
	def test_full_8_steps_execution_pipeline(self):
		"""Ca kiểm thử tối thượng: Xác thực chuỗi 8 bước tự động hóa của ChatGPT vận hành trơn tru"""
		mock_prompt_package = {
			"positive": "3D Donghua, character To Moc standing in Long Dang academy",
			"negative": "low quality, blurry",
			"seed": "998244353",
			"duration": 4.0,
			"camera": "Wide Shot"
		}
		
		# Khởi chạy bộ tương thích tự động hóa
		adapter = LTXAutomationAdapter()
		adapter.activate_plugin()
		
		success_flag = adapter.execute_render_pipeline(scene_id="scene_01", prompt_data=mock_prompt_package)
		
		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng đầu ra
		self.assertTrue(success_flag)
		# Kiểm tra xem dữ liệu trong Clipboard máy tính có trùng khớp với payload hệ thống tự sinh không
		current_clipboard = pyperclip.paste()
		self.assertIn("998244353", current_clipboard)
		self.assertIn("To Moc standing", current_clipboard)
		
		# Kiểm tra xem file vật lý .mp4 đã được import chuẩn vào thư mục chưa
		expected_file_path = "projects/ToanDanTaoPhong/assets/video/scene_01_render.mp4"
		self.assertTrue(os.path.exists(expected_file_path))
		
		adapter.deactivate_plugin()

if __name__ == "__main__":
	unittest.main()
