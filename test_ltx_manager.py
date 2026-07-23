from ltx.ltx_manager import LTXManager
from analyzer.scene_object import Scene
import time

def gui_status_update(scene_id, status, progress):
	"""Hàm giả lập giao diện GUI nhận tín hiệu thời gian thực từ LTX Manager"""
	if status == "Rendering":
		# Vẽ thanh tiến trình Progress bar thô bằng ký tự trên Terminal giống hệt ảnh mẫu
		bar = "█" * (progress // 10) + "░" * (10 - (progress // 10))
		print(f"[{scene_id}] Trạng thái: {status} |{bar}| {progress}%", end="\r")
	elif status == "Done":
		print(f"\n[{scene_id}] Trạng thái: {status} (Đã hoàn thành sinh phim!)")

def run_test():
	# 1. Khởi tạo bộ quản lý kết xuất LTX
	ltx_studio = LTXManager()
	ltx_studio.set_status_callback(gui_status_update)

	# 2. Tạo nhanh 3 thực thể phân cảnh Object để đưa vào hàng đợi kết xuất
	scene1 = Scene(id="SCENE_01", chapter=1, title="Mở đầu", summary="Tô Mộc bước vào học viện", characters=["Tô Mộc"], environments=["Academy"], props=[], dialogues=[], duration=5.0)
	scene2 = Scene(id="SCENE_02", chapter=1, title="Cao trào", summary="Lâm Uyển gọi lớn Tô Mộc", characters=["Lâm Uyển", "Tô Mộc"], environments=["Long Dang City"], props=[], dialogues=[], duration=5.0)
	
	print("--- HỆ THỐNG RENDERING QUEUE START ---")
	# Đẩy liên tiếp 2 phân cảnh vào xếp hàng xử lý tuần tự
	ltx_studio.add_to_queue(scene1)
	ltx_studio.add_to_queue(scene2)

	# Giữ cho chương trình chính không bị đóng lập tức để luồng ngầm thực thi hoàn tất
	while ltx_studio.is_processing:
		time.sleep(1)

if __name__ == "__main__":
	run_test()
