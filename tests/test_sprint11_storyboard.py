import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from database.base import Base
from database.engine import engine
from ai.scene_splitter.storyboard import StoryboardEngine

class TestStoryboardQAReview(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo cấu trúc hạ tầng cơ sở dữ liệu giả lập sạch"""
		Base.metadata.create_all(bind=engine)
		self.db = SessionLocal()
		self.engine = StoryboardEngine(self.db)

	def test_senior_architecture_storyboard_slicing(self):
		"""Ca kiểm thử nghiệm thu QA: Xác thực thuật toán bẻ cú pháp phân cảnh văn học hoạt động sạch lỗi logic"""
		mock_novel_story = "Tô Mộc bước vào học viện Long Dạng. Lâm Uyển lặng lẽ đứng đợi dưới gốc cây cổ thụ."
		
		# Kích hoạt động cơ phân rã Storyboard v0.8
		scenes_matrix = self.engine.slice_novel_into_vivid_scenes(episode_id=15, raw_novel_text=mock_novel_story)

		print("\n============ KẾT QUẢ NGHIỆM THU QA CODE REVIEW - MILESTONE v0.8 ============")
		for sc in scenes_matrix:
			print(f"🎬 [Scene ID: {sc['scene_id']}] Vị trí: {sc['scene_index']} | Nội dung bối cảnh: \"{sc['scene_text']}\"")
		print("=========================================================================")

		# Khẳng định kiểm thử tự động (Assertions) đạt tiêu chuẩn chất lượng của Microsoft/JetBrains
		self.assertEqual(len(scenes_matrix), 2) # Bộ truyện 2 câu bắt buộc phải rã thành đúng 2 phân cảnh độc lập
		self.assertEqual(scenes_matrix[0]["scene_id"], 1501) # Khớp chính xác ID phân tầng tầng 1501
		self.assertEqual(scenes_matrix[1]["scene_index"], 2)

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
    