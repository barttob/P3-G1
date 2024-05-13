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

        right_part = RightPart(self.change_tab)

        self.tab_widget = QTabWidget()
        main_tab = MainTab(self.change_tab)
        config_tab = ConfigTab(right_part)  # Komunikacja miedzy klasami
        self.info_tab = InfoTab()

        self.tab_widget.addTab(main_tab, "Main")
        self.tab_widget.addTab(config_tab, "Konfiguracja nestingu")
        self.tab_widget.addTab(self.info_tab, "Wizualizacja")

        self.setCentralWidget(self.tab_widget)
    
    def change_tab(self, tab_index, gcode_text):
        self.tab_widget.setCurrentIndex(tab_index)
        self.info_tab.set_gcode_text(gcode_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    create_table()  # Inicjalizacja bazy danych

    window = MainWindow()
    window.show()
    loop.run_forever()
