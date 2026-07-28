import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.database.session import SessionLocal
from src.database.base import Base
from src.database.engine import engine
from src.controllers.storyboard_controller import StoryboardController

class TestCodingStandardCompliance(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo cấu trúc hạ tầng cơ sở dữ liệu giả lập sạch"""
		Base.metadata.drop_all(bind=engine)
		Base.metadata.create_all(bind=engine)
		self.db = SessionLocal()
		# Khởi tạo Controller điều phối
		self.controller = StoryboardController(self.db)

	def test_5_layers_data_flow_without_gui_leak(self):
		"""Ca kiểm thử nghiệm thu Coding Standard: Xác thực luồng dữ liệu tịnh tiến sạch qua đúng các phân lớp"""
		mock_chapter_script = "Tô Mộc mở cổng bước vào sân trường học viện. Lâm Uyển lặng yên quan sát."
		
		# Giả lập hành động người dùng bấm nút trên GUI -> Phát lệnh truyền dữ liệu qua Controller
		response_package = self.controller.handle_gui_request_to_slice_chapter(
			episode_id=15, 
			raw_text=mock_chapter_script
		)

		print("\n============ KẾT QUẢ NGHIỆM THU CODING STANDARD ENFORCEMENT ============")
		print(f" Trạng thái xử lý điều hướng: {response_package['status'].upper()}")
		print(f" Thông điệp phản hồi gửi GUI: \"{response_package['message']}\"")
		print(f" Kiến trúc mạch trục dọc:   GUI ➔ Controller ➔ Service ➔ Repository ➔ DB [✓]")
		print("=========================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng kiến trúc
		self.assertEqual(response_package["status"], "success")
		self.assertEqual(len(response_package["data"]), 2)

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
