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
import sys
from math import pi

# Declare global variables
space_between_objects = None
explore_holes = False
parallel = True
optimization = None
accuracy = None
rotations = None
starting_point = None
import numpy as np
import random

class RightPart(QWidget):

    def __init__(self):
        super().__init__()

        # self.space_between_objects = None
        # self.optimization = None
        # self.rotations = None
        # self.accuracy = None
        # self.parallel = True
        # self.explore_holes = False
        # self.starting_point = None

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
        self.volume = Box(50000, 50000)
        self.initUI()
        
    def initUI(self):
        pass

    def update(self, space_between_objects, explore_holes, parallel, optimization, accuracy, rotations, starting_point):
        global global_space_between_objects, global_explore_holes, global_parallel, global_optimization, global_accuracy, global_rotations, global_starting_point
        # Update global variables
        global_space_between_objects = float(space_between_objects)
        global_explore_holes = bool(explore_holes)
        global_parallel = bool(parallel)
        global_optimization = str(optimization)
        global_accuracy = float(accuracy)
        global_rotations = int(rotations)
        global_starting_point = str(starting_point)

        # Print updated configuration
        print("Updated configuration:")
        print("Space between objects:", global_space_between_objects)
        print("Explore holes:", global_explore_holes)
        print("Parallel:", global_parallel)
        print("Optimization:", global_optimization)
        print("Accuracy:", global_accuracy)
        print("Rotations:", global_rotations)
        print("Starting point:", global_starting_point)

    def display_file(self, file_paths):
        # Access global variables
        global global_space_between_objects, global_explore_holes, global_parallel, global_optimization, global_accuracy, global_rotations, global_starting_point

        self.inputPoints = []
        for file_path in file_paths:
            file_to_parse = Parser(file_path)
            if file_path.lower().endswith('.dxf'):
                self.inputPoints += file_to_parse.parse_dxf()
            elif file_path.lower().endswith('.svg'):
                self.inputPoints += file_to_parse.parse_svg()
        # Parametry nestingu
        config = NfpConfig()
        # Sposob ulozenia obiektow
        if global_optimization == "CENTER":
            config.alignment = NfpConfig.Alignment.CENTER
        elif global_optimization == "BOTTOM_LEFT":
            config.alignment = NfpConfig.Alignment.BOTTOM_LEFT
        elif global_optimization == "BOTTOM_RIGHT":
            config.alignment = NfpConfig.Alignment.BOTTOM_RIGHT
        elif global_optimization == "TOP_LEFT":
            config.alignment = NfpConfig.Alignment.TOP_LEFT
        elif global_optimization == "TOP_RIGHT":
            config.alignment = NfpConfig.Alignment.TOP_RIGHT
        elif global_optimization == "DONT_ALIGN":
            config.alignment = NfpConfig.Alignment.DONT_ALIGN
        # Odstep miedzy obiektami
        config.min_obj_distance = global_space_between_objects
        #Punkt poczatkowy
        if global_starting_point == "CENTER":
            config.starting_point = NfpConfig.Alignment.CENTER
        elif global_starting_point == "BOTTOM_LEFT":
            config.starting_point = NfpConfig.Alignment.BOTTOM_LEFT
        elif global_starting_point == "BOTTOM_RIGHT":
            config.starting_point = NfpConfig.Alignment.BOTTOM_RIGHT
        elif global_starting_point == "TOP_LEFT":
            config.starting_point = NfpConfig.Alignment.TOP_LEFT
        elif global_starting_point == "TOP_RIGHT":
            config.starting_point = NfpConfig.Alignment.TOP_RIGHT
        elif global_starting_point == "DONT_ALIGN":
            config.starting_point = NfpConfig.Alignment.DONT_ALIGN
        # Obroty obiektow
        if global_rotations == 4:
            config.rotations = [0, 0.5 * pi, pi, 1.5 * pi]
        elif global_rotations == 8:
            config.rotations = [i * 0.125 * pi for i in range(8)]
        # Dokladnosc
        config.accuracy = global_accuracy
        # Wielowatkowosc
        config.parallel = global_parallel
        # Eksploracja otworow
        config.explore_holes = global_explore_holes

        num_bins = nest(self.inputPoints, self.volume, 1, config)

        fig = Figure(figsize=(8, 8))  # Set figure size to be 2 times bigger
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
