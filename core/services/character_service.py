from sqlalchemy.orm import Session
from database.models.character import CharacterModel

class CharacterService:
    def __init__(self, db_session: Session):
        """Khởi tạo service với một phiên kết nối Database (Session)"""
        self.db = db_session

    def add_character(self, character_data: dict) -> CharacterModel:
        """Thêm một nhân vật mới vào Cơ sở dữ liệu SQLite"""
        db_character = CharacterModel(
            name=character_data.get("Tên"),
            gender=character_data.get("Giới tính"),
            age=character_data.get("Tuổi"),
            hair=character_data.get("Tóc"),
            eyes=character_data.get("Mắt"),
            clothes=character_data.get("Trang phục"),
            personality=character_data.get("Tính cách"),
            style=character_data.get("Prompt Style", "Chinese Donghua style"),
            negative_prompt=character_data.get("Negative Prompt"),
            notes=character_data.get("Ghi chú")
        )
        self.db.add(db_character)
        self.db.commit()
        self.db.refresh(db_character)
        return db_character

    def get_character_by_name(self, name: str) -> CharacterModel:
        """Truy vấn hồ sơ nhân vật từ Database dựa trên tên gọi"""
        return self.db.query(CharacterModel).filter(CharacterModel.name == name).first()

    def build_ai_prompt(self, character_name: str) -> str:
        """
        [PROMPT BUILDER LOGIC]
        Tự động truy vấn thuộc tính thô và lắp ghép thành chuỗi Prompt AI hoàn chỉnh
        """
        character = self.get_character_by_name(character_name)
        if not character:
            return f"Character '{character_name}' not found."

        # Tạo mảng danh sách chứa các thuộc tính thô để nối chuỗi (như thiết kế của ChatGPT)
        prompt_parts = []
        
        if character.name:
            prompt_parts.append(f"Character: {character.name}")
        if character.age and character.gender:
            prompt_parts.append(f"{character.age}-year-old {character.gender.lower()}")
        elif character.gender:
            prompt_parts.append(character.gender)
            
        if character.hair:
            prompt_parts.append(f"{character.hair.lower()} hair")
        if character.eyes:
            prompt_parts.append(f"{character.eyes.lower()} eyes")
        if character.clothes:
            prompt_parts.append(character.clothes)
        if character.personality:
            prompt_parts.append(f"{character.personality.lower()} expression")
        if character.style:
            prompt_parts.append(character.style)
            
        # Thêm các thẻ bổ trợ chất lượng mặc định cho AI Art
        prompt_parts.extend(["masterpiece", "cinematic lighting", "anime"])

        # Nối tất cả lại bằng dấu phẩy để ra đoạn prompt hoàn chỉnh cho AI tạo ảnh
        full_prompt = ", ".join([part.strip() for part in prompt_parts if part])
        return full_prompt
