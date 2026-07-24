from sqlalchemy.orm import Session
from database.models.character import CharacterModel
from database.models.asset import AssetModel
from database.models.audio import AudioModel
from core.logger import studio_logger

class AssetDependencyResolver:
	def __init__(self, db_session: Session):
		"""Khởi tạo bộ giải quyết phụ thuộc tài nguyên kết nối SQLite"""
		self.db = db_session

	def resolve_character_dependencies(self, character_name: str) -> dict:
		"""
		[UNREAL ENGINE STYLE ASSET DEPENDENCY RESOLVER]
		Tự động quét hệ thống để trích xuất cây phụ thuộc đóng băng của nhân vật.
		Triệt tiêu hoàn toàn việc so khớp chuỗi lỏng lẻo, bảo vệ tính nhất quán v1.0.
		"""
		studio_logger.logger.info(f"[DREAMFORGE CORE] Đang trích xuất cây phụ thuộc cho nhân vật: '{character_name}'...")

		# 1. Truy vấn lấy hồ sơ gốc của nhân vật trong Character Bible
		character = self.db.query(CharacterModel).filter(CharacterModel.name == character_name).first()
		
		# Khởi tạo bộ khung dữ liệu mặc định an toàn nếu nhân vật mới chưa cấu hình đầy đủ trong thư viện
		dependency_tree = {
			"character_name": character_name,
			"seed": "23561", # Mã hạt giống cố định mặc định
			"portrait_path": f"projects/assets/characters/default.png",
			"voice_path": f"projects/assets/audio/default_voice.mp3",
			"assigned_props": []
		}

		if character:
			# Nạp mã Seed ghim cố định từ hồ sơ nhân vật
			dependency_tree["seed"] = getattr(character, 'seed', "23561") or "23561"
			
			# 2. TỰ ĐỘNG TRUY VẾT LINK SANG BẢNG ASSETS TRUNG TÂM (Ảnh chân dung)
			if hasattr(character, 'asset_id') and character.asset_id:
				asset = self.db.query(AssetModel).filter(AssetModel.id == character.asset_id).first()
				if asset: dependency_tree["portrait_path"] = asset.path
			else:
				dependency_tree["portrait_path"] = f"projects/ToanDanTaoPhong/assets/characters/{character_name.lower()}.png"

			# 3. TỰ ĐỘNG TRUY VẾT LINK SANG BẢNG AUDIOS (Giọng đọc lồng tiếng AI)
			if hasattr(character, 'voice_id') and character.voice_id:
				audio = self.db.query(AudioModel).filter(AudioModel.id == character.voice_id).first()
				if audio: dependency_tree["voice_path"] = audio.audio_path

			# 4. TỰ ĐỘNG TRUY VẾT VŨ KHÍ (Props) ĐANG ĐƯỢC GẮN TRÊN NHÂN VẬT
			if getattr(character, 'weapon', None):
				dependency_tree["assigned_props"].append(character.weapon)

		studio_logger.logger.info(f" -> Đóng gói cây phụ thuộc thành công cho [{character_name}]: Seed={dependency_tree['seed']}, Props={dependency_tree['assigned_props']}")
		return dependency_tree