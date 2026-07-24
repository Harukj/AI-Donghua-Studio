from sqlalchemy.orm import Session
from database.repositories.character_repository import CharacterRepository
from core.logger import studio_logger

class CharacterService:
	def __init__(self, db_session: Session):
		"""Khởi tạo lớp dịch vụ quản lý nhân vật, tiêm kho lưu trữ Repository"""
		self.repo = CharacterRepository(db_session)

	def save_new_character_profile(self, data: dict, project_id: str = "ToanDanTaoPhong"):
		"""[CREATE PROFILE] Nhận dữ liệu phân rã từ GUI và ủy quyền lưu xuống SQLite"""
		return self.repo.create({
			"project_id": project_id,
			"name": data.get("Tên", "Nhân vật mới"),
			"alias": data.get("Biệt danh", ""),
			"gender": data.get("Giới tính", "Nam"),
			"hair": data.get("Tóc", "black hair"),
			"face": data.get("Khuôn mặt", "handsome face"),
			"body": data.get("Thân hình", "athletic body"),
			"eyes": data.get("Ánh mắt", "sharp eyes"),
			"costume": data.get("Trang phục", "academy uniform"),
			"accessories": data.get("Phụ kiện", "none"),
			"seed": data.get("Mã Seed", "23561"),
			"image_path": data.get("Ảnh đại diện", "")
		})

	def get_fixed_character_prompt_tags(self, character_name: str) -> str:
		"""
		[PROMPT BUILDER CONCATENATION]
		Thuật toán tự động gộp nối cơ học bộ 6 thuộc tính thành phần của nhân vật.
		Triệt tiêu hoàn toàn ô lưu prompt thô, đảm bảo tính nhất quán 100% giữa các tập phim.
		"""
		character = self.repo.find_by_name(character_name)
		if not character:
			return f"character {character_name}"

		# Lắp ghép tuần tự theo đúng sơ đồ khối từ trên xuống dưới của ChatGPT trên hình ảnh
		components_matrix = [
			f"character {character.name}",
			character.hair,
			character.face,
			character.body,
			character.eyes,
			character.costume
		]
		
		# Nếu nhân vật có mang theo vũ khí hoặc phụ kiện kịch bản
		if character.accessories and "none" not in character.accessories.lower():
			components_matrix.append(f"holding {character.accessories.lower()}")

		# Lọc bỏ khoảng trống thừa và kết chuỗi sạch cách nhau bằng dấu phẩy
		final_profile_prompt = ", ".join([tags.strip().lower() for tags in components_matrix if tags])
		
		studio_logger.logger.info(f"DreamForge Core: Đã tự động sinh Prompt chân dung cơ học cho [{character_name}]")
		return final_prompt_profile_prompt if 'final_prompt_profile_prompt' in locals() else final_profile_prompt