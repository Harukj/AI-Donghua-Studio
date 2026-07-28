import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugins.plugin_manager import DreamForgeAPIManager
from plugins.ltx_automation import LTXAutomationAdapter

class TestDreamForgeAPIRegistry(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo trung tâm điều phối API và nạp Plugin mẫu"""
		self.api_gateway = DreamForgeAPIManager()
		self.ltx_adapter = LTXAutomationAdapter()

	def test_automated_plugin_registration_and_api_gateway_call(self):
		"""Ca kiểm thử tối vĩ đại: Xác thực vòng đời đăng ký và gọi API tập trung sạch lỗi"""
		# 1. Thực hiện đăng ký Plugin qua cổng API Manager
		reg_success = self.api_gateway.register_plugin_adapter(self.ltx_adapter)
		self.assertTrue(reg_success)

		# 2. Phát chỉ thị thực thi thông qua cổng API tập trung thay vì gọi trực tiếp Class con
		mock_payload = {
			"scene_id": "shot_1502",
			"prompt_data": "3D Donghua animation, character Lam Uyen waiting under old tree"
		}
		
		# Gọi thông qua thực thể execute_api_call bám sát thiết kế DreamForge API của ChatGPT
		api_report = self.api_gateway.execute_api_call(
			plugin_name="ltx_automation_adapter",
			payload=mock_payload
		)

		print("\n============ KẾT QUẢ NGHIỆM THU ĐỘNG CƠ CORE - DREAMFORGE API ============")
		print(f" 📡 Trạng thái Cổng API Gateway: {api_report['status'].upper()}")
		print(f" 🔌 Định tuyến dynamic Adapter:  {api_report['plugin'].upper()}")
		print(f" 🎬 Video Clip xuất xưởng:      {api_report['video_path']}")
		print("=========================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng kiến trúc
		self.assertEqual(api_report["status"], "success")
		self.assertIn("shot_1502", api_report["video_path"])
		self.assertTrue(api_report["video_path"].endswith(".mp4"))

if __name__ == "__main__":
	unittest.main()
