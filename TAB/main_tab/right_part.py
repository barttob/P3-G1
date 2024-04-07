
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QSizePolicy, QPushButton, QFileDialog, \
    QLabel, QLineEdit, QComboBox, QDialog, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import Qt
import random
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pynest2d import *
from utils.parser import Parser
import sys
from math import pi
import numpy as np
import random
from svg_to_gcode.compiler import Compiler, interfaces
from svg_to_gcode.svg_parser import parse_file
from pygcode import Line


class ToolParametersDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parametry narzędzia")
        
        self.layout = QVBoxLayout()
        
        # Combo box to select tool
        self.tool_label = QLabel("Wybierz narzędzie:")
        self.tool_combobox = QComboBox()
        self.tool_combobox.addItems(["Laserowe", "Plazmowe", "Stożkowe", "Płaskie"])
        self.tool_combobox.currentIndexChanged.connect(self.update_tool_parameters)
        self.layout.addWidget(self.tool_label)
        self.layout.addWidget(self.tool_combobox)

        # LineEdits for tool parameters
        self.movement_speed_label = QLabel("Prędkość ruchu:")
        self.movement_speed_edit = QLineEdit()
        self.layout.addWidget(self.movement_speed_label)
        self.layout.addWidget(self.movement_speed_edit)

        self.cutting_speed_label = QLabel("Prędkość cięcia:")
        self.cutting_speed_edit = QLineEdit()
        self.layout.addWidget(self.cutting_speed_label)
        self.layout.addWidget(self.cutting_speed_edit)

        self.depth_label = QLabel("Głębokość cięcia:")  # brak w gcodzie
        self.depth_edit = QLineEdit()
        self.layout.addWidget(self.depth_label)
        self.layout.addWidget(self.depth_edit)

        self.dwell_label = QLabel("Czas przestoju:")
        self.dwell_edit = QLineEdit()
        self.layout.addWidget(self.dwell_label)
        self.layout.addWidget(self.dwell_edit)

        self.unit_label = QLabel("Jednostka:")  # brak w gcodzie
        self.unit_edit = QLineEdit()
        self.layout.addWidget(self.unit_label)
        self.layout.addWidget(self.unit_edit)

        self.header_label = QLabel("Niestandardowy nagłówek:")
        self.header_edit = QLineEdit()
        self.layout.addWidget(self.header_label)
        self.layout.addWidget(self.header_edit)

        self.footer_label = QLabel("Niestandardowy stopka:")
        self.footer_edit = QLineEdit()
        self.layout.addWidget(self.footer_label)
        self.layout.addWidget(self.footer_edit)

        # Button to confirm tool parameters
        self.confirm_button = QPushButton("Generuj")
        self.confirm_button.clicked.connect(self.accept)
        self.layout.addWidget(self.confirm_button)

        self.setLayout(self.layout)
        self.update_tool_parameters(0)  # Set initial state based on current index
        
    def update_tool_parameters(self, index):
        # Get the current tool selection
        current_tool = self.tool_combobox.currentText()

        # Show none parameters by default
        #self.movement_speed_label.setVisible(False)
        #self.movement_speed_edit.setVisible(True)
        #self.cutting_speed_label.setVisible(True)
        #self.cutting_speed_edit.setVisible(True)
        #self.depth_label.setVisible(True)
        #self.depth_edit.setVisible(True)
        #self.dwell_label.setVisible(True)
        #self.dwell_edit.setVisible(True)
        #self.unit_label.setVisible(True)
        #self.unit_edit.setVisible(True)
        #self.header_label.setVisible(True)
        #self.header_edit.setVisible(True)
        #self.footer_label.setVisible(True)
        #self.footer_edit.setVisible(True)

        # Hide parameters based on tool selection
        if current_tool == "Laserowe":
            self.movement_speed_label.setVisible(True)
            self.movement_speed_edit.setVisible(True)
            self.cutting_speed_label.setVisible(True)
            self.cutting_speed_edit.setVisible(True)
            self.depth_label.setVisible(True)
            self.depth_edit.setVisible(True)
            self.dwell_label.setVisible(True)
            self.dwell_edit.setVisible(True)
            self.unit_label.setVisible(True)
            self.unit_edit.setVisible(True)
            self.header_label.setVisible(True)
            self.header_edit.setVisible(True)
            self.footer_label.setVisible(True)
            self.footer_edit.setVisible(True)

        elif current_tool == "Plazmowe":
            self.movement_speed_label.setVisible(False)
            self.movement_speed_edit.setVisible(False)
            self.cutting_speed_label.setVisible(False)
            self.cutting_speed_edit.setVisible(False)
            self.depth_label.setVisible(False)
            self.depth_edit.setVisible(False)
            self.dwell_label.setVisible(False)
            self.dwell_edit.setVisible(False)
            self.unit_label.setVisible(False)
            self.unit_edit.setVisible(False)
            self.header_label.setVisible(False)
            self.header_edit.setVisible(False)
            self.footer_label.setVisible(False)
            self.footer_edit.setVisible(False)

        elif current_tool == "Stożkowe":
            self.movement_speed_label.setVisible(False)
            self.movement_speed_edit.setVisible(False)
            self.cutting_speed_label.setVisible(False)
            self.cutting_speed_edit.setVisible(False)
            self.depth_label.setVisible(False)
            self.depth_edit.setVisible(False)
            self.dwell_label.setVisible(False)
            self.dwell_edit.setVisible(False)
            self.unit_label.setVisible(False)
            self.unit_edit.setVisible(False)
            self.header_label.setVisible(False)
            self.header_edit.setVisible(False)
            self.footer_label.setVisible(False)
            self.footer_edit.setVisible(False)

        elif current_tool == "Płaskie":
            self.movement_speed_label.setVisible(False)
            self.movement_speed_edit.setVisible(False)
            self.cutting_speed_label.setVisible(False)
            self.cutting_speed_edit.setVisible(False)
            self.depth_label.setVisible(False)
            self.depth_edit.setVisible(False)
            self.dwell_label.setVisible(False)
            self.dwell_edit.setVisible(False)
            self.unit_label.setVisible(False)
            self.unit_edit.setVisible(False)
            self.header_label.setVisible(False)
            self.header_edit.setVisible(False)
            self.footer_label.setVisible(False)
            self.footer_edit.setVisible(False)


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

        # Button to open tool parameters dialog
        self.open_tool_parameters_button = QPushButton("Generuj G-code")
        self.open_tool_parameters_button.clicked.connect(self.open_tool_parameters_dialog)
        layout.addWidget(self.open_tool_parameters_button)

        self.setLayout(layout)
        self.inputPoints = []
        self.volume = None  # Move initialization to display_file method

    def open_tool_parameters_dialog(self):
        dialog = ToolParametersDialog()
        if dialog.exec_():
            # Get user-defined tool parameters
            movement_speed = float(dialog.movement_speed_edit.text())
            cutting_speed = float(dialog.cutting_speed_edit.text())
            depth = float(dialog.depth_edit.text())
            dwell_time = float(dialog.dwell_edit.text())
            unit = dialog.unit_edit.text()
            custom_header = [dialog.header_edit.text()]
            custom_footer = [dialog.footer_edit.text()]

            # Generate G-code from SVG
            gcode_compiler = Compiler(
                interfaces.Gcode,
                movement_speed=movement_speed,
                cutting_speed=cutting_speed,  # Ustawienie prędkości cięcia
                pass_depth=depth,  # Ustawienie głębokości cięcia
                dwell_time=dwell_time,  # Ustawienie czasu przestoju
                unit=unit,  # Ustawienie jednostki
                custom_header=custom_header,  # Ustawienie niestandardowego nagłówka
                custom_footer=custom_footer  # Ustawienie niestandardowej stopki
            )

            curves = parse_file("output.svg")  # Using previously saved SVG file
            gcode_compiler.append_curves(curves)

            # Get the file location for saving G-code
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.AnyFile)
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            file_dialog.setNameFilter("G-code files (*.gcode)")
            if file_dialog.exec_():
                gcode_filename = file_dialog.selectedFiles()[0]

                # Save the G-code to the final file
                gcode_compiler.compile_to_file(gcode_filename)

                # Inform the user about the saved G-code file
                print(f"G-code file saved as: {os.path.abspath(gcode_filename)}")
                return

            print("Canceled saving the G-code file")
            return

        print("Canceled generating G-code")

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
    
    def generate_rotations(self, num_rotations):
        angle_step = 2 * pi / num_rotations
        rotations = [i * angle_step for i in range(num_rotations)]
        return rotations

    def display_file(self, file_paths, width, height):
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
            self.inputPoints += file_to_parse.parse_svg()

        self.volume = Box(width, height)
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
        else:
            nfp_config.rotations = self.generate_rotations(global_rotations)
        # Dokladnosc
        nfp_config.accuracy = global_accuracy
        # Wielowatkowosc
        nfp_config.parallel = global_parallel
        # Eksploracja otworow
        nfp_config.explore_holes = global_explore_holes

        spacing = int(global_space_between_objects * 0.352777778)

        num_bins = nest(self.inputPoints, self.volume, spacing, nfp_config)
        

        #fig = Figure(figsize=(8, 8))
        #ax = fig.add_subplot(111)

        # Ustawienie marginesów na zerowe wartości, dodanie parametru tight_layout i pad_inches
        fig = Figure(figsize=(8, 8), tight_layout={'pad': 0})
        ax = fig.add_subplot(111)

        for item in self.inputPoints:
            x_values = []
            y_values = []
            transItem = item.transformedShape()
            if item.binId() == 0:
                rows = len(transItem.toString().strip().split('\n')) - 1
                for i in range(rows - 1):
                    x_value = transItem.vertex(i).x()
                    y_value = transItem.vertex(i).y()
                    x_values.append(x_value)
                    y_values.append(y_value)
                random_color = (random.random(), random.random(), random.random())
                ax.plot(x_values, y_values, color=random_color, linewidth=1)

        ax.set_aspect('equal')
        ax.set_xlim([-self.volume.width() / 2, self.volume.width() / 2])
        ax.set_ylim([-self.volume.height() / 2, self.volume.height() / 2])

        ax.set_xticks([])
        ax.set_yticks([])

        # Save the figure as SVG with tight bounding box and zero padding
        svg_filename = "output.svg"
        fig.savefig(svg_filename, format='svg', bbox_inches='tight', pad_inches=0)

        # Add canvas to scene
        canvas = FigureCanvas(fig)
        self.scene.addWidget(canvas)

        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas.updateGeometry()

        # Inform the user about the saved SVG file
        print(f"SVG file saved as: {os.path.abspath(svg_filename)}")

    def generate_gcode(self):
        # Open the tool parameters dialog
        self.open_tool_parameters_dialog()

