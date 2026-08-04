from sqlalchemy.orm import Session
from src.database.models.episode import EpisodeModel
from src.core.logger import studio_logger

class ProductionWorkflowEngine:
	def __init__(self, db_session: Session):
		"""Khởi tạo Động cơ điều phối quy trình sản xuất 9 phân lớp - Production Workflow v1.0"""
		self.db = db_session

	def advance_workflow_stage(self, current_stage: str) -> str:
		"""
		[PRODUCTION WORKFLOW PIPELINE - 9 INDUSTRIAL LAYERS]
		Điều phối chu trình dịch chuyển mạch dữ liệu qua đúng 9 nấc nghiêm ngặt của ChatGPT:
		episode -> chapter -> scene -> shot -> asset -> prompt -> render -> review -> export.
		"""
		workflow_stages = ["episode", "chapter", "scene", "shot", "asset", "prompt", "render", "review", "export"]
		stage_lower = current_stage.lower().strip()

		if stage_lower not in workflow_stages:
			raise ValueError(f"Nấc quy trình '{current_stage}' không tồn tại trong thiết kế của DreamForge!")

		current_index = workflow_stages.index(stage_lower)
		
		# Nếu đã chạm đến nấc cuối cùng (export), khóa trạng thái hoàn thành dây chuyền
		if current_index == len(workflow_stages) - 1:
			next_stage = "export"
			studio_logger.logger.info("[WORKFLOW] [✓] Phim hoạt hình thành phẩm đã xuất bản và gộp nối hoàn tất!")
		else:
			next_stage = workflow_stages[current_index + 1]
			studio_logger.logger.info(f"[WORKFLOW] Mạch sản xuất tịnh tiến: [{stage_lower.upper()}] ➔ ➔ ➔ [{next_stage.upper()}]")

		return next_stage
