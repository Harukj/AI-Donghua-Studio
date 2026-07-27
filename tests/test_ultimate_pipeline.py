import unittest
import os  # Bổ sung dòng import này để sửa lỗi NameError
from database.session import SessionLocal
from database.base import Base
from database.engine import engine
from pipeline.ultimate_movie_pipeline import UltimateMoviePipeline

class TestUltimateMoviePipeline(unittest.TestCase):
	def setUp(self):
		Base.metadata.create_all(bind=engine)
		self.db = SessionLocal()
		self.pipeline = UltimateMoviePipeline(self.db)

	def test_full_horizontal_movie_production(self):
		mock_docx_input = "projects/ToanDanTaoPhong/novel/chuong_15.docx"
		
		final_output_movie = self.pipeline.execute_production_pipeline(
			docx_file_path=mock_docx_input,
			project_id="ToanDanTaoPhong",
			episode_num=15
		)
		
		self.assertTrue(final_output_movie.endswith("Episode15.mp4"))
		self.assertTrue(os.path.exists(os.path.dirname(final_output_movie)))

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
