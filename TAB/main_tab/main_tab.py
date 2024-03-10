import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from TAB.main_tab.left_part import LeftPart
from TAB.main_tab.right_part import RightPart

class MainTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Pierwsza część (lewa)
        left_part = LeftPart()
        layout.addWidget(left_part)
        # Ustawienie stałej szerokości dla lewej części
        left_part.setFixedWidth(650)

        # Druga część (prawa)
        right_part = RightPart()
        layout.addWidget(right_part)
