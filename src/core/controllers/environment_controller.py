from sqlalchemy.orm import Session
from src.services.environment_service import EnvironmentService
# Chèn thêm dòng này vào khu vực import đầu file environment_controller.py:
from database.models.environment import EnvironmentModel 

class EnvironmentController:
	def __init__(self, db_session: Session):
		self.service = EnvironmentService(db_session)

	def handle_create_environment(self, env_data: dict):
		if not env_data.get("name"):
			raise ValueError("Tên bối cảnh không được để trống!")
		return self.service.add_environment(env_data)

	def handle_load_environment(self, name: str):
		return self.service.get_env_by_name(name)

	def handle_save_environment(self, current_name: str, new_data: dict):
		env = self.service.get_env_by_name(current_name)
		if env:
			env.name = new_data.get("Tên bối cảnh", env.name)
			env.time_of_day = new_data.get("Thời gian", env.time_of_day)
			env.weather = new_data.get("Thời tiết", env.weather)
			env.architecture_style = new_data.get("Kiến trúc", env.architecture_style)
			env.description_prompt = new_data.get("Mô tả bối cảnh", env.description_prompt)
			env.style = new_data.get("Style", env.style)
			env.negative_prompt = new_data.get("Negative Prompt", env.negative_prompt)
			self.service.db.commit()
		return env

	def handle_get_all_environments(self):
		return self.service.db.query(self.service.db.query(EnvironmentModel).all())
