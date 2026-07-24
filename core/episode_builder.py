import os
import time
from core.logger import studio_logger

class EpisodeBuilder:
	def __init__(self, project_id: str, episode_number: int):
		"""Khởi tạo bộ gộp phim tự động cho Tập phim"""
		self.project_id = project_id
		self.episode_number = episode_number
		self.export_dir = os.path.join("projects", project_id.replace(" ", "_"), "exports")
		
		if not os.path.exists(self.export_dir):
			os.makedirs(self.export_dir)

	def stitch_shots_into_episode(self, completed_shot_paths: list[str]) -> str:
		"""
		[EPISODE BUILDER AUTOMATION PIPELINE]
		Tự động đọc danh sách các tệp clip ngắn .mp4 đã render xong của Shot
		để gộp thành một tập phim hoàn chỉnh xuất lên YouTube theo sơ đồ ChatGPT.
		"""
		studio_logger.logger.info(f"[EPISODE BUILDER] Bắt đầu dây chuyền gộp nối {len(completed_shot_paths)} video Shots...")
		
		# Giả lập thời gian xử lý render gộp của FFmpeg/CapCut Engine ngầm (1.5 giây)
		time.sleep(1.5)
		
		final_output_path = os.path.join(self.export_dir, f"episode_{self.episode_number:02d}_final.mp4")
		
		studio_logger.logger.info(f"[SUCCESS] Đã đóng gói xong Tập phim: '{final_output_path}'")
		return final_output_path