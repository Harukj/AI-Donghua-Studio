import os
import json
from sqlalchemy.orm import Session
from database.models.episode import EpisodeModel
from database.models.shot import ShotModel
from core.logger import studio_logger

class EpisodePackageGenerator:
	def __init__(self, db_session: Session):
		"""Khởi tạo cỗ máy đóng gói tập phim đa tầng - DreamForge Engine v1.0"""
		self.db = db_session

	def generate_six_layers_package(self, episode_id: int, project_id: str) -> dict:
		"""
		[EPISODE PACKAGE GENERATOR CORE]
		Tự động đóng băng cấu trúc dữ liệu và xuất bản cây thư mục 6 lớp theo đúng đặc tả của ChatGPT.
		"""
		# 1. Truy vấn thông tin Tập phim từ SQLite Production Database
		episode = self.db.query(EpisodeModel).filter(EpisodeModel.id == episode_id).first()
		if not episode:
			raise ValueError(f"Không tìm thấy Tập phim ID [{episode_id}] trong hệ thống Database!")

		# Định vị đường dẫn thư mục gốc đóng gói bám sát ảnh chụp ChatGPT
		package_root_dir = os.path.join("projects", project_id, f"Episode_{episode.episode_number}")
		
		# 2. Khai hỏa khởi tạo đồng loạt các phân khu thư mục con vật lý
		sub_layers = ["scenes", "shots", "prompts", "assets", "metadata"]
		for layer in sub_layers:
			os.makedirs(os.path.join(package_root_dir, layer), exist_ok=True)

		# 3. Thu thập danh sách toàn bộ các cú máy (Shots) đối ứng
		shots_list = self.db.query(ShotModel).filter(ShotModel.scene_id == episode_id).all()
		
		# 4. Xuất bản tệp tin hạt nhân đầu não: episode.json
		episode_master_data = {
			"episode_id": episode.id,
			"project_id": project_id,
			"episode_number": episode.episode_number,
			"title": episode.title,
			"summary": episode.summary,
			"total_shots": len(shots_list),
			"compiled_metadata": {
				"software_version": "DreamForge Engine v1.0.0",
				"pipeline_status": "package_locked"
			}
		}
		
		master_json_path = os.path.join(package_root_dir, "episode.json")
		with open(master_json_path, "w", encoding="utf-8") as f:
			json.dump(episode_master_data, f, indent=4, ensure_ascii=False)

		# 5. Đóng băng dữ liệu Prompts và cú máy con xuống các phân khu tương ứng
		for shot in shots_list:
			# Xuất bản file prompt ma trận tĩnh ngăn chặn sự ảo tưởng của AI
			prompt_file_path = os.path.join(package_root_dir, "prompts", f"shot_{shot.index}_prompt.txt")
			with open(prompt_file_path, "w", encoding="utf-8") as f:
				f.write(str(shot.prompt))

		studio_logger.logger.info(f"[PACKAGE SUCCESS] ➔ Đóng gói thành công Tập {episode.episode_number} vào: {package_root_dir}")
		
		return {
			"status": "success",
			"package_path": package_root_dir,
			"master_json": master_json_path
		}
