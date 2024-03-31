from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene, QSizePolicy, QMessageBox
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
import numpy as np
import random

# Declare global variables
global_space_between_objects = None
global_explore_holes = False
global_parallel = True
global_optimization = None
global_accuracy = None
global_rotations = None
global_starting_point = None

# Define CombinedConfig class
class CombinedConfig:
    def __init__(self, nfp_config, bottom_left_config):
        self.nfp_config = nfp_config
        self.bottom_left_config = bottom_left_config

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
        global_space_between_objects = space_between_objects
        global_explore_holes = explore_holes
        global_parallel = parallel
        global_optimization = optimization
        global_accuracy = accuracy
        global_rotations = rotations
        global_starting_point = starting_point

        # Print updated configuration
        print("Updated configuration:")
        print("Space between objects:", global_space_between_objects)
        print("Explore holes:", global_explore_holes)
        print("Parallel:", global_parallel)
        print("Optimization:", global_optimization)
        print("Accuracy:", global_accuracy)
        print("Rotations:", global_rotations)
        print("Starting point:", global_starting_point)
    
    def check_parameters(self):
        global global_space_between_objects, global_optimization, global_accuracy, global_rotations, global_starting_point
        variables = [global_space_between_objects, global_optimization, global_accuracy, global_rotations, global_starting_point]
        for var in variables:
            if var is None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: Not all nesting parameters are configured.")
                msg.setInformativeText("Please configure all nesting parameters before calling the display_file function.")
                msg.setWindowTitle("Error")
                msg.exec_()
                return

    def display_file(self, file_paths):
        # Access global variables
        #global global_space_between_objects, global_explore_holes, global_parallel, global_optimization, global_accuracy, global_rotations, global_starting_point
        # Update configuration based on user input
        #self.check_parameters()
        variables = [global_space_between_objects, global_optimization, global_accuracy, global_rotations, global_starting_point]
        for var in variables:
            if var is None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: Not all nesting parameters are configured.")
                msg.setInformativeText("Please configure all nesting parameters before calling the nesting function.")
                msg.setWindowTitle("Error")
                msg.exec_()
                return
        self.inputPoints = []
        for file_path in file_paths:
            file_to_parse = Parser(file_path)
            if file_path.lower().endswith('.dxf'):
                self.inputPoints += file_to_parse.parse_dxf()
            elif file_path.lower().endswith('.svg'):
                self.inputPoints += file_to_parse.parse_svg()

        # Parametry nestingu
        nfp_config = NfpConfig()
        # Sposob ulozenia obiektow
        if global_optimization == "CENTER":
            nfp_config.alignment = NfpConfig.Alignment.CENTER
        elif global_optimization == "BOTTOM_LEFT":
            nfp_config.alignment = NfpConfig.Alignment.BOTTOM_LEFT
        elif global_optimization == "BOTTOM_RIGHT":
            nfp_config.alignment = NfpConfig.Alignment.BOTTOM_RIGHT
        elif global_optimization == "TOP_LEFT":
            nfp_config.alignment = NfpConfig.Alignment.TOP_LEFT
        elif global_optimization == "TOP_RIGHT":
            nfp_config.alignment = NfpConfig.Alignment.TOP_RIGHT
        elif global_optimization == "DONT_ALIGN":
            nfp_config.alignment = NfpConfig.Alignment.DONT_ALIGN
        #Punkt poczatkowy
        if global_starting_point == "CENTER":
            nfp_config.starting_point = NfpConfig.Alignment.CENTER
        elif global_starting_point == "BOTTOM_LEFT":
            nfp_config.starting_point = NfpConfig.Alignment.BOTTOM_LEFT
        elif global_starting_point == "BOTTOM_RIGHT":
            nfp_config.starting_point = NfpConfig.Alignment.BOTTOM_RIGHT
        elif global_starting_point == "TOP_LEFT":
            nfp_config.starting_point = NfpConfig.Alignment.TOP_LEFT
        elif global_starting_point == "TOP_RIGHT":
            nfp_config.starting_point = NfpConfig.Alignment.TOP_RIGHT
        elif global_starting_point == "DONT_ALIGN":
            nfp_config.starting_point = NfpConfig.Alignment.DONT_ALIGN
        # Obroty obiektow
        if global_rotations == 0:
            nfp_config.rotations = []
        elif global_rotations == 1:
            nfp_config.rotations = [0]
        elif global_rotations == 2:
            nfp_config.rotations = [0, pi]
        elif global_rotations == 3:
            nfp_config.rotations = [0, 0.5 * pi, pi]
        elif global_rotations == 4:
            nfp_config.rotations = [0, 0.5 * pi, pi, 1.5 * pi]
        elif global_rotations == 5:
            nfp_config.rotations = [0, 0.25 * pi, 0.5 * pi, 0.75 * pi, pi]
        elif global_rotations == 6:
            nfp_config.rotations = [0, 0.333 * pi, 0.667 * pi, pi, 1.333 * pi, 1.667 * pi]
        elif global_rotations == 7:
            nfp_config.rotations = [0, 0.286 * pi, 0.571 * pi, 0.857 * pi, pi, 1.286 * pi, 1.571 * pi]
        elif global_rotations == 8:
            nfp_config.rotations = [i * 0.125 * pi for i in range(8)]
        # Dokladnosc
        nfp_config.accuracy = global_accuracy
        # Wielowatkowosc
        nfp_config.parallel = global_parallel
        # Eksploracja otworow
        nfp_config.explore_holes = global_explore_holes

        spacing = int(global_space_between_objects)

        num_bins = nest(self.inputPoints, self.volume, spacing, nfp_config)

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
