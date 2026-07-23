import logging

# Cấu hình định dạng log chuẩn hóa chuyên nghiệp
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s [%(levelname)s] (%(filename)s) -> %(message)s",
	datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("AI_Donghua_Studio")
