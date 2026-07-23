from sqlalchemy.orm import Session
from database.models.environment import EnvironmentModel

class EnvironmentService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add_environment(self, env_data: dict) -> EnvironmentModel:
        """Thêm một bối cảnh mới vào SQLite"""
        db_env = EnvironmentModel(
            name=env_data.get("name"),
            time_of_day=env_data.get("time_of_day"),
            weather=env_data.get("weather"),
            architecture_style=env_data.get("architecture_style"),
            description_prompt=env_data.get("description_prompt"),
            style=env_data.get("style", "Chinese Donghua style"),
            negative_prompt=env_data.get("negative_prompt")
        )
        self.db.add(db_env)
        self.db.commit()
        self.db.refresh(db_env)
        return db_env

    def get_env_by_name(self, name: str) -> EnvironmentModel:
        """Truy vấn bối cảnh bằng tên"""
        return self.db.query(EnvironmentModel).filter(EnvironmentModel.name == name).first()

    def build_environment_prompt(self, env_name: str) -> str:
        """[Prompt Builder] Tự động dựng chuỗi prompt bối cảnh cho AI"""
        env = self.get_env_by_name(env_name)
        if not env:
            return f"Environment '{env_name}' not found."

        prompt_parts = []
        if env.name:
            prompt_parts.append(env.name)
        if env.architecture_style:
            prompt_parts.append(env.architecture_style)
        if env.time_of_day:
            prompt_parts.append(f"during {env.time_of_day.lower()}")
        if env.weather:
            prompt_parts.append(f"{env.weather.lower()} weather")
        if env.description_prompt:
            prompt_parts.append(env.description_prompt)
        if env.style:
            prompt_parts.append(env.style)

        prompt_parts.extend(["masterpiece", "ultra detailed", "8k resolution"])
        return ", ".join([part.strip() for part in prompt_parts if part])
