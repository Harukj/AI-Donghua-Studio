import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.database.session import SessionLocal
from src.database.base import Base
from src.database.engine import engine
from src.database.models.episode import EpisodeModel
from src.services.ai_production_assistant import AIProductionAssistant

class TestAIProductionAssistantSubsystem(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo hạ tầng cơ sở dữ liệu giả lập sạch"""
		Base.metadata.drop_all(bind=engine)
		Base.metadata.create_all(bind=engine)
		
		self.db = SessionLocal()
		self.assistant = AIProductionAssistant(self.db)

		# Nạp bản ghi tập phim mẫu phục vụ kiểm thử
		self.test_ep = EpisodeModel(project_id="ToanDanTaoPhong", episode_number=15, status="In Progress")
		self.db.add(self.test_ep)
		self.db.commit()

	def test_single_trigger_agent_production_lifecycle(self):
		"""Ca kiểm thử tối vĩ đại: Xác thực nút bấm đơn nhất kích hoạt Agent tự trị vận hành khép kín chuỗi 8 bước của ChatGPT"""
		story_text = "Tô Mộc mở cửa bước vào học viện. Lâm Uyển đang đứng đợi ở sân."
		
		# Giả lập người dùng bấm nút [ Create Episode ] duy nhất một lần
		agent_success = self.assistant.execute_autonomous_production_lifecycle(
			project_id="ToanDanTaoPhong", episode_num=15, raw_chapter_text=story_text
		)

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng dữ liệu
		self.assertTrue(agent_success)

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
