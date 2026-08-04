from sqlalchemy.orm import Session
from src.database.repositories.environment_repository import EnvironmentRepository
from src.core.logger import studio_logger

class EnvironmentService:
	def __init__(self, db_session: Session):
		"""Khởi tạo dịch vụ quản lý bối cảnh, tiêm kho lưu trữ chuyên trách v1.0"""
		self.repo = EnvironmentRepository(db_session)

	def get_fixed_environment_prompt_tags(self, location_name: str) -> str:
		"""
		[ENVIRONMENT MAATRIX CONCATENATION]
		Thuật toán tự động gộp nối cơ học bộ 5 thuộc tính thành phần của bối cảnh.
		Triệt tiêu hoàn toàn ô nhập prompt tự do để bảo vệ tính nhất quán không gian phim.
		"""
		env = self.repo.find_by_name(location_name)
		
		# Khung từ khóa mẫu lấy chính xác 100% từ hình ảnh của ChatGPT nếu địa danh mới chưa cấu hình
		if not env:
			return "scene setting at long dang academy, chinese fantasy academy architecture, morning lighting, sunny weather, epic atmosphere"

		# Lắp ghép tuần tự từ trên xuống dưới theo sơ đồ khối của ChatGPT
		env_matrix = [
			f"scene setting at {env.environment.lower()}",
			f"{env.architecture.lower()} architecture" if env.architecture else "",
			f"{env.lighting.lower()} lighting" if env.lighting else "",
			f"{env.weather.lower()} weather" if env.weather else "",
			f"{env.atmosphere.lower()} atmosphere" if env.atmosphere else ""
		]

		# Lọc sạch các khoảng trống thừa và nối lại bằng dấu phẩy
		final_env_prompt = ", ".join([tags.strip() for tags in env_matrix if tags])
		
		studio_logger.logger.info(f"DreamForge Core: Đã tự động sinh Prompt bối cảnh cơ học cho địa danh [{location_name}]")
		return final_env_prompt
