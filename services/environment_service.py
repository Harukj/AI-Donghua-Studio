from sqlalchemy.orm import Session
from database.models.environment import EnvironmentModel

class EnvironmentService:
	def __init__(self, db_session: Session):
		self.db = db_session

	def add_environment(self, env_data: dict) -> EnvironmentModel:
		"""Thêm một hồ sơ bối cảnh thương mại mới vào SQLite"""
		db_env = EnvironmentModel(
			name=env_data.get("Tên bối cảnh"),
			category=env_data.get("Danh mục"),
			description=env_data.get("Mô tả bối cảnh"),
			prompt=env_data.get("Prompt"),
			negative_prompt=env_data.get("Negative Prompt"),
			lighting=env_data.get("Ánh sáng"),
			weather=env_data.get("Thời tiết"),
			time_of_day=env_data.get("Thời gian"),
			camera_default=env_data.get("Góc máy"),
			seed=env_data.get("Mã Seed"),
			thumbnail=env_data.get("Ảnh đại diện"),
			notes=env_data.get("Ghi chú")
		)
		self.db.add(db_env)
		self.db.commit()
		self.db.refresh(db_env)
		return db_env

	def get_env_by_name(self, name: str) -> EnvironmentModel:
		"""Truy vấn thực thể bối cảnh dựa theo tên gọi"""
		return self.db.query(EnvironmentModel).filter(EnvironmentModel.name == name).first()

	def build_environment_prompt(self, env_name: str) -> str:
		"""[PROMPT BUILDER ENVIRONMENT] Tự động bóc tách và lắp ráp câu lệnh không gian"""
		env = self.get_env_by_name(env_name)
		if not env:
			return ""

		prompt_parts = []
		if env.name:
			prompt_parts.append(env.name)
		if env.category:
			prompt_parts.append(f"{env.category.lower()}")
		if env.architecture:  # Trường kiến trúc dự phòng nếu có
			prompt_parts.append(env.architecture)
		if env.time_of_day:
			prompt_parts.append(f"during {env.time_of_day.lower()}")
		if env.weather:
			prompt_parts.append(f"{env.weather.lower()} weather")
		if env.lighting:
			prompt_parts.append(f"{env.lighting.lower()} lighting")
		if env.prompt:
			prompt_parts.append(env.prompt)
		if env.style:
			prompt_parts.append(env.style)

		prompt_parts.extend(["masterpiece", "ultra detailed", "8k resolution"])
		return ", ".join([part.strip() for part in prompt_parts if part])
