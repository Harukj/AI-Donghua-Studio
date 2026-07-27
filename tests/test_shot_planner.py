import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.scene_splitter.shot_planner import ShotPlanner

class TestShotPlannerv08(unittest.TestCase):
	def test_automated_4_shots_segmentation(self):
		"""Ca kiểm thử tích hợp: Xác thực bộ chia cú máy xuất ra đúng bộ 4 Shots kèm mốc thời gian của ChatGPT"""
		scene_content = "Tô Mộc bước vào học viện."
		
		planner = ShotPlanner(scene_id=701)
		output_shots = planner.generate_shot_plan_matrix(scene_content)
		
		print("\n============ KẾT QUẢ NGHIỆM THU SPRINT 11 - SHOT PLANNER V0.8 ============")
		for shot in output_shots:
			print(f"🎬 [Shot ID: {shot.id}] Index: {shot.index} | Ngữ cảnh: {shot.context_type.upper()}")
			print(f"   Thời lượng kết xuất: {shot.duration} giây | Khung hình: {shot.camera} ({shot.movement})")
		print("==========================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng
		self.assertEqual(len(output_shots), 4)
		self.assertEqual(output_shots[0].duration, 5.0) # Shot 1 bắt buộc phải dài 5 giây
		self.assertEqual(output_shots[2].context_type, "reaction") # Shot 3 bắt buộc phải là reaction
		self.assertEqual(output_shots[3].duration, 3.0) # Shot 4 bắt buộc phải dài 3 giây

if __name__ == "__main__":
	unittest.main()
