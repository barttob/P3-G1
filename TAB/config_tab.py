from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class ConfigTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Tu będą ustawienia konfiguracyjne")
        layout.addWidget(label)
