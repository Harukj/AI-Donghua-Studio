from core.logger import studio_logger

class FXPlanner:
	def __init__(self):
		"""Khởi tạo trình quản lý hiệu ứng kỹ xảo hạt ảo - FX Planner v0.8"""
		pass

	def resolve_shot_fx_directives(self, environment_context: str = "default") -> dict:
		"""
		[FX PLANNER CORE LOGIC]
		Tự động trích xuất ma trận hạt môi trường từ sơ đồ của ChatGPT: wind, leaves, dust, fog.
		"""
		# Khởi tạo bộ từ khóa mặc định khớp 100% khung hiển thị của ChatGPT trên trình duyệt
		fx_config = {
			"wind": "gentle blowing wind",
			"leaves": "falling cinematic tree leaves",
			"dust": "floating micro dust particles in ambient light",
			"fog": "subtle depth fog atmospheric haze"
		}
		
		# Tự động đẩy mạnh hiệu ứng nếu là cảnh chiến đấu cao trào
		if environment_context.lower() == "combat":
			fx_config.update({
				"wind": "strong dynamic wind gust",
				"leaves": "swirling debris and fast leaves",
				"dust": "heavy smoke and ground dust particles",
				"fog": "thick dramatic cinematic fog"
			})
			
		studio_logger.logger.info(f"[FX PLANNER] Đã khóa bộ hạt môi trường: Gió=[{fx_config['wind']}], Hiệu ứng=[{fx_config['leaves']}]")
		return fx_config
