import os
import shutil
from src.core.logger import studio_logger

class VideoAssetManager:
	def __init__(self, project_id: str = "ToanDanTaoPhong"):
		"""Khởi tạo bộ quản lý tài nguyên video tập trung - Video Asset Manager v1.0"""
		self.project_id = project_id.replace(" ", "_")
		# Định vị chính xác bộ khung đường dẫn cây thư mục vật lý theo đặc tả của ChatGPT
		self.base_render_dir = os.path.join("projects", self.project_id, "renders")
		self.scenes_dir = os.path.join(self.base_render_dir, "scenes")
		
		self._initialize_storage_tree()

	def _initialize_storage_tree(self):
		"""Tự động quét và khởi tạo cấu trúc thư mục rỗng chuẩn hóa nếu hệ thống chưa có"""
		if not os.path.exists(self.scenes_dir):
			os.makedirs(self.scenes_dir)
			studio_logger.logger.info(f"[ASSET MANAGER] Khởi tạo thành công cây thư mục lưu trữ: {self.scenes_dir}")

	def register_rendered_shot_clip(self, source_cache_path: str, shot_index: int) -> str:
		"""
		[SHOT CLIP POSITIONING]
		Di chuyển file video clip thô từ bộ nhớ đệm cache tạm thời vào đúng thư mục scenes/ 
		và đổi tên thành định dạng chuẩn hóa thương mại của ChatGPT: Shot01.mp4, Shot02.mp4...
		"""
		if not os.path.exists(source_cache_path):
			raise FileNotFoundError(f"Không tìm thấy file video nguồn tại cache: {source_cache_path}")
			
		filename = f"Shot{shot_index:02d}.mp4" # Ép chuỗi chuẩn hóa thương mại: Shot01.mp4
		destination_path = os.path.join(self.scenes_dir, filename)
		
		# Thực hiện di chuyển file vật lý (hoặc copy đè nếu trùng tên)
		shutil.move(source_cache_path, destination_path)
		studio_logger.logger.info(f"[ASSET MANAGER] Đã đồng bộ cú máy vật lý -> [{destination_path}]")
		return destination_path

	def get_all_ordered_shots(self) -> list[str]:
		"""Quét thư mục hệ thống và trả về danh sách đường dẫn các file Shot đã xếp thứ tự để cấp cho Timeline Engine"""
		try:
			files = os.listdir(self.scenes_dir)
			shot_files = [os.path.join(self.scenes_dir, f) for f in files if f.startswith("Shot") and f.endswith(".mp4")]
			return sorted(shot_files) # Sắp xếp tăng dần Shot01 -> Shot02 -> Shot03
		except Exception as e:
			studio_logger.logger.error(f"Lỗi quét danh mục tệp tin video: {e}")
			return []
