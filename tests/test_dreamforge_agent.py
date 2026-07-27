import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.dreamforge_agent import DreamForgeAIAgent
from services.production_scheduler import ProductionScheduler
from database.session import SessionLocal

class TestDreamForgeAgentv09(unittest.TestCase):
	def test_agent_autonomous_reasoning_and_scheduler_hud(self):
		"""Ca kiểm thử tối thượng: Xác thực AI Agent tự trị ra quyết định và Scheduler cập nhật mốc HUD 28%"""
		db = SessionLocal()
		story_text = "Tô Mộc bất ngờ quay đầu nhìn về phía chân trời xa xăm."
		
		# 1. Tích kiểm hoạt động của AI Agent tự trị
		agent = DreamForgeAIAgent()
		agent_output = agent.run_autonomous_director_agent(story_text)
		
		print("\n============ KẾT QUẢ NGHIỆM THU REASONING AGENT (CON SỐ MỚI 28%) ============")
		print(f" 🤖 AI Agent suy luận quyết định: \"{agent_output['agent_decision']}\"")
		print(f" 🖼️ Ý tưởng thiết kế ảnh bìa Thumbnail: {agent_output['directives_matrix']['thumbnail_concept']}")
		print("=============================================================================")

		self.assertIn("thumbnail_concept", agent_output["directives_matrix"])
		self.assertEqual(agent_output["directives_matrix"]["estimated_progress"], "28%")

		# 2. Tích kiểm nút gộp Production Scheduler mốc 28%
		scheduler = ProductionScheduler(db)
		report = scheduler.schedule_episode_production_matrix("ToanDanTaoPhong", 15, [story_text])
		self.assertEqual(report["production_hud_progress"], "28%")
		self.assertIn("thumbnail_node", report)
		
		db.close()

if __name__ == "__main__":
	unittest.main()
