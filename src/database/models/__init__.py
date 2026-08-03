# Mở file src/database/models/__init__.py và dán đè toàn bộ nội dung sạch này vào:

from .episode import EpisodeModel
from .shot import ShotModel
from .asset_component import AssetComponentModel
from .environment import EnvironmentModel
from .asset import AssetModel  # Khớp chuẩn xác với class AssetModel(Base) ở dòng 5 file asset.py
from .character import CharacterModel
from .dependency import CharacterDependencyModel

# Đóng băng danh sách thực thể sản xuất sạch, triệt tiêu vĩnh viễn các khai báo ma trùng lặp
__all__ = [
	"EpisodeModel", 
	"ShotModel", 
	"AssetComponentModel", 
	"EnvironmentModel", 
	"AssetModel",
	"CharacterModel",
	"CharacterDependencyModel"
]
