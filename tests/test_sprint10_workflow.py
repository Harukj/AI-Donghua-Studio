import unittest
import sys
import os

# Ép Python đưa thư mục gốc của dự án DreamForge Engine vào danh sách tìm kiếm module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.session import SessionLocal
from database.base import Base
from database.engine import engine
from database.models.episode import EpisodeModel
from services.production_workflow import ProductionWorkflowEngine

class TestProductionWorkflowSprint10(unittest.TestCase):
	def setUp(self):
		"""Thiết lập phiên kết nối cơ sở dữ liệu SQLite - Giải phóng xung đột bảng episodes"""
		from database.base import Base
		from database.engine import engine
		
		# 1. Clear hoàn toàn cache metadata cũ để tránh lỗi Table already defined
		Base.metadata.clear()
		
		# 2. Tái khởi tạo lại toàn bộ cấu trúc bảng mới chứa đầy đủ 9 nấc công nghiệp
		Base.metadata.create_all(bind=engine)
		
		self.db = SessionLocal()
		self.engine = ProductionWorkflowEngine(self.db)

		# 3. Khởi tạo bản ghi Tập phim mẫu để nghiệm thu Episode Manager
		self.test_ep = EpisodeModel(project_id="ToanDanTaoPhong", episode_number=15, title="Khởi đầu trận chiến")
		self.db.add(self.test_ep)
		self.db.commit()


	def test_sequential_9_stages_transition(self):
		"""Ca kiểm thử nghiệm thu: Xác thực chuỗi tịnh tiến tăm tắp qua đúng 9 nấc đặc tả của ChatGPT"""
		stages_chain = ["episode", "chapter", "scene", "shot", "asset", "prompt", "render", "review", "export"]
		
		current = "episode"
		for i in range(len(stages_chain) - 1):
			next_stage = self.engine.advance_workflow_stage(current)
			self.assertEqual(next_stage, stages_chain[i+1])
			current = next_stage

	def tearDown(self):
		self.db.delete(self.test_ep)
		self.db.commit()
		self.db.close()

if __name__ == "__main__":
	unittest.main()
