
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QSizePolicy, QPushButton, QFileDialog, \
    QLabel, QLineEdit, QComboBox, QDialog, QDialogButtonBox, QMessageBox, QTextEdit
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
import multiprocessing
from PyQt5.QtWidgets import QDialog

class ToolParametersDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parametry narzędzia")
        
        self.layout = QVBoxLayout()
        
        # Etykieta do wyświetlania aktualnie wybranego narzędzia
        self.selected_tool_label = QLabel("")

        # Ustawienie początkowej wartości etykiety na podstawie wartości z global_saved_parameters
        if global_saved_parameters and 'type_tool' in global_saved_parameters:
            selected_tool = global_saved_parameters['type_tool']
            self.selected_tool_label.setText(f"Aktualnie wybrane narzędzie: {selected_tool}")
        else:
            self.selected_tool_label.setText("Aktualnie nie wybrano narzędzia.")

        self.layout.addWidget(self.selected_tool_label)

        # Tworzenie pól dla parametrów narzędzia przed generowaniem gcodu dla lasera
        # LineEdits for tool parameters
        self.cutting_speed_label = QLabel("Prędkość cięcia:")
        self.cutting_speed_edit = QLineEdit()
        self.layout.addWidget(self.cutting_speed_label)
        self.layout.addWidget(self.cutting_speed_edit)

        self.movement_speed_label = QLabel("Prędkość ruchu:")
        self.movement_speed_edit = QLineEdit()
        self.layout.addWidget(self.movement_speed_label)
        self.layout.addWidget(self.movement_speed_edit)

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

        # Tworzenie pól dla parametrów narzędzia przed generowaniem gcodu dla plazmy
        self.plasma_power_label = QLabel("Plazma power:")
        self.plasma_power_edit = QLineEdit()
        self.layout.addWidget(self.plasma_power_label)
        self.layout.addWidget(self.plasma_power_edit)

        self.plasma_speed_label = QLabel("Plazma speed:")
        self.plasma_speed_edit = QLineEdit()
        self.layout.addWidget(self.plasma_speed_label)
        self.layout.addWidget(self.plasma_speed_edit)


        # Tworzenie pól dla parametrów narzędzia przed generowaniem gcodu dla stożka

        self.cone_power_label = QLabel("Cone power:")
        self.cone_power_edit = QLineEdit()
        self.layout.addWidget(self.cone_power_label)
        self.layout.addWidget(self.cone_power_edit)

        self.cone_speed_label = QLabel("Cone speed:")
        self.cone_speed_edit = QLineEdit()
        self.layout.addWidget(self.cone_speed_label)
        self.layout.addWidget(self.cone_speed_edit)

        # Button to confirm tool parameters
        self.confirm_button = QPushButton("Generuj")
        self.confirm_button.clicked.connect(self.accept)
        self.layout.addWidget(self.confirm_button)

        self.setLayout(self.layout)
        self.update_tool_parameters(0)  # Set initial state based on current index
        
    def update_tool_parameters(self, index):
        # Get the current tool selection
        current_tool = global_saved_parameters['type_tool']

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
        if current_tool == "laser":
            self.cutting_speed_label.setVisible(True)
            self.cutting_speed_edit.setVisible(True)
            self.cutting_speed_edit.setText(global_saved_parameters['cutting_speed'])
            self.movement_speed_label.setVisible(True)
            self.movement_speed_edit.setVisible(True)
            self.movement_speed_edit.setText(global_saved_parameters['speed_movement'])
            self.depth_label.setVisible(True)
            self.depth_edit.setVisible(True)
            self.depth_edit.setText(global_saved_parameters['cutting_depth'])
            self.dwell_label.setVisible(True)
            self.dwell_edit.setVisible(True)
            self.dwell_edit.setText(global_saved_parameters['downtime'])
            self.unit_label.setVisible(True)
            self.unit_edit.setVisible(True)
            self.unit_edit.setText(global_saved_parameters['unit'])
            self.header_label.setVisible(True)
            self.header_edit.setVisible(True)
            self.header_edit.setText(global_saved_parameters['custom_header'])
            self.footer_label.setVisible(True)
            self.footer_edit.setVisible(True)
            self.footer_edit.setText(global_saved_parameters['custom_footer'])
            self.plasma_power_label.setVisible(False)
            self.plasma_power_edit.setVisible(False)
            self.plasma_speed_label.setVisible(False)
            self.plasma_speed_edit.setVisible(False)
            self.cone_power_label.setVisible(False)
            self.cone_power_edit.setVisible(False)
            self.cone_speed_label.setVisible(False)
            self.cone_speed_edit.setVisible(False)

        elif current_tool == "plazma":
            self.plasma_power_label.setVisible(True)
            self.plasma_power_edit.setVisible(True)
            self.plasma_power_edit.setText(global_saved_parameters['plasma_power'])
            self.plasma_speed_label.setVisible(True)
            self.plasma_speed_edit.setVisible(True)
            self.plasma_speed_edit.setText(global_saved_parameters['plasma_speed'])
            

            self.cutting_speed_label.setVisible(False)
            self.cutting_speed_edit.setVisible(False)
            self.movement_speed_label.setVisible(False)
            self.movement_speed_edit.setVisible(False)
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

            self.cone_power_label.setVisible(False)
            self.cone_power_edit.setVisible(False)
            self.cone_speed_label.setVisible(False)
            self.cone_speed_edit.setVisible(False)

            

        elif current_tool == "stożek":
            self.cone_power_label.setVisible(True)
            self.cone_power_edit.setVisible(True)
            self.cone_power_edit.setText(global_saved_parameters['cone_power'])
            self.cone_speed_label.setVisible(True)
            self.cone_speed_edit.setVisible(True)
            self.cone_speed_edit.setText(global_saved_parameters['cone_speed'])

            self.cutting_speed_label.setVisible(False)
            self.cutting_speed_edit.setVisible(False)
            self.movement_speed_label.setVisible(False)
            self.movement_speed_edit.setVisible(False)
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

            self.plasma_power_label.setVisible(False)
            self.plasma_power_edit.setVisible(False)
            self.plasma_speed_label.setVisible(False)
            self.plasma_speed_edit.setVisible(False)



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


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Generated G-code")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        simulate_button = QPushButton("Symuluj")
        layout.addWidget(simulate_button)
        simulate_button.clicked.connect(self.simulate_clicked)

        save_button = QPushButton("Zapisz")
        layout.addWidget(save_button)
        save_button.clicked.connect(self.save_clicked)

        self.setLayout(layout)

    def set_generated_gcode(self, generated_gcode):
        self.generated_gcode = generated_gcode
        self.text_edit.setText(generated_gcode)

    def simulate_clicked(self):
        # Tutaj możesz dodać logikę dla przycisku "Symuluj"
        pass

    def save_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("G-code files (*.gcode)")

        if file_dialog.exec_():
            gcode_filename = file_dialog.selectedFiles()[0]

            # Sprawdź, czy rozszerzenie ".gcode" jest dodane
            if not gcode_filename.endswith(".gcode"):
                gcode_filename += ".gcode"

            with open(gcode_filename, 'w') as file:
                file.write(self.generated_gcode)

            print(f"G-code file saved as: {os.path.abspath(gcode_filename)}")
        else:
            print("Canceled saving the G-code file")


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
        self.open_tool_parameters_button.clicked.connect(self.open_tool_parameters_dialog_right)
        layout.addWidget(self.open_tool_parameters_button)

        self.setLayout(layout)
        self.inputPoints = []
        self.volume = None  # Move initialization to display_file method


    # metoda przyjmująca parametry narzędzia wybrane podczas konifguracji nestingu 
    def sended_tool_param(self, saved_parameters):
        
        # Deklaracja zmiennej globalnej
        global global_saved_parameters
        
        # Przypisanie wartości zmiennej globalnej
        global_saved_parameters = saved_parameters
        


    def open_tool_parameters_dialog_right(self):
        dialog = ToolParametersDialog()

        if dialog.exec_():
            # Tworzenie i konfiguracja okna dialogowego
            custom_dialog = CustomDialog()
            custom_dialog.setModal(True)

            # Pobierz parametry narzędzia od użytkownika
            cutting_speed = float(dialog.cutting_speed_edit.text())
            movement_speed = float(dialog.movement_speed_edit.text())
            depth = float(dialog.depth_edit.text())
            dwell_time = float(dialog.dwell_edit.text())
            unit = dialog.unit_edit.text()
            custom_header = [dialog.header_edit.text()]
            custom_footer = [dialog.footer_edit.text()]

            # Wygeneruj G-kod z pliku SVG
            gcode_compiler = Compiler(
                interfaces.Gcode,   
                cutting_speed=cutting_speed,
                movement_speed=movement_speed,
                pass_depth=depth,
                dwell_time=dwell_time,
                unit=unit,
                custom_header=custom_header,
                custom_footer=custom_footer
            )

            curves = parse_file("output.svg")
            gcode_compiler.append_curves(curves)

            # Odczytaj wygenerowany G-kod
            generated_gcode = gcode_compiler.compile()

            # Ustaw wygenerowany G-kod w oknie dialogowym
            custom_dialog.set_generated_gcode(generated_gcode)

            custom_dialog.exec_()

            print("Canceled generating G-code")

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
        # Wyświetl listę obrotów w terminalu
        rotations_text = ", ".join([f"{rot:.2f}" for rot in rotations])
        print(f"Wygenerowane obroty: [{rotations_text}] rad")
        return rotations

    def display_file(self, file_paths, width, height, checked_paths):
        variables = [global_space_between_objects, global_optimization, global_accuracy, global_rotations, global_starting_point]
        #Sprawdzenie konfiguracji
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
        # for path in checked_paths:
        #     print(path)
        file_to_parse = Parser(checked_paths)
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
        
        for i in range(len(self.inputPoints)):
            print()
        #     print(i)
        #     print(self.inputPoints[i].isFixed())
        #     print(self.inputPoints[i].holeCount())
        #     print(self.inputPoints[i].isContourConvex())
        #     print(self.inputPoints[i].areHolesConvex())
        #     print(self.inputPoints[i].holeCount())
        #     print(self.inputPoints[i].boundingBox())
            # print(self.inputPoints[i].area())

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
        self.open_tool_parameters_dialog_right()

