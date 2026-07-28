from sqlalchemy.orm import Session
from database.session import SessionLocal

# Import toàn bộ các Service Layer cốt lõi của Studio
from services.character_service import CharacterService
from services.environment_service import EnvironmentService
from core.project_manager import ProjectManager
from core.plugins.plugin_manager import plugin_registry
from core.plugins.ltx_video_plugin import LTXVideoPlugin
from core.plugins.elevenlabs_audio_plugin import ElevenLabsAudioPlugin
plugin_registry.register_plugin(LTXVideoPlugin())
plugin_registry.register_plugin(ElevenLabsAudioPlugin())
class DependencyProvider:
	def __init__(self):
		"""Khởi tạo phiên làm việc kết nối Database dùng chung cho các dịch vụ"""
		self.db: Session = SessionLocal()
		
		# Khởi tạo tập trung các Service (Dependency Injection Boilerplate)
		self._character_service = CharacterService(self.db)
		self._environment_service = EnvironmentService(self.db)
		self._project_manager = ProjectManager()

	def get_character_service(self) -> CharacterService:
		"""Cung cấp dịch vụ quản lý nhân vật"""
		return self._character_service

	def get_environment_service(self) -> EnvironmentService:
		"""Cung cấp dịch vụ quản lý bối cảnh"""
		return self._environment_service

	def get_project_manager(self) -> ProjectManager:
		"""Cung cấp dịch vụ quản lý cấu trúc dự án"""
		return self._project_manager

	def close_all(self):
		"""Giải phóng kết nối khi đóng ứng dụng phần mềm"""
		try:
			self.db.close()
		except Exception:
			pass

# Khởi tạo một đối tượng Provider duy nhất cho toàn bộ hệ thống (Singleton Pattern)
ioc_container = DependencyProvider()
