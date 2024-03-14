from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt
import xml.etree.ElementTree as ET
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from xml.dom import minidom
import svg.path
import matplotlib.pyplot as plt
from pynest2d import *
from utils.parser import Parser

class RightPart(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label)
        
        # Create QGraphicsView and QGraphicsScene for embedding matplotlib plot
        self.graphics_view = QGraphicsView()
        layout.addWidget(self.graphics_view)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        self.setLayout(layout)
        self.inputPoints = []
        self.volume = Box(150000, 150000)
        self.initUI()
        
    def initUI(self):
        pass

    def display_file(self, file_path):
        file_to_parse = Parser(file_path)
        if file_path.lower().endswith('.dxf'):
            self.inputPoints = file_to_parse.parse_dxf()
        elif file_path.lower().endswith('.svg'):
            self.inputPoints = file_to_parse.parse_svg()

        config = NfpConfig()
        config.alignment = NfpConfig.Alignment.BOTTOM_LEFT
        config.starting_point = NfpConfig.Alignment.CENTER

        num_bins = nest(self.inputPoints, self.volume, 1, config)
        # Clear the scene before adding new items
        fig = Figure()
        ax = fig.add_subplot(111)


        # fig, ax = plt.subplots(figsize=(8, 6), dpi=150)  # Create a new figure for each item

        for item in self.inputPoints:
            # figure.sca(ax)
            x_values = []
            y_values = []
            transItem = item.transformedShape()
            print(transItem)
            rows = len(transItem.toString().strip().split('\n')) - 1
            for i in range(rows - 1):
                x_value = transItem.vertex(i).x()
                y_value = transItem.vertex(i).y()
                x_values.append(x_value)
                y_values.append(y_value)
            ax.plot(x_values, y_values, color='black', linewidth=1)  # Adjust linewidth

        canvas = FigureCanvas(fig)
        self.scene.addWidget(canvas)
        ax.set_aspect('equal')
        ax.set_xlim([-self.volume.width()/2, self.volume.width()/2])
        ax.set_ylim([-self.volume.height()/2, self.volume.height()/2])

        ax.set_xticks([])
        ax.set_yticks([])

        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas.updateGeometry()

