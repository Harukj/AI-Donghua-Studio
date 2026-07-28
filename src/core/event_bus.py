from typing import Callable, Dict, List

class EventBus:
	def __init__(self):
		"""Khởi tạo kho chứa các hàm lắng nghe sự kiện (Listeners)"""
		self._listeners: Dict[str, List[Callable]] = {}

	def subscribe(self, event_type: str, callback: Callable):
		"""Các màn hình giao diện (GUI) gọi hàm này để đăng ký lắng nghe một Sự kiện"""
		if event_type not in self._listeners:
			self._listeners[event_type] = []
		self._listeners[event_type].append(callback)
		print(f"EventBus: Màn hình đã đăng ký lắng nghe thành công Sự kiện -> [{event_type}]")

	def publish(self, event_type: str, *args, **kwargs):
		"""Khi có một hành động xảy ra (Ví dụ: bấm Save), gọi hàm này để phát tín hiệu tự động cho các màn hình khác"""
		if event_type in self._listeners:
			print(f"EventBus: [PHÁT TÍN HIỆU SUY KIỆN] -> Đang thông báo cho các bên về sự kiện: '{event_type}'")
			for callback in self._listeners[event_type]:
				try:
					callback(*args, **kwargs) # Kích hoạt tự động hàm làm mới (Refresh) giao diện
				except Exception as e:
					print(f"EventBus Lỗi thực thi callback: {e}")

# Khởi tạo một kênh truyền sự kiện dùng chung duy nhất cho ứng dụng
event_bus = EventBus()
