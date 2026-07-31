# Mở file src/database/models/__init__.py và dán đè toàn bộ bằng nội dung nạp tương đối sạch này:

from .episode import EpisodeModel
from .shot import ShotModel
from .asset_component import AssetComponentModel
from .environment import EnvironmentModel
from .asset import AssetModel
from .character import CharacterModel  # Bảo đảm nạp đúng thực thể nhân vật
from .dependency import CharacterDependencyModel  # TIÊM BỔ SUNG: Nạp tệp phụ thuộc nhân vật

# Đóng băng danh sách thực thể sản xuất sạch
__all__ = [
    "EpisodeModel", 
    "ShotModel", 
    "AssetComponentModel", 
    "EnvironmentModel", 
    "AssetModel",
    "CharacterModel",
    "CharacterDependencyModel"
]
