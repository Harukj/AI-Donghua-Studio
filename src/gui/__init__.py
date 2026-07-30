# Mở file src/gui/__init__.py và dán đè toàn bộ bằng nội dung export sạch này:

from src.gui.main_window import MainWindow
from src.gui.dashboard import Dashboard
from src.gui.sidebar import Sidebar
from src.gui.statusbar import StatusBar
__all__ = ["MainWindow", "Dashboard", "Sidebar", "StatusBar"]
