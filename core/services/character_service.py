from sqlalchemy.orm import Session
from database.models.character import CharacterModel

class CharacterService:
    def __init__(self, db_session: Session):
        """Khởi tạo service nhận vào một Session kết nối Database"""
        self.db = db_session

    def create_character(self, character_data: dict) -> CharacterModel:
        """[Create Character] Thêm một nhân vật mới vào hệ thống dữ liệu"""
        db_character = CharacterModel(
            name=character_data.get("Tên"),
            alias=character_data.get("Biệt danh"),
            gender=character_data.get("Giới tính"),
            age=character_data.get("Tuổi"),
            height=character_data.get("Chiều cao"),
            weight=character_data.get("Cân nặng"),
            hair=character_data.get("Tóc"),
            eyes=character_data.get("Mắt"),
            face=character_data.get("Khuôn mặt"),
            skin=character_data.get("Màu da"),
            costume=character_data.get("Trang phục"),
            weapon=character_data.get("Vũ khí"),
            personality=character_data.get("Tính cách"),
            voice=character_data.get("Giọng nói"),
            style=character_data.get("Style"),
            positive_prompt=character_data.get("Positive Prompt"),
            negative_prompt=character_data.get("Negative Prompt"),
            notes=character_data.get("Ghi chú"),
            seed=character_data.get("Mã Seed"),
            image=character_data.get("Ảnh đại diện")
        )
        self.db.add(db_character)
        self.db.commit()
        self.db.refresh(db_character)
        return db_character

    def load_character(self, character_name: str) -> CharacterModel:
        """[Load Character] Tải thông tin hồ sơ của một nhân vật cụ thể theo tên"""
        return self.db.query(CharacterModel).filter(CharacterModel.name == character_name).first()

    def update_character(self, character_name: str, new_data: dict) -> CharacterModel:
        """[Update Character / Save Character] Cập nhật và lưu lại dữ liệu thay đổi của nhân vật"""
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
            
            self.db.commit()
            self.db.refresh(character)
        return character

    def delete_character(self, character_name: str) -> bool:
        """[Delete Character] Xóa hoàn toàn một hồ sơ nhân vật khỏi SQLite"""
        character = self.load_character(character_name)
        if character:
            self.db.delete(character)
            self.db.commit()
            return True
        return False

    def search_character(self, keyword: str) -> list[CharacterModel]:
        """[Search Character] Tìm kiếm nhân vật theo từ khóa gần đúng (Tên hoặc Biệt danh)"""
        return self.db.query(CharacterModel).filter(
            (CharacterModel.name.like(f"%{keyword}%")) | 
            (CharacterModel.alias.like(f"%{keyword}%"))
        ).all()
        
    def get_all_characters(self) -> list[CharacterModel]:
        """Lấy toàn bộ danh sách để tải lên danh mục UI lề trái"""
        return self.db.query(CharacterModel).all()
