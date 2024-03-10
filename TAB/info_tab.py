from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class InfoTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Tu będą informacje")
        layout.addWidget(label)
