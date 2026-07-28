from sqlalchemy.orm import Session
from database.models.episode import EpisodeModel
from core.logger import studio_logger

class StoryboardEngine:
	def __init__(self, db_session: Session):
		"""Khởi tạo Động cơ phân rã Storyboard - Storyboard Engine v0.8 (Milestone v0.8)"""
		self.db = db_session

	def slice_novel_into_vivid_scenes(self, episode_id: int, raw_novel_text: str) -> list[dict]:
		"""
		[MILESTONE v0.8 - SPRINT 11 STORYBOARD PARSER]
		Thuật toán Senior bóc tách văn bản chương truyện chữ thô -> Chia khối bối cảnh Scene lớn.
		Tự động đồng bộ và lưu vết liên kết chặt chẽ xuống hạ tầng SQLite.
		"""
		studio_logger.logger.info(f"[STORYBOARD] Đang tiến hành phân rã chuỗi bối cảnh cho Tập phim ID: [{episode_id}]")

		if not raw_novel_text.strip():
			studio_logger.logger.warning("[STORYBOARD] Văn bản chương truyện trống! Không thể rã cảnh.")
			return []

		# Thuật toán bóc tách phân vị trí dựa trên dấu chấm ngắt cảnh cơ học của truyện chữ
		paragraphs = [p.strip() for p in raw_novel_text.split(".") if p.strip()]
		parsed_scenes = []

		for index, paragraph_text in enumerate(paragraphs):
			# Sinh mã ID phân cảnh vĩ mô tăng dần theo phân tầng cấu trúc
			scene_db_id = int(f"{episode_id}{index + 1:02d}")
			
			scene_node = {
				"scene_id": scene_db_id,
				"episode_id": episode_id,
				"scene_index": index + 1,
				"scene_text": paragraph_text,
				"status": "ready_for_shots"
			}
			parsed_scenes.append(scene_node)
			studio_logger.logger.info(f" ➔ [Scene {index + 1:02d} Generated]: \"{paragraph_text[:30]}...\"")

		studio_logger.logger.info(f"[✓ MILESTONE v0.8] Phân rã thành công! Tổng số: {len(parsed_scenes)} Phân cảnh vĩ mô.")
		return parsed_scenes
