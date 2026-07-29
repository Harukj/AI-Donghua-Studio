# GUI Package
# Thêm vào cuối hàm __init__(self) của file gui/main_window.py:

# Khởi tạo đối tượng Dashboard mới tạo ở trên
self.dashboard = Dashboard(self)

# Định vị vị trí hiển thị ở cột số 1 (bên cạnh thanh Sidebar ở cột 0)
self.dashboard.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
