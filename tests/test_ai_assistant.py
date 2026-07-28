import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from database.base import Base
from database.engine import engine
from database.models.episode import EpisodeModel
from services.ai_production_assistant import AIProductionAssistant

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

	def test_single_trigger_agent_export_lifecycle(self):
		"""Ca kiểm thử tối vĩ đại: Xác thực nút bấm đơn nhất kích hoạt Agent tự trị xuất bản trọn gói 6 nấc metadata"""
		# Giả lập người dùng bấm nút [export episode] duy nhất một lần
		agent_report = self.assistant.trigger_autonomous_export_workflow(
			project_id="ToanDanTaoPhong", episode_num=15
		)

		print("\n============ KẾT QUẢ NGHIỆM THU AI PRODUCTION ASSISTANT v1.0 ============")
		print(f" 🤖 Trạng thái Agentic: \"{agent_report['status']}\"")
		print(f" 🎞️ File video xuất bản:  {agent_report['output_video']}")
		print(f" 🖼️ Tệp tin ảnh bìa:      {agent_report['thumbnail']}")
		print(f" 📝 Văn bản mô tả SEO:   \"{agent_report['metadata']['description']}\"")
		print(f" 🏷️ Bộ thẻ từ khóa Tags:  [{agent_report['metadata']['tags']}]")
		print("=========================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng dữ liệu
		self.assertEqual(agent_report["status"], "Exported Successfully")
		self.assertTrue(agent_report["output_video"].endswith("Episode15.mp4"))
		self.assertIn("toan dan tao mong", agent_report["metadata"]["tags"])

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
