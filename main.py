import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from qasync import QEventLoop

from TAB.main_tab.main_tab import MainTab
from TAB.config_tab import ConfigTab
from TAB.info_tab import InfoTab
from TAB.main_tab.right_part import RightPart
from db.open_db import create_table

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OptiNest v1.0")
        screen_geometry = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_geometry)
        self.showFullScreen()

        right_part = RightPart()

        tab_widget = QTabWidget()
        main_tab = MainTab()
        config_tab = ConfigTab(right_part)  # Komunikacja miedzy klasami
        info_tab = InfoTab()

        tab_widget.addTab(main_tab, "Main")
        tab_widget.addTab(config_tab, "Konfiguracja nestingu")
        tab_widget.addTab(info_tab, "Wizualizacja")

        self.setCentralWidget(tab_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    create_table()  # Inicjalizacja bazy danych

    window = MainWindow()
    window.show()
    loop.run_forever()
