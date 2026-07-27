import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.scene_splitter.shot_planner import ShotPlanner
from ai.prompt_builder.camera_planner import CameraPlanner
from ai.prompt_builder.lighting_planner import LightingPlanner

class TestShotPlannerv08(unittest.TestCase):
	def test_automated_4_shots_segmentation(self):
		scene_content = "Tô Mộc bước vào học viện."
		
		# 1. Kích hoạt bộ bẻ cú máy Shot Planner
		planner = ShotPlanner(scene_id=701)
		output_shots = planner.generate_shot_plan_matrix(scene_content)
		
		# 2. Khởi chạy song hành hai cỗ máy Planner hạt nhân mới theo ảnh mẫu của ChatGPT
		cam_planner = CameraPlanner()
		light_planner = LightingPlanner()
		
		print("\n============ KẾT QUẢ NGHIỆM THU MA TRẬN 3 PLANNER (VERSION 0.8) ============")
		
		# Lấy cú máy số 1 (Shot 1 - Establishing) làm tiêu điểm kiểm tra nghiệm thu
		shot1 = output_shots[0]
		cam_directives = cam_planner.resolve_shot_camera_directives(shot1.context_type)
		light_directives = light_planner.resolve_shot_lighting_directives("morning")
		
		# Tiến hành lắp ráp Mixer cơ học theo đúng bộ khung Token của Studio
		final_token_prompt = (
			f"3D Chinese Donghua style, {cam_directives['camera'].lower()}, shot on {cam_directives['lens']} lens, "
			f"{cam_directives['movement'].lower()}, at {cam_directives['height'].lower()}, "
			f"under {light_directives['type'].lower()} {light_directives['name'].lower()} setup with dynamic {light_directives['fx'].lower()}"
		)
		
		print(f"\n🎬 [Shot 1 Matrix Token Generated]:\n \"{final_token_prompt}\"")
		print("==========================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng dữ liệu
		self.assertEqual(len(output_shots), 4)
		self.assertIn("shot on 24mm lens", final_token_prompt)
		self.assertIn("slow push", final_token_prompt)
		self.assertIn("eye level", final_token_prompt)
		self.assertIn("volumetric morning setup with dynamic sun rays", final_token_prompt)

if __name__ == "__main__":
	unittest.main()
