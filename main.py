import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from TAB.main_tab.main_tab import MainTab
from TAB.config_tab import ConfigTab
from TAB.info_tab import InfoTab
from db.database import create_table, insert_sample_data

# Inicjalizacja bazy danych
create_table()
# insert_sample_data()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OptiNest v1.0")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()

        tab_widget = QTabWidget()
        main_tab = MainTab()
        config_tab = ConfigTab()
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
