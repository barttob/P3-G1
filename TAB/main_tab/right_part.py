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
import numpy as np
import random

class RightPart(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Create QGraphicsView and QGraphicsScene for embedding matplotlib plot
        self.graphics_view = QGraphicsView()
        layout.addWidget(self.graphics_view)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        self.setLayout(layout)
        self.inputPoints = []
        self.volume = None  # Move initialization to display_file method
        
    def initUI(self):
        pass

    def display_file(self, file_paths, width, height):  # Dodaj parametry szerokości i wysokości
        self.inputPoints = []
        for file_path in file_paths:
            file_to_parse = Parser(file_path)
            self.inputPoints += file_to_parse.parse_svg()
            
        config = NfpConfig()
        config.alignment = NfpConfig.Alignment.BOTTOM_LEFT
        config.starting_point = NfpConfig.Alignment.CENTER
        config.rotations = [i * (2 * 3.14159) / 12 for i in range(12)]
        config.accuracy = 0.65
        config.explore_holes = False
        config.parallel = True

        self.volume = Box(width, height)

        num_bins = nest(self.inputPoints, self.volume, 1, config)

        fig = Figure(figsize=(8, 8))
        ax = fig.add_subplot(111)

        for item in self.inputPoints:
            x_values = []
            y_values = []
            transItem = item.transformedShape()
            rows = len(transItem.toString().strip().split('\n')) - 1
            for i in range(rows - 1):
                x_value = transItem.vertex(i).x()
                y_value = transItem.vertex(i).y()
                x_values.append(x_value)
                y_values.append(y_value)
            random_color = (random.random(), random.random(), random.random())
            ax.plot(x_values, y_values, color=random_color, linewidth=1)

        canvas = FigureCanvas(fig)
        self.scene.addWidget(canvas)
        ax.set_aspect('equal')
        ax.set_xlim([-self.volume.width()/2, self.volume.width()/2])
        ax.set_ylim([-self.volume.height()/2, self.volume.height()/2])

        ax.set_xticks([])
        ax.set_yticks([])

        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas.updateGeometry()


