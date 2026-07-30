# Mở file src/database/models/__init__.py và dán đè toàn bộ bằng nội dung nạp tương đối này:

from .episode import EpisodeModel
from .shot import ShotModel
from .asset_component import AssetComponentModel
from .environment import EnvironmentModel

# Đóng băng danh mục thực thể bảo vệ an toàn tuyệt đối cho luồng nạp của SQLAlchemy
__all__ = ["EpisodeModel", "ShotModel", "AssetModel", "EnvironmentModel"]
