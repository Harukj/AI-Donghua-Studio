import os
from core.logger import studio_logger

class SceneIntelligence:
	def __init__(self):
		"""Khởi tạo cỗ máy trí tuệ phân cảnh - Scene Intelligence Engine v0.8"""
		pass

	def parse_cinematic_yaml_directives(self, yaml_data: dict) -> dict:
		"""
		[SCENE INTELLIGENCE PIPELINE v0.8]
		Bóc tách 100% cấu trúc file YAML của ChatGPT bao gồm:
		Title, Characters, Environment, Action, Emotion, Suggested Camera.
		"""
		studio_logger.logger.info("[SCENE INTEL] Đang phân rã gói dữ liệu cấu trúc YAML của Đạo diễn AI...")
		
		# Trích xuất an toàn các trường thông tin theo đúng sơ đồ khối trên trình duyệt
		title = yaml_data.get("Scene", {}).get("title", "Gặp nhau tại học viện")
		characters = yaml_data.get("Characters", [])
		environment = yaml_data.get("Environment", "Học viện Long Dạng")
		actions = yaml_data.get("Action", [])
		emotions = yaml_data.get("Emotion", [])
		suggested_cameras = yaml_data.get("Suggested_camera", [])

		studio_logger.logger.info(f" -> [✓] Tiêu đề cảnh: {title}")
		studio_logger.logger.info(f" -> [✓] Trạng thái cảm xúc phát hiện: {emotions}")
		studio_logger.logger.info(f" -> [✓] Danh sách góc máy chỉ định: {suggested_cameras}")

		# Đóng gói dữ liệu cấu trúc phức hợp trả về cho hệ thống Shot Planner tiếp quản
		return {
			"scene_title": title,
			"characters_list": characters,
			"environment_name": environment,
			"action_tags": ", ".join(actions),
			"emotion_tags": ", ".join(emotions),
			"cameras_list": suggested_cameras
		}
