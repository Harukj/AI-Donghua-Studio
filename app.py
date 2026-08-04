from src.gui.main_window import MainWindow
from src.database.init_db import init_database

init_database()

if __name__ == "__main__":
    init_database()
    app = MainWindow()
    app.mainloop()
