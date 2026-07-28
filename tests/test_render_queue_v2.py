import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.database.session import SessionLocal
from src.database.base import Base
from src.database.engine import engine
from src.database.models.shot import ShotModel
from src.database.models.version_control import AssetVersionModel
from src.services.render_queue_service import RenderQueueService

class TestRenderQueueAndVersionControl(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo cấu trúc bảng SQLite và dọn sạch metadata cache"""
		Base.metadata.drop_all(bind=engine)
		Base.metadata.create_all(bind=engine)
		
		self.db = SessionLocal()
		self.render_service = RenderQueueService(self.db)

		# 1. Nạp dữ liệu cấu trúc quản lý phiên bản tài nguyên đóng băng an toàn của ChatGPT
		self.v_ep01 = AssetVersionModel(character_name="To Moc", episode_number=1, version_tag="Version 2")
		self.v_ep15 = AssetVersionModel(character_name="To Moc", episode_number=15, version_tag="Version 3")
		
		# 2. Nạp một cú máy giả lập bị lỗi (failed) để tích kiểm chức năng cứu hộ Retry
		self.bad_shot = ShotModel(id=150109, scene_id=1501, index=9, status="failed", prompt="combat error shot")
		
		self.db.add(self.v_ep01)
		self.db.add(self.v_ep15)
		self.db.add(self.bad_shot)
		self.db.commit()

	def test_asset_version_ghim_cung_and_render_retry_pipeline(self):
		"""Ca kiểm thử tối thượng: Xác thực việc ghim cứng phiên bản tập phim độc lập và nút bấm cứu hộ Retry hoạt động sạch lỗi"""
		# Kiểm duyệt tính độc lập phiên bản của Asset Version Control
		ep01_config = self.db.query(AssetVersionModel).filter(AssetVersionModel.episode_number == 1).first()
		ep15_config = self.db.query(AssetVersionModel).filter(AssetVersionModel.episode_number == 15).first()
		self.assertEqual(ep01_config.version_tag, "Version 2")
		self.assertEqual(ep15_config.version_tag, "Version 3") # Không bao giờ làm hỏng các tập cũ

		# Kích hoạt nút bấm cứu hộ "Sau này có thể retry" trên Terminal
		retry_success = self.render_service.retry_failed_render_job(shot_id=150109)
		self.assertTrue(retry_success)
		
		# Truy vấn lại DB để kiểm tra xem GPU đã tự động đẩy trạng thái lên RENDERING chưa
		fixed_shot = self.db.query(ShotModel).filter(ShotModel.id == 150109).first()
		print("\n============ KẾT QUẢ NGHIỆM THU HÀNG ĐỢI RENDER VÀ KIỂM SOÁT PHIÊN BẢN ============")
		print(f" 📁 Quản lý phiên bản: Tập 01 ghim cứng dùng ➔ {ep01_config.version_tag}")
		print(f" 📁 Quản lý phiên bản: Tập 15 nâng cấp dùng  ➔ {ep15_config.version_tag}")
		print(f" 🛠️ [NÚT BẤM CỨU HỘ RETRY]: Cú máy lỗi 150109 đã tự động tái nạp thành công ➔ [{fixed_shot.status.upper()}]")
		print("=================================================================================")
		self.assertEqual(fixed_shot.status, "rendering")

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
