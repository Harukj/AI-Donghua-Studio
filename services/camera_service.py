from sqlalchemy.orm import Session
from database.repositories.camera_repository import CameraRepository
from core.logger import studio_logger

class CameraService:
	def __init__(self, db_session: Session):
		"""Khởi tạo dịch vụ quản lý góc máy ảo, tiêm kho lưu trữ chuyên trách"""
		self.repo = CameraRepository(db_session)

	def get_fixed_camera_prompt_tags(self, preset_name: str) -> str:
		"""
		[CAMERA BUILDER AUTOMATION]
		Đọc trực tiếp bộ 5 thuộc tính phân rã từ cơ sở dữ liệu.
		Nối chuỗi tĩnh (Static Concat) cơ học tuyệt đối để bảo vệ tính nhất quán cho khung hình phim AI.
		"""
		camera = self.repo.find_by_preset_name(preset_name)
		
		# Khung từ khóa góc máy mẫu lấy chính xác 100% từ hình ảnh của ChatGPT nếu preset chưa được cấu hình
		if not camera:
			return "wide shot, shot on 24mm lens, eye level height, slow push camera movement, rule of thirds composition"

		# Lắp ghép tuần tự bộ 5 phân lớp thông tin máy quay ảo theo đúng đặc tả của Đạo diễn AI
		camera_matrix = [
			camera.shot_type,
			f"shot on {camera.lens} lens" if camera.lens else "",
			f"{camera.height.lower()} height" if camera.height else "",
			f"{camera.movement.lower()} camera movement" if camera.movement else "",
			f"{camera.composition.lower()} composition" if camera.composition else ""
		]

		# Lọc sạch các khoảng trống thừa và kết chuỗi sạch cách nhau bằng dấu phẩy
		final_camera_prompt = ", ".join([tags.strip() for tags in camera_matrix if tags])
		
		studio_logger.logger.info(f"DreamForge Core: Đã tự động sinh Prompt góc máy cơ học cho preset [{preset_name}]")
		return final_camera_prompt
