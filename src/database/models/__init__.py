# Mở file src/database/models/__init__.py và dán đè toàn bộ bằng nội dung sạch này:

from .episode import EpisodeModel
from .shot import ShotModel
from .asset_component import AssetComponentModel
from .environment import EnvironmentModel
from .asset import AssetModel
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
