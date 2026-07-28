import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.database.session import SessionLocal
from src.database.base import Base
from src.database.engine import engine
from src.services.prompt_service import PromptComposerService

class TestPromptComposerV2Subsystem(unittest.TestCase):
	def setUp(self):
		Base.metadata.create_all(bind=engine)
		self.db = SessionLocal()
		self.service = PromptComposerService(self.db)

	def test_automated_9_layers_static_mixing_and_override(self):
		"""Ca kiểm thử nghiệm thu: Xác thực thuật toán trộn 9 lớp và tính năng tự động cập nhật Prompt khi đổi Camera"""
		# 1. Kiểm tra luồng sinh câu lệnh ma trận mặc định
		default_package = self.service.compose_shot_prompt_from_components(shot_id=150101)
		self.assertIn("3d chinese donghua animation style", default_package["positive"])
		self.assertIn("close up shot", default_package["positive"])

		# 2. Giả lập hành động của Đạo diễn: Đổi từ Close Up sang Toàn cảnh (Establishing Shot)
		# Toàn bộ câu lệnh phải tự động cập nhật lan truyền tăm tắp
		camera_preset_override = {
			"camera": "wide establishing panoramic shot, drone viewpoint"
		}
		updated_package = self.service.compose_shot_prompt_from_components(
			shot_id=150101, 
			dynamic_overrides=camera_preset_override
		)

		print("\n============ KẾT QUẢ NGHIỆM THU COMPONENT PROMPT ENGINE v2.0 ============")
		print(f" 🎬 Câu lệnh trộn 9 lớp tự động cập nhật (Sau khi Đạo diễn đổi góc máy):\n \"{updated_package['positive']}\"")
		print("=========================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng dữ liệu
		self.assertIn("wide establishing panoramic shot", updated_package["positive"])
		self.assertNotIn("close up shot", updated_package["positive"]) # Bảo đảm góc máy cũ đã bị xóa bỏ hoàn toàn
		self.assertIn("character profile: to moc", updated_package["positive"]) # Bảo đảm các thành phần khác được giữ nguyên vẹn

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
