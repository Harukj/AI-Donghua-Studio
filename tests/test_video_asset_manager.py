import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.video_asset_manager import VideoAssetManager

class TestVideoAssetManagerv10(unittest.TestCase):
	def setUp(self):
		"""Thiết lập môi trường giả lập tệp tin trước khi test"""
		self.project_name = "ToanDanTaoPhong_Test"
		self.manager = VideoAssetManager(project_id=self.project_name)
		
		# Khởi tạo một file clip tạm thời trong thư mục bộ nhớ đệm cache
		self.mock_cache_file = "mock_cache_shot.mp4"
		with open(self.mock_cache_file, "w") as f:
			f.write("VIDEO_STREAM_DATA")

	def test_automated_video_positioning_tree(self):
		"""Ca kiểm thử nghiệm thu: Xác thực file thô được di chuyển và đổi tên thành Shot01.mp4 tăm tắp"""
		# Kích hoạt luồng đồng bộ file vật lý của Asset Manager
		final_dest = self.manager.register_rendered_shot_clip(self.mock_cache_file, shot_index=1)
		
		print("\n============ KẾT QUẢ NGHIỆM THU VIDEO ASSET MANAGER V1.0 ============")
		print(f" Vị trí file video gốc sau khi đồng bộ cấu trúc:\n \"{final_dest}\"")
		print("=====================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng
		self.assertTrue(final_dest.endswith("Shot01.mp4"))
		self.assertTrue(os.path.exists(final_dest))
		
		# Kiểm tra hàm quét danh mục phục vụ Timeline Engine
		ordered_list = self.manager.get_all_ordered_shots()
		self.assertEqual(len(ordered_list), 1)

	def tearDown(self):
		"""Dọn dẹp sạch sẽ các tệp tin và thư mục giả lập sau khi kết thúc test"""
		import shutil
		test_dir = os.path.join("projects", self.project_name)
		if os.path.exists(test_dir):
			shutil.rmtree(test_dir)
		if os.path.exists(self.mock_cache_file):
			os.remove(self.mock_cache_file)

if __name__ == "__main__":
	unittest.main()
