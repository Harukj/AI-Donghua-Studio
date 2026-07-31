# Mở file src/database/models/__init__.py và dán đè toàn bộ bằng nội dung nạp tương đối sạch này:

from .episode import EpisodeModel
from .shot import ShotModel
from .asset_component import AssetComponentModel
from .environment import EnvironmentModel

# Đóng băng danh sách thực thể sản xuất sạch, loại bỏ hoàn toàn các Class mồ côi cũ
__all__ = ["EpisodeModel", "ShotModel", "AssetComponentModel", "EnvironmentModel"]
