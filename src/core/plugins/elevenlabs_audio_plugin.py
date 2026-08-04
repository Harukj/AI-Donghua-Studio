from src.core.plugins.base_plugin import BasePlugin
from src.core.logger import studio_logger

class ElevenLabsAudioPlugin(BasePlugin):
	def get_plugin_name(self) -> str:
		return "ElevenLabs_Audio_Voice_Generator"

	def execute(self, data: dict) -> dict:
		"""Nhận dữ liệu lời thoại từ Storyboard và giả lập gọi API sinh giọng nói nhân vật .mp3"""
		dialogue = data.get("dialogue", "Không có thoại")
		speaker = data.get("speaker", "Quần chúng")
		scene_id = data.get("scene_id", "UNKNOWN")
		
		studio_logger.logger.info(f"[PLUGIN AUDIO] Đang chuyển đổi văn bản thoại của nhân vật [{speaker}] sang giọng nói AI...")
		
		return {
			"status": "SUCCESS",
			"audio_file_path": f"projects/assets/audio/{scene_id.lower()}_voice.mp3"
		}
