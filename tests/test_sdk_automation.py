import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.plugins.ltx_automation import LTXAutomationAdapter

class TestDreamForgeSDKSubsystem(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo và cắm nạp Plugin mẫu thử nghiệm"""
		self.plugin = LTXAutomationAdapter()

	def test_sdk_shared_api_compliance_lifecycle(self):
		"""Ca kiểm thử tối vĩ đại: Xác thực vòng đời nạp Plugin tuân thủ chung API initialize và execute"""
		# 1. Tích kiểm nấc khởi tạo API chung
		init_success = self.plugin.initialize()
		self.assertTrue(init_success)

		# 2. Tích kiểm nấc kích hoạt và cắm rút
		self.plugin.activate_plugin()
		self.assertTrue(self.plugin.is_active)

		# 3. Tích kiểm luồng xử lý thực thi truyền nhận Payload sạch
		mock_payload = {
			"scene_id": "shot_1501",
			"prompt_data": "3D Donghua animation, character To Moc standing under golden hour sun"
		}
		render_report = self.plugin.execute(mock_payload)

		print("\n============ KẾT QUẢ NGHIỆM THU KIẾN TRÚC SUPREME DREAMFORGE SDK ============")
		print(f" 🔌 Tên Plugin nạp thành công: {render_report['plugin'].upper()}")
		print(f" 🛠️ Phương thức API 1 [initialize]: ĐẠT TIÊU CHUẨN [✓]")
		print(f" 🛠️ Phương thức API 2 [execute]:    ĐẠT TIÊU CHUẨN [✓]")
		print(f" 🎥 Đường dẫn vật lý Asset xuất xưởng: {render_report['video_path']}")
		print("=============================================================================")

		self.assertEqual(render_report["status"], "success")
		self.assertTrue(render_report["video_path"].endswith("shot_1501.mp4"))

if __name__ == "__main__":
	unittest.main()
