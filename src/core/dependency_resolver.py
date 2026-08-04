from sqlalchemy.orm import Session
from src.database.models.character import CharacterModel
from src.database.repositories.component_repository import AssetComponentRepository
from src.core.logger import studio_logger

class AssetDependencyResolver:
	def __init__(self, db_session: Session):
		self.db = db_session
		self.component_repo = AssetComponentRepository(db_session)

	def resolve_character_dependencies(self, character_name: str) -> dict:
		"""
		[DREAMFORGE ENGINE - ASSET COMPONENT MIXER]
		Tự động quét cấu trúc bảng asset_components để trích xuất prompt bộ phận ngoại hình.
		Ép luồng cập nhật tự động toàn bộ mạch phim khi chỉnh sửa một thuộc tính duy nhất.
		"""
		studio_logger.logger.info(f"[DREAMFORGE CORE] Đang phân rã ma trận thuộc tính cho: '{character_name}'...")

		character = self.db.query(CharacterModel).filter(CharacterModel.name == character_name).first()
		
		resolved_data = {
			"character_name": character_name,
			"seed": "23561",
			"description_tags": f"character {character_name}"
		}

		if character:
			# Lấy danh sách toàn bộ bộ phận (Tóc, Mặt, Quần áo...) của nhân vật này trong DB
			components = self.component_repo.get_components_by_asset(character.id)
			
			if components:
				# Trích xuất và trộn cơ học chuỗi prompt của toàn bộ các bộ phận đang lưu cứng trong DB
				prompt_tags_list = [f"character {character_name}"]
				for comp in components:
					if comp.prompt:
						prompt_tags_list.append(comp.prompt.lower())
						
				resolved_data["description_tags"] = ", ".join(prompt_tags_list)
				# Lấy mã seed đóng băng từ thành phần đầu tiên tìm thấy
				resolved_data["seed"] = components[0].seed or "23561"
			else:
				# Khung dữ liệu dự phòng an toàn nếu nghệ sĩ chưa phân rã bộ phận trong DB
				resolved_data["description_tags"] = f"character {character_name}, detailed 3d features"
				resolved_data["seed"] = getattr(character, 'seed', "23561") or "23561"

		studio_logger.logger.info(f" -> [AUTO COMPONENT SYNC]: \"{resolved_data['description_tags']}\"")
		return resolved_data