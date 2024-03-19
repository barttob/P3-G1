import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from TAB.main_tab.left_part import LeftPart
from TAB.main_tab.right_part import RightPart
from TAB.config_tab import ConfigTab

class MainTab(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # First row layout
        first_row_layout = QHBoxLayout()
        main_layout.addLayout(first_row_layout)

        # First part (left)
        left_part = LeftPart()
        first_row_layout.addWidget(left_part)
        left_part.setFixedWidth(650)

        # Second part (right)
        right_part = RightPart()
        first_row_layout.addWidget(right_part)

        # Second row layout
        second_row_layout = QHBoxLayout()
        main_layout.addLayout(second_row_layout)

        left_part.right_part = right_part
