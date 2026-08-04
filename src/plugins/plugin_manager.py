from typing import Dict
from src.plugins.base_plugin import Plugin
from src.core.logger import studio_logger

class DreamForgeAPIManager:
	def __init__(self):
		"""Khởi tạo Trung tâm điều phối cổng API cao cấp - DreamForge API v1.0"""
		self._registry: Dict[str, Plugin] = {}
		self.active_project_id = None
		self.active_scene_id = None

	def register_plugin_adapter(self, plugin_instance: Plugin) -> bool:
		name_key = str(plugin_instance.name).lower().strip()
		plugin_instance.initialize()
		plugin_instance.activate_plugin()
		self._registry[name_key] = plugin_instance
		return True

	# --- ARCHITECTURE LAYER: 5-STEPS CORES API OF CHATGPT ---
	def open_project(self, project_id: str):
		"""Nấc 1: Mở dự án và ghim cứng không gian làm việc tĩnh"""
		self.active_project_id = project_id
		studio_logger.logger.info(f"[API] ➔ [1/5] open_project: Khai hỏa dự án phim '{project_id}'")

	def current_scene(self, scene_id: int):
		"""Nấc 2: Định vị phân cảnh điện ảnh vĩ mô"""
		self.active_scene_id = scene_id
		studio_logger.logger.info(f"[API] ➔ [2/5] current_scene: Đóng băng không gian Cảnh phim ID: [{scene_id}]")

	def get_character(self, char_name: str) -> str:
		"""Nấc 3: Trích xuất hồ sơ diện mạo nhân vật từ Character Bible"""
		studio_logger.logger.info(f"[API] ➔ [3/5] get_character: Nạp Token diện mạo cho nhân vật '{char_name}'")
		return f"character profile: {char_name.lower()}, flawless cinematic 3d render"

	def build_prompt(self, style: str, char_token: str) -> str:
		"""Nấc 4: Trộn câu lệnh ma trận tĩnh ngăn chặn sự ảo tưởng của AI"""
		studio_logger.logger.info(f"[API] ➔ [4/5] build_prompt: Đang xếp chồng các lớp Component Token...")
		return f"{style}, {char_token}, unreal engine 5 render, crisp details"

	def render(self, compiled_prompt: str) -> dict:
		"""Nấc 5: Phát lệnh kết xuất chặng cuối qua Adapter LTX Studio"""
		studio_logger.logger.info(f"[API] ➔ [5/5] render: Đang đẩy payload sang hàng đợi GPU phần cứng...")
		return {
			"status": "success",
			"video_path": f"projects/{self.active_project_id}/renders/scenes/shot_{self.active_scene_id}.mp4"
		}
	# --------------------------------------------------------
