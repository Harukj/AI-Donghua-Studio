from gui.main_window import MainWindow
from database.init_db import init_database

init_database()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()