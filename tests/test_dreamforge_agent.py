import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.plugins.ltx_automation import LTXAutomationAdapter
from src.services.production_scheduler import ProductionScheduler
from src.database.session import SessionLocal
from src.ai.dreamforge_agent import DreamForgeAIAgent
class TestDreamForgeAgentv09(unittest.TestCase):
	def test_agent_autonomous_reasoning_and_scheduler_hud(self):
		"""Ca kiểm thử tối thượng: Xác thực AI Agent tự trị ra quyết định xuất bản video và Scheduler cập nhật mốc HUD 28%"""
		db = SessionLocal()
		story_text = "Tô Mộc bất ngờ quay đầu nhìn về phía chân trời xa xăm."
		
		# 1. Tích kiểm hoạt động tự trị của AI Agent v1.0
		agent = DreamForgeAIAgent(db)
		final_movie_path = agent.execute_autonomous_production_lifecycle(story_text)
		
		print("\n============ KẾT QUẢ NGHIỆM THU REASONING AGENT (VERSION 1.0) ============")
		print(f" 🎬 File phim thành phẩm được xuất bản tự trị:\n \"{final_movie_path}\"")
		print("==========================================================================")

		# Khẳng định kiểm duyệt chất lượng tệp tin đầu ra của Agent
		self.assertTrue(final_movie_path.endswith(".mp4"))

		# 2. Tích kiểm nút gộp Production Scheduler mốc 28%
		scheduler = ProductionScheduler(db)
		report = scheduler.schedule_episode_production_matrix("ToanDanTaoPhong", 15, [story_text])
		
		self.assertEqual(report["production_hud_progress"], "28%")
		self.assertIn("thumbnail_node", report)
		
		db.close()


if __name__ == "__main__":
	unittest.main()
