import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from database.base import Base
from database.engine import engine
from database.models.shot import ShotModel
from ai.prompt_builder.consistency_engine import AssetConsistencyEngine

class TestAssetConsistencyv08(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo cấu trúc bảng SQLite giả lập và nạp 2 Shots chờ xử lý"""
		from database.base import Base
		from database.engine import engine
		
		Base.metadata.create_all(bind=engine)
		self.db = SessionLocal()
		self.engine = AssetConsistencyEngine(self.db)

		# Cú máy 1: Xóa bỏ tham số prompt_formula gãy xích
		self.shot_draft = ShotModel(
			id=990101, scene_id=9901, index=1, status="draft",
			prompt="3d donghua, character To Moc with long black hair walking"
		)
		
		# Cú máy 2: Xóa bỏ tham số prompt_formula gãy xích
		self.shot_rendered = ShotModel(
			id=990102, scene_id=9901, index=2, status="rendered",
			prompt="3d donghua, character To Moc with long black hair looking back"
		)

		self.db.add(self.shot_draft)
		self.db.add(self.shot_rendered)
		self.db.commit()


	def test_cascade_token_propagation_logic(self):
		"""Ca kiểm thử tối thượng: Xác thực việc thay đổi kiểu tóc chỉ lan truyền xuống file chưa render"""
		# Đạo diễn phát lệnh đổi sang kiểu tóc ngắn: short black hair
		total_propagated = self.engine.propagate_character_token_update(
			char_name="To Moc",
			component_type="hair",
			new_token_value="short black hair",
			auto_confirm=True
		)

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng
		self.assertEqual(total_propagated, 1) # Bắt buộc chỉ được cập nhật duy nhất 1 file dạng draft

		# Truy vấn lại DB để kiểm tra nội dung chuỗi Prompt đã được nối đuôi Token tóc mới chưa
		updated_draft_shot = self.db.query(ShotModel).filter(ShotModel.id == 990101).first()
		self.assertIn("updated_hair: short black hair", updated_draft_shot.prompt)

		# Đảm bảo file đã render không bị biến đổi bậy bạ làm hỏng phim cũ
		intact_rendered_shot = self.db.query(ShotModel).filter(ShotModel.id == 990102).first()
		self.assertNotIn("updated_hair", intact_rendered_shot.prompt)

	def tearDown(self):
		self.db.delete(self.shot_draft)
		self.db.delete(self.shot_rendered)
		self.db.commit()
		self.db.close()

if __name__ == "__main__":
	unittest.main()
