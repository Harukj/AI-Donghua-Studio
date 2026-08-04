from sqlalchemy.orm import Session
from src.database.repositories.character_repository import CharacterRepository

class CharacterService:
	def __init__(self, db_session: Session):
		"""Khởi tạo Service Layer kết nối thông qua CharacterRepository chuyên trách"""
		self.repo = CharacterRepository(db_session)

	def create_character(self, character_data: dict):
		"""[Create Character] Ủy quyền cho Repository thêm bản ghi mới"""
		return self.repo.create({
			"name": character_data.get("Tên"),
			"alias": character_data.get("Biệt danh"),
			"gender": character_data.get("Giới tính"),
			"age": character_data.get("Tuổi"),
			"height": character_data.get("Chiều cao"),
			"weight": character_data.get("Cân nặng"),
			"hair": character_data.get("Tóc"),
			"eyes": character_data.get("Mắt"),
			"face": character_data.get("Khuôn mặt"),
			"skin": character_data.get("Màu da"),
			"costume": character_data.get("Trang phục"),
			"weapon": character_data.get("Vũ khí"),
			"personality": character_data.get("Tính cách"),
			"voice": character_data.get("Giọng nói"),
			"style": character_data.get("Style"),
			"positive_prompt": character_data.get("Positive Prompt"),
			"negative_prompt": character_data.get("Negative Prompt"),
			"seed": character_data.get("Mã Seed"),
			"image": character_data.get("Ảnh đại diện"),
			"notes": character_data.get("Ghi chú")
		})

	def load_character(self, character_name: str):
		"""[Load Character] Ủy quyền tìm kiếm theo tên"""
		return self.repo.find_by_name(character_name)

	def update_character(self, character_name: str, new_data: dict):
		"""[Update Character / Save Character] Thực thi lưu cập nhật thông tin"""
		character = self.load_character(character_name)
		if character:
			character.name = new_data.get("Tên", character.name)
			character.alias = new_data.get("Biệt danh", character.alias)
			character.gender = new_data.get("Giới tính", character.gender)
			character.age = new_data.get("Tuổi", character.age)
			character.height = new_data.get("Chiều cao", character.height)
			character.weight = new_data.get("Cân nặng", character.weight)
			character.hair = new_data.get("Tóc", character.hair)
			character.eyes = new_data.get("Mắt", character.eyes)
			character.face = new_data.get("Khuôn mặt", character.face)
			character.skin = new_data.get("Màu da", character.skin)
			character.costume = new_data.get("Trang phục", character.costume)
			character.weapon = new_data.get("Vũ khí", character.weapon)
			character.personality = new_data.get("Tính cách", character.personality)
			character.voice = new_data.get("Giọng nói", character.voice)
			character.style = new_data.get("Style", character.style)
			character.positive_prompt = new_data.get("Positive Prompt", character.positive_prompt)
			character.negative_prompt = new_data.get("Negative Prompt", character.negative_prompt)
			character.seed = new_data.get("Mã Seed", character.seed)
			character.image = new_data.get("Ảnh đại diện", character.image)
			character.notes = new_data.get("Ghi chú", character.notes)
			
			self.repo.db.commit()
		return character

	def delete_character(self, character_name: str) -> bool:
		"""[Delete Character] Xóa hồ sơ nhân vật thông qua ID nhận diện"""
		character = self.load_character(character_name)
		if character:
			return self.repo.delete(character.id)
		return False

	def search_character(self, keyword: str) -> list:
		"""[Search Character] Gọi hàm tìm kiếm từ khóa nâng cao của Repository"""
		return self.repo.search_by_keyword(keyword)
		
	def get_all_characters(self) -> list:
		"""Lấy toàn bộ danh sách nhân vật đưa lên UI"""
		return self.repo.get_all()

	def build_ai_prompt(self, character_name: str) -> str:
		"""[PROMPT BUILDER LOGIC] Lắp ráp prompt giữ nguyên tính nhất quán"""
		character = self.load_character(character_name)
		if not character:
			return ""
		prompt_parts = [f"Character: {character.name}"]
		if character.age and character.gender:
			prompt_parts.append(f"{character.age}-year-old {character.gender.lower()}")
		if character.hair: prompt_parts.append(f"{character.hair.lower()} hair")
		if character.eyes: prompt_parts.append(f"{character.eyes.lower()} eyes")
		if character.costume: prompt_parts.append(character.costume)
		if character.style: prompt_parts.append(character.style)
		prompt_parts.extend(["masterpiece", "cinematic lighting", "anime"])
		return ", ".join([part.strip() for part in prompt_parts if part])
