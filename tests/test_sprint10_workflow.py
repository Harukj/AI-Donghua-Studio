import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from database.base import Base
from database.engine import engine
from services.production_workflow import ProductionWorkflowEngine

class TestProductionWorkflowSprint10(unittest.TestCase):
	def setUp(self):
		Base.metadata.create_all(bind=engine)
		self.db = SessionLocal()
		self.engine = ProductionWorkflowEngine(self.db)

	def test_sequential_5_stages_transition(self):
		"""Ca kiểm thử nghiệm thu: Xác thực mạch dịch chuyển tuần tự qua đúng 5 nấc đặc tả của ChatGPT"""
		# Nấc 1: Chapter sang Scene
		stage2 = self.engine.advance_workflow_stage("chapter")
		self.assertEqual(stage2, "scene")

		# Nấc 2: Scene sang Shot
		stage3 = self.engine.advance_workflow_stage(stage2)
		self.assertEqual(stage3, "shot")

		# Nấc 3: Shot sang Prompt
		stage4 = self.engine.advance_workflow_stage(stage3)
		self.assertEqual(stage4, "prompt")

		# Nấc 4: Prompt sang Videos (Kết xuất thành phẩm)
		stage5 = self.engine.advance_workflow_stage(stage4)
		self.assertEqual(stage5, "videos")

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
