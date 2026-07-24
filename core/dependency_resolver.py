from sqlalchemy.orm import Session
from database.models.character import CharacterModel
from database.models.dependency import CharacterDependencyModel
from core.logger import studio_logger

class AssetDependencyResolver:
	def __init__(self, db_session: Session):
		self.db = db_session

	def resolve_character_dependencies(self, character_name: str) -> dict:
		"""
		[DREAMFORGE CORE - 6 LAYERS DEPENDENCY RESOLVER]
		Quét và tự động đồng bộ hóa bộ 6 thuộc tính phụ thuộc của nhân vật.
		Đảm bảo quy tắc: Sửa 1 thông số trong DB, toàn bộ Prompt tự động cập nhật theo.
		"""
		studio_logger.logger.info(f"[DREAMFORGE ENGINE] Đang giải quyết ma trận phụ thuộc cho: '{character_name}'...")

		# 1. Tìm hồ sơ gốc của nhân vật
		character = self.db.query(CharacterModel).filter(CharacterModel.name == character_name).first()
		
		# Khung xương dữ liệu mô tả nhân vật mặc định
		resolved_data = {
			"character_name": character_name,
			"seed": "23561",
			"description_tags": f"character {character_name}, detailed features",
			"voice": "default_voice"
		}

		if character:
			# 2. Truy vấn lấy ma trận phụ thuộc đóng băng trong bảng character_dependencies
			dep = self.db.query(CharacterDependencyModel).filter(CharacterDependencyModel.character_id == character.id).first()
			
			if dep:
				# Trộn cơ học bộ 5 thuộc tính ngoại hình (hair, face, body, costume, weapon) thành chuỗi tả chân dung cố định
				tags_list = [
					f"character {character_name}",
					dep.hair,
					dep.face,
					dep.body,
					dep.costume
				]
				if dep.weapon and "none" not in dep.weapon.lower():
					tags_list.append(f"holding {dep.weapon.lower()}")
					
				resolved_data["description_tags"] = ", ".join([t.strip() for t in tags_list if t])
				resolved_data["seed"] = dep.locked_seed
				resolved_data["voice"] = dep.voice
			else:
				# Luồng dự phòng nếu nhân vật chưa được cấu hình bảng phụ thuộc chi tiết
				resolved_data["description_tags"] = f"character {character_name}, {getattr(character, 'hair', '')}, {getattr(character, 'costume', '')}"
				resolved_data["seed"] = getattr(character, 'seed', "23561") or "23561"

		studio_logger.logger.info(f" -> [RESOLVED SUCCESS]: Chuỗi chân dung đồng nhất xuất ra: \"{resolved_data['description_tags']}\"")
		return resolved_data