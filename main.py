import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from TAB.main_tab.main_tab import MainTab
from TAB.config_tab import ConfigTab
from TAB.info_tab import InfoTab
from TAB.main_tab.right_part import RightPart
from db.open_db import create_table
from db.db_operations import insert_tool_parameter, insert_nest_config, select_all_tool_parameters, select_all_nest_configs

# Inicjalizacja bazy danych
create_table()
# insert_tool_parameter('laser', 103, 10, 12, 29, 'NULL' , 'mm', 'M10', 'M24')
# insert_tool_parameter('plazma', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL' , 'NULL', 'NULL', 'NULL')
# insert_tool_parameter('stozek', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL' , 'NULL', 'NULL', 'NULL')
# insert_nest_config('default_laser', 0.3 , 'CENTER', 'CENTER', 4, 0.65, 0, 1, 1)
# insert_nest_config('best_laser', 0.3 , 'BOTTOM_LEFT', 'CENTER', 360, 1, 0, 1, 1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OptiNest v1.0")
        # self.setGeometry(100, 100, 1360, 720)
        screen_geometry = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_geometry)
        self.showFullScreen()

        # Tworzenie instancji RightPart
        right_part = RightPart()

        tab_widget = QTabWidget()
        main_tab = MainTab()
        config_tab = ConfigTab(right_part)  # Komunikacja miedzy klasami
        info_tab = InfoTab()

        tab_widget.addTab(main_tab, "Main")
        tab_widget.addTab(config_tab, "Konfiguracja nestingu")
        tab_widget.addTab(info_tab, "Info")

        self.setCentralWidget(tab_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
