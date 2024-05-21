
from PyQt5.QtGui import QImage, QPixmap, QPainter, QFont, QColor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
import random
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pynest2d import NfpConfig, nest, Box, Item, Point
from utils.parser import Parser
import sys
from math import pi
import numpy as np
import random
import time
from svg_to_gcode.compiler import Compiler, interfaces
from svg_to_gcode.svg_parser import parse_file
from pygcode import Line
from svg.path import parse_path
import math
import multiprocessing
from PyQt5.QtWidgets import QDialog
import sqlite3
from datetime import datetime
import secrets
from matplotlib.patches import Rectangle
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from PyQt5.QtGui import QColor, QPen  # Import QPen here
from PyQt5.QtCore import Qt, QPointF, QLineF
import asyncio
from qasync import asyncSlot
import re
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import MultipleLocator, FuncFormatter
from collections import namedtuple

import time

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
        self.cutting_speed_label = QLabel("Prędkość cięcia: (mm/s)")
        self.cutting_speed_edit = QLineEdit()
        self.layout.addWidget(self.cutting_speed_label)
        self.layout.addWidget(self.cutting_speed_edit)

        self.movement_speed_label = QLabel("Prędkość ruchu: (mm/s)")
        self.movement_speed_edit = QLineEdit()
        self.layout.addWidget(self.movement_speed_label)
        self.layout.addWidget(self.movement_speed_edit)

        self.probing_depth_label = QLabel("Głębokość sondowania: (mm)")  # brak w gcodzie
        self.probing_depth_edit = QLineEdit()
        self.layout.addWidget(self.probing_depth_label)
        self.layout.addWidget(self.probing_depth_edit)

        #self.depth_label = QLabel("Głębokość cięcia:")  # brak w gcodzie
        #self.depth_edit = QLineEdit()
        #self.layout.addWidget(self.depth_label)
        #self.layout.addWidget(self.depth_edit)

        self.dwell_label = QLabel("Czas przestoju: (ms)")
        self.dwell_edit = QLineEdit()
        self.layout.addWidget(self.dwell_label)
        self.layout.addWidget(self.dwell_edit)

        self.unit_label = QLabel("Jednostka: (mm)")  # brak w gcodzie
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
        self.plasma_power_label = QLabel("Plazma power: (W)")
        self.plasma_power_edit = QLineEdit()
        self.layout.addWidget(self.plasma_power_label)
        self.layout.addWidget(self.plasma_power_edit)

        self.plasma_speed_label = QLabel("Plazma speed: (mm/s)")
        self.plasma_speed_edit = QLineEdit()
        self.layout.addWidget(self.plasma_speed_label)
        self.layout.addWidget(self.plasma_speed_edit)

        self.cutting_height_label = QLabel("Wysokość cięcia: (mm)")
        self.cutting_height_edit = QLineEdit()
        self.layout.addWidget(self.cutting_height_label)
        self.layout.addWidget(self.cutting_height_edit)

        self.piercing_height_label = QLabel("Wysokość przebicia: (mm)")
        self.piercing_height_edit = QLineEdit()
        self.layout.addWidget(self.piercing_height_label)
        self.layout.addWidget(self.piercing_height_edit)

        self.piercing_time_label = QLabel("Czas przebicia: (s)")
        self.piercing_time_edit = QLineEdit()
        self.layout.addWidget(self.piercing_time_label)
        self.layout.addWidget(self.piercing_time_edit)

        self.floating_height_label = QLabel("Czas dryfu: (s)")
        self.floating_height_edit = QLineEdit()
        self.layout.addWidget(self.floating_height_label)
        self.layout.addWidget(self.floating_height_edit)






        # Tworzenie pól dla parametrów narzędzia przed generowaniem gcodu dla stożka

        self.cone_power_label = QLabel("Cone power: (W)")
        self.cone_power_edit = QLineEdit()
        self.layout.addWidget(self.cone_power_label)
        self.layout.addWidget(self.cone_power_edit)

        self.cone_speed_label = QLabel("Cone speed: (mm/s)")
        self.cone_speed_edit = QLineEdit()
        self.layout.addWidget(self.cone_speed_label)
        self.layout.addWidget(self.cone_speed_edit)

        self.floating_height_cone_label = QLabel("Czas dryfu dla frezu: (s)")
        self.floating_height_cone_edit = QLineEdit()
        self.layout.addWidget(self.floating_height_cone_label)
        self.layout.addWidget(self.floating_height_cone_edit)

        self.total_depth_of_cutting_label = QLabel("Całkowita głębokość skrawania: (mm)")
        self.total_depth_of_cutting_edit = QLineEdit()
        self.layout.addWidget(self.total_depth_of_cutting_label)
        self.layout.addWidget(self.total_depth_of_cutting_edit)

        self.depth_of_cutting_per_pass_label = QLabel("Głębokość skrawania na przejście: (mm)")
        self.depth_of_cutting_per_pass_edit = QLineEdit()
        self.layout.addWidget(self.depth_of_cutting_per_pass_label)
        self.layout.addWidget(self.depth_of_cutting_per_pass_edit)

        




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
            self.probing_depth_label.setVisible(False)
            self.probing_depth_edit.setVisible(False)
            self.cutting_height_label.setVisible(False)
            self.cutting_height_edit.setVisible(False)
            self.piercing_height_label.setVisible(False)
            self.piercing_height_edit.setVisible(False)
            self.piercing_time_label.setVisible(False)
            self.piercing_time_edit.setVisible(False)
            self.floating_height_label.setVisible(False)
            self.floating_height_edit.setVisible(False)
            self.floating_height_cone_label.setVisible(False)
            self.floating_height_cone_edit.setVisible(False)
            self.total_depth_of_cutting_label.setVisible(False)
            self.total_depth_of_cutting_edit.setVisible(False)
            self.depth_of_cutting_per_pass_label.setVisible(False)
            self.depth_of_cutting_per_pass_edit.setVisible(False)
            self.probing_depth_label.setVisible(False)
            self.probing_depth_edit.setVisible(False)

        elif current_tool == "plazma":
            #self.plasma_power_label.setVisible(True)
            #self.plasma_power_edit.setVisible(True)
            #self.plasma_power_edit.setText(global_saved_parameters['plasma_power'])
            #self.plasma_speed_label.setVisible(True)
            #self.plasma_speed_edit.setVisible(True)
            #self.plasma_speed_edit.setText(global_saved_parameters['plasma_speed'])
            

            self.cutting_speed_label.setVisible(True)
            self.cutting_speed_edit.setVisible(True)
            self.cutting_speed_edit.setText(global_saved_parameters['cutting_speed'])
            self.movement_speed_label.setVisible(True)
            self.movement_speed_edit.setVisible(True)
            self.movement_speed_edit.setText(global_saved_parameters['speed_movement'])
            self.probing_depth_label.setVisible(True)
            self.probing_depth_edit.setVisible(True)
            self.probing_depth_edit.setText(global_saved_parameters['probing_depth'])
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

            self.cutting_height_label.setVisible(True)
            self.cutting_height_edit.setVisible(True)
            self.cutting_height_edit.setText(global_saved_parameters['cutting_height'])
            self.piercing_height_label.setVisible(True)
            self.piercing_height_edit.setVisible(True)
            self.piercing_height_edit.setText(global_saved_parameters['piercing_height'])
            self.piercing_time_label.setVisible(True)
            self.piercing_time_edit.setVisible(True)
            self.piercing_time_edit.setText(global_saved_parameters['piercing_time'])
            self.floating_height_label.setVisible(True)
            self.floating_height_edit.setVisible(True)
            self.floating_height_edit.setText(global_saved_parameters['floating_height'])

            self.floating_height_cone_label.setVisible(False)
            self.floating_height_cone_edit.setVisible(False)
            self.total_depth_of_cutting_label.setVisible(False)
            self.total_depth_of_cutting_edit.setVisible(False)
            self.depth_of_cutting_per_pass_label.setVisible(False)
            self.depth_of_cutting_per_pass_edit.setVisible(False)
            self.probing_depth_label.setVisible(False)
            self.probing_depth_edit.setVisible(False)

        elif current_tool == "stożek":
            #self.cone_power_label.setVisible(True)
            #self.cone_power_edit.setVisible(True)
            #self.cone_power_edit.setText(global_saved_parameters['cone_power'])
            #self.cone_speed_label.setVisible(True)
            #self.cone_speed_edit.setVisible(True)
            #self.cone_speed_edit.setText(global_saved_parameters['cone_speed'])

            self.cutting_speed_label.setVisible(True)
            self.cutting_speed_edit.setVisible(True)
            self.cutting_speed_edit.setText(global_saved_parameters['cutting_speed'])
            self.movement_speed_label.setVisible(True)
            self.movement_speed_edit.setVisible(True)
            self.movement_speed_edit.setText(global_saved_parameters['speed_movement'])
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

            

            self.floating_height_cone_label.setVisible(True)
            self.floating_height_cone_edit.setVisible(True)
            self.floating_height_cone_edit.setText(global_saved_parameters['floating_height_cone'])
            self.total_depth_of_cutting_label.setVisible(True)
            self.total_depth_of_cutting_edit.setVisible(True)
            self.total_depth_of_cutting_edit.setText(global_saved_parameters['total_depth_of_cutting'])
            self.depth_of_cutting_per_pass_label.setVisible(True)
            self.depth_of_cutting_per_pass_edit.setVisible(True)
            self.depth_of_cutting_per_pass_edit.setText(global_saved_parameters['depth_of_cutting_per_pass'])

            self.plasma_power_label.setVisible(False)
            self.plasma_power_edit.setVisible(False)
            self.plasma_speed_label.setVisible(False)
            self.plasma_speed_edit.setVisible(False)
            self.cone_power_label.setVisible(False)
            self.cone_power_edit.setVisible(False)
            self.cone_speed_label.setVisible(False)
            self.cone_speed_edit.setVisible(False)
            self.probing_depth_label.setVisible(False)
            self.probing_depth_edit.setVisible(False)
            self.cutting_height_label.setVisible(False)
            self.cutting_height_edit.setVisible(False)
            self.piercing_height_label.setVisible(False)
            self.piercing_height_edit.setVisible(False)
            self.piercing_time_label.setVisible(False)
            self.piercing_time_edit.setVisible(False)
            self.floating_height_label.setVisible(False)
            self.floating_height_edit.setVisible(False)
            
            



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
    def __init__(self, change_tab_func, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Generated G-code")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.change_tab_func = change_tab_func

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.description_edit = QLineEdit()  # Pole tekstowe do wpisania opisu gkodu
        self.description_edit.setPlaceholderText("Wprowadź opis G kodu...")
        layout.addWidget(self.description_edit)

        simulate_button = QPushButton("Symuluj")
        layout.addWidget(simulate_button)
        simulate_button.clicked.connect(self.simulate_clicked)

        save_button = QPushButton("Zapisz")
        layout.addWidget(save_button)
        save_button.clicked.connect(self.save_clicked)

        save_to_db_button = QPushButton("Zapisz do bazy")
        layout.addWidget(save_to_db_button)
        save_to_db_button.clicked.connect(self.save_to_db_clicked)

        self.setLayout(layout)

    def set_generated_gcode(self, generated_gcode):
        self.generated_gcode = generated_gcode
        self.text_edit.setText(generated_gcode)

    def simulate_clicked(self):
        self.change_tab_func(2, self.text_edit.toPlainText())
        self.close()

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

    def save_to_db_clicked(self):
        # Pobierz opis z pola tekstowego
        description = self.description_edit.text()

        # Generowanie losowego ciągu znaków w systemie szesnastkowym
        random_hex_string = secrets.token_hex(4)  # Ustaw długość ciągu na 4 bajty (8 znaków)

        gcode_filename = f"g{random_hex_string}.gcode"
        gcode_filepath = os.path.join("./g_code/", gcode_filename)
        
        with open(gcode_filepath, 'w') as file:
            file.write(self.generated_gcode)

        # Zapisz rekord do bazy danych
        conn = sqlite3.connect('./db/database.db')
        cursor = conn.cursor()

        try:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO GcodeHistory (generation_date, file_path, description) VALUES (?, ?, ?)",
                           (current_date, gcode_filepath, description))
            conn.commit()
            print("Record saved to GcodeHistory table successfully.")
            QMessageBox.information(self, "Success", "G-code and record saved successfully.")
        except Exception as e:
            conn.rollback()
            print(f"Error occurred while saving record to database: {str(e)}")
            QMessageBox.warning(self, "Error", f"Error occurred while saving record to database: {str(e)}")

        conn.close()

class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setRenderHints(
            QPainter.Antialiasing |
            QPainter.SmoothPixmapTransform |
            QPainter.TextAntialiasing
        )
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Uzyskanie aktualnych skal
        oldScale = self.transform().m11()

        # Ograniczenie poziomu zoomu
        if event.angleDelta().y() > 0:
            scaleFactor = zoomInFactor
        else:
            scaleFactor = zoomOutFactor

        # Nowa skala po zastosowaniu zoomu
        newScale = oldScale * scaleFactor

        if 0.000001 < newScale < 1000:  # Ogranicz zakres skalowania np. od 0.05x do 10x
            self.scale(scaleFactor, scaleFactor)
    
    def resetZoom(self):
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def zoomIn(self):
        self.scale(1.2, 1.2)

    def zoomOut(self):
        self.scale(1 / 1.2, 1 / 1.2)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)
        super().mouseReleaseEvent(event)

class RightPart(QWidget):
    rotation_displayed = pyqtSignal(float)
    
    def __init__(self, change_tab_func):
        super().__init__()
        layout = QVBoxLayout()  # Layout to arrange widgets vertically

        self.change_tab_func = change_tab_func
        self.FigureList = namedtuple('FigureList', ['x_coords', 'y_coords', 'collides', 'index'])
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        layout.addWidget(self.progress_bar)

        # ComboBox for layer selection
        self.layerComboBox = QComboBox()
        self.layerComboBox.currentIndexChanged.connect(self.display_selected_layer)
        layout.addWidget(self.layerComboBox)  # Add ComboBox right after ProgressBar

        # Create and configure QLabel for summary text
        self.summary_label = QLabel()
        self.summary_label.setText("Podsumowanie")  # Initial text    
        layout.addWidget(self.summary_label)

        # Graphics View with zooming capability
        self.graphics_view = ZoomableGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        layout.addWidget(self.graphics_view)

        zoom_button_layout = QHBoxLayout()
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.clicked.connect(self.graphics_view.zoomIn)
        zoom_button_layout.addWidget(self.zoom_in_button)
        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.clicked.connect(self.graphics_view.zoomOut)
        zoom_button_layout.addWidget(self.zoom_out_button)
        self.reset_zoom_button = QPushButton("Reset Zoom")
        self.reset_zoom_button.clicked.connect(self.graphics_view.resetZoom)
        zoom_button_layout.addWidget(self.reset_zoom_button)
        self.grid_button = QPushButton('Toggle Grid', self)
        self.grid_button.clicked.connect(self.toggle_grid)
        zoom_button_layout.addWidget(self.grid_button)
        self.grid_displayed = False
        layout.addLayout(zoom_button_layout)

        button_layout = QHBoxLayout()
        # 'Stop Nesting' Button
        self.stop_nesting_button = QPushButton("Stop Nesting")
        self.stop_nesting_button.clicked.connect(self.request_stop)
        button_layout.addWidget(self.stop_nesting_button)

        # 'Generuj G-code' Button
        self.open_tool_parameters_button = QPushButton("Generuj G-code")
        self.open_tool_parameters_button.clicked.connect(self.open_tool_parameters_dialog_right)
        button_layout.addWidget(self.open_tool_parameters_button)        

        # Add the button layout to the main vertical layout
        layout.addLayout(button_layout)

        # Set the layout for the widget
        self.setLayout(layout)

        # Initialization
        self.inputPoints = []
        self.svg_to_mm = 0.352777778  # Conversion factor from SVG units to mm
        self.volume = None
        self.stop_requested = False
        self.figures = []

    
    def request_stop(self):
        self.stop_requested = True
        self.progress_bar.setValue(0)
        print("Stop requested. The nesting process will be terminated after the current iteration.")
    def stop_nesting(self):
            self.nesting_process.request_stop()
            
    # metoda przyjmująca parametry narzędzia wybrane podczas konifguracji nestingu 
    def sended_tool_param(self, saved_parameters):
        
        # Deklaracja zmiennej globalnej
        global global_saved_parameters
        
        # Przypisanie wartości zmiennej globalnej
        global_saved_parameters = saved_parameters
        
    def open_tool_parameters_dialog_right(self):
        dialog = ToolParametersDialog()

        if dialog.exec_():

            if (global_saved_parameters['type_tool']) == "laser":

                # Tworzenie i konfiguracja okna dialogowego
                custom_dialog = CustomDialog(self.change_tab_func)
                custom_dialog.setModal(True)

                # Pobierz parametry narzędzia od użytkownika
                cutting_speed = float(dialog.cutting_speed_edit.text())
                movement_speed = float(dialog.movement_speed_edit.text())
                #depth = float(dialog.depth_edit.text())
                dwell_time = float(dialog.dwell_edit.text())
                unit = dialog.unit_edit.text()
                custom_header = [dialog.header_edit.text()]
                custom_footer = [dialog.footer_edit.text()]

                # Wygeneruj G-kod z pliku SVG
                gcode_compiler = Compiler(
                    interfaces.Gcode,   
                    cutting_speed=cutting_speed,
                    movement_speed=movement_speed,
                    pass_depth=0,  #tego nie ma w kodzie
                    dwell_time=dwell_time,
                    unit=unit,
                    custom_header=custom_header,
                    custom_footer=custom_footer
                )

                curves = parse_file("output.svg")
                gcode_compiler.append_curves(curves)

                # Odczytaj wygenerowany G-kod
                generated_gcode = gcode_compiler.compile()




                def remove_lines_range(generated_gcode, start_line, end_line):
                    lines = generated_gcode.split('\n')
                    modified_lines = []

                    for i, line in enumerate(lines, start=1):
                        if start_line <= i <= end_line:
                            continue  # Pomijamy linie z zakresu, które mają być usunięte
                        modified_lines.append(line)

                    return '\n'.join(modified_lines)


                # Przykładowe użycie
                modified_gcode1 = remove_lines_range(generated_gcode, 6, 26)


                def remove_lines_range_reverse(generated_gcode, start_line, end_line):
                    lines = generated_gcode.split('\n')
                    total_lines = len(lines)
                    modified_lines = []

                    for i in range(total_lines - 1, -1, -1):
                        if start_line <= total_lines - i <= end_line:
                            continue  # Pomijamy linie z zakresu, które mają być usunięte
                        modified_lines.insert(0, lines[i])

                    return '\n'.join(modified_lines)


                # Przykładowe użycie
                modified_gcode2 = remove_lines_range_reverse(modified_gcode1, 2, 18)





                # Ustaw wygenerowany G-kod w oknie dialogowym
                custom_dialog.set_generated_gcode(modified_gcode2)

                custom_dialog.exec_()

                print("Canceled generating G-code")

            elif (global_saved_parameters['type_tool']) == "plazma":
                # tutaj generowanie G-codu dla plazmy

                # Tworzenie i konfiguracja okna dialogowego
                custom_dialog = CustomDialog(self.change_tab_func)
                custom_dialog.setModal(True)

                # Pobierz parametry narzędzia od użytkownika
                cutting_speed = float(dialog.cutting_speed_edit.text())
                movement_speed = float(dialog.movement_speed_edit.text())
                #depth = float(dialog.depth_edit.text())
                dwell_time = float(dialog.dwell_edit.text())
                unit = dialog.unit_edit.text()
                custom_header = [dialog.header_edit.text()]
                custom_footer = [dialog.footer_edit.text()]

                # Wygeneruj G-kod z pliku SVG
                gcode_compiler = Compiler(
                    interfaces.Gcode,
                    cutting_speed=cutting_speed,
                    movement_speed=movement_speed,
                    pass_depth=0, # tego nie ma w g-kodzie
                    dwell_time=dwell_time,
                    unit=unit,
                    custom_header=custom_header,
                    custom_footer=custom_footer
                )

                curves = parse_file("output.svg")
                gcode_compiler.append_curves(curves)

                # Odczytaj wygenerowany G-kod
                generated_gcode = gcode_compiler.compile()


                # Pobierz parametry narzędzia od użytkownika potrzebne do modyfikacji G kodu dla narzędzia plazma
                piercing_height = dialog.piercing_height_edit.text()
                piercing_time = dialog.piercing_time_edit.text()
                #cutting_height = dialog.cutting_height_edit.text()
                #cutting_height = float(dialog.cutting_height_edit.text()) + 8.21
                cutting_height = str(round(float(dialog.cutting_height_edit.text()) + 6.21, 2))
                floating_height = dialog.floating_height_edit.text()
                probing_depth = dialog.probing_depth_edit.text()

                # Modyfikacja wygenerowanego G-kodu
                modified_lines = []
                for line in generated_gcode.split('\n'):
                    # Usuń "S255" z każdej linii
                    modified_tokens = [token for token in line.split() if 'S255' not in token]
                    modified_line = ' '.join(modified_tokens)
                    # Dodaj nowe linie przed linią z "M3"
                    if 'M3' in modified_line:
                        modified_lines.append("G0 Z5")  # Linia (a)
                        modified_lines.append(f"G38.2 Z{probing_depth} F100")  # Głębokość sondowania (probing_depth)
                        modified_lines.append("G10 L20 P1 Z0")  # Linia (c)
                        modified_lines.append("G1 Z8.21 F1000")  # Linia (d)
                        modified_lines.append("G10 L20 P1 Z0")  # Linia (e)
                        modified_lines.append(f"G0 Z{piercing_height} F2500")  # Ustawienie wysokośći przekłucia (piercing height)
                        modified_lines.append(modified_line)  # Dodaj oryginalną linię z "M3" po dodaniu nowych linii
                        modified_lines.append("M300")  # Waiting for ARC OK
                        modified_lines.append(f"G4 P{piercing_time}")  # Czas przekłucia [ms] piercing time
                        modified_lines.append(f"G0 Z{cutting_height} F700")  # Wysokość cięcia cutting height
                    elif 'M5' in modified_line:
                        modified_lines.append(modified_line)  # Dodaj oryginalną linię z "M5"
                        modified_lines.append(f"G0 Z{floating_height} F2500")  # Dodaj wysokość dryfu (flying height)
                    else:
                        modified_lines.append(modified_line)

                generated_gcode = '\n'.join(modified_lines)


                def remove_lines_range(generated_gcode, start_line, end_line):
                    lines = generated_gcode.split('\n')
                    modified_lines = []

                    for i, line in enumerate(lines, start=1):
                        if start_line <= i <= end_line:
                            continue  # Pomijamy linie z zakresu, które mają być usunięte
                        modified_lines.append(line)

                    return '\n'.join(modified_lines)


                # Przykładowe użycie
                modified_gcode1 = remove_lines_range(generated_gcode, 6, 46)


                def remove_lines_range_reverse(generated_gcode, start_line, end_line):
                    lines = generated_gcode.split('\n')
                    total_lines = len(lines)
                    modified_lines = []

                    for i in range(total_lines - 1, -1, -1):
                        if start_line <= total_lines - i <= end_line:
                            continue  # Pomijamy linie z zakresu, które mają być usunięte
                        modified_lines.insert(0, lines[i])

                    return '\n'.join(modified_lines)


                # Przykładowe użycie
                modified_gcode2 = remove_lines_range_reverse(modified_gcode1, 2, 57)



                # Ustaw wygenerowany G-kod w oknie dialogowym
                custom_dialog.set_generated_gcode(modified_gcode2)

                custom_dialog.exec_()

                print("Canceled generating G-code")


            elif (global_saved_parameters['type_tool']) == "stożek":
                
                # Tworzenie i konfiguracja okna dialogowego
                custom_dialog = CustomDialog(self.change_tab_func)
                custom_dialog.setModal(True)

                # Pobierz parametry narzędzia od użytkownika
                cutting_speed = float(dialog.cutting_speed_edit.text())
                movement_speed = float(dialog.movement_speed_edit.text())
                #depth = float(dialog.depth_edit.text())
                dwell_time = float(dialog.dwell_edit.text())
                unit = dialog.unit_edit.text()
                custom_header = [dialog.header_edit.text()]
                custom_footer = [dialog.footer_edit.text()]

                # Wygeneruj G-kod z pliku SVG
                gcode_compiler = Compiler(
                    interfaces.Gcode,   
                    cutting_speed=cutting_speed,
                    movement_speed=movement_speed,
                    pass_depth=0, # tego nie ma w g-kodzie
                    dwell_time=dwell_time,
                    unit=unit,
                    custom_header=custom_header,
                    custom_footer=custom_footer
                )

                curves = parse_file("output.svg")
                gcode_compiler.append_curves(curves)

                # Odczytaj wygenerowany G-kod
                generated_gcode = gcode_compiler.compile()


                # Pobierz parametry narzędzia od użytkownika potrzebne do modyfikacji G kodu dla narzędzia stożek ---- poniżej jeszcze puste
            
                #to wysokość dryfu dla frezu                    floating_height_cone
                #głębokość wiercenia                            total_depth_of_cutting
                #decrement_step do co ile ma się obniżać  frez  depth_of_cutting_per_pass

                floating_height_cone = dialog.floating_height_cone_edit.text()
                floating_height_cone_int = int(floating_height_cone)

                total_depth_of_cutting = dialog.total_depth_of_cutting_edit.text()
                total_depth_of_cutting_int = int(total_depth_of_cutting)

                depth_of_cutting_per_pass = dialog.depth_of_cutting_per_pass_edit.text()
                depth_of_cutting_per_pass_int = int(depth_of_cutting_per_pass)

                quantity_of_copies_line_int = total_depth_of_cutting_int // depth_of_cutting_per_pass_int
                if total_depth_of_cutting_int % depth_of_cutting_per_pass_int != 0:
                    quantity_of_copies_line_int += 1


                def remove_duplicate_lines(generated_gcode):
                    lines = generated_gcode.split('\n')
                    modified_lines = []

                    previous_line = None
                    for line in lines:
                        if line == previous_line:
                            continue  # Pomijaj linie, które są identyczne z poprzednią
                        modified_lines.append(line)
                        previous_line = line

                    return '\n'.join(modified_lines)
                
                
                modified_gcode = remove_duplicate_lines(generated_gcode)




                def duplicate_lines_between_m3_and_g4(generated_gcode, duplicates=1):
                    lines = generated_gcode.split('\n')
                    modified_lines = []

                    is_between_m3_and_g4 = False
                    lines_to_duplicate = []

                    for line in lines:
                        if 'M3 S255' in line:
                            is_between_m3_and_g4 = True
                            lines_to_duplicate.clear()  # Wyczyść listę linii do zduplikowania
                        elif 'G4 P29.0' in line:
                            is_between_m3_and_g4 = False
                            # Zduplikuj linie między "M3 S255" a "G4 P29.0"
                            for _ in range(duplicates):
                                for duplicate_line in lines_to_duplicate:
                                    modified_lines.append(duplicate_line)
                        elif is_between_m3_and_g4:
                            lines_to_duplicate.append(line)

                        modified_lines.append(line)

                    return '\n'.join(modified_lines)

                # Użycie:
                #modified_gcode2 = duplicate_lines_between_m3_and_g4(modified_gcode, #total_depth_of_cutting_int-1) #duplicates to głębokość wiercenia
                
                modified_gcode2 = duplicate_lines_between_m3_and_g4(modified_gcode, quantity_of_copies_line_int-1) #duplicates to głębokość wiercenia



                def add_custom_command(generated_gcode):
                    lines = generated_gcode.split('\n')
                    modified_lines = []

                    is_between_m3_and_m5 = False

                    for line in lines:
                        if 'M3 S255' in line:
                            is_between_m3_and_m5 = True
                            modified_lines.append(line)  # Dodaj linię "M3 S255" do wynikowego kodu
                        elif 'M5' in line:
                            is_between_m3_and_m5 = False
                            modified_lines.append(line)  # Dodaj linię "M5" do wynikowego kodu
                        elif is_between_m3_and_m5 and line.startswith('G1 F'):
                            modified_lines.append('G0 Z-250')  # Dodaj linię "G0 Z-250" przed linią "G1 F"
                            modified_lines.append(line)
                        else:
                            modified_lines.append(line)

                    return '\n'.join(modified_lines)

                # Użycie:
                modified_gcode3 = add_custom_command(modified_gcode2)


                def decrement_custom_command(generated_gcode, decrement_step=1):
                    lines = generated_gcode.split('\n')
                    modified_lines = []

                    is_between_m3_and_m5 = False
                    z_counter = decrement_step  # Inicjalizuj licznik Z

                    for line in lines:
                        if 'M3 S255' in line:
                            is_between_m3_and_m5 = True
                            modified_lines.append(line)  # Dodaj linię "M3 S255" do wynikowego kodu
                        elif 'M5' in line:
                            is_between_m3_and_m5 = False
                            modified_lines.append(line)  # Dodaj linię "M5" do wynikowego kodu
                            z_counter = decrement_step  # Zresetuj licznik po zakończeniu sekcji między "M3 S255" a "M5"
                        elif is_between_m3_and_m5 and 'G0 Z-250' in line:  # Możesz dostosować ten warunek do Twoich potrzeb
                            modified_lines.append(f'G0 Z-{z_counter}')
                            z_counter += decrement_step
                        else:
                            modified_lines.append(line)

                    return '\n'.join(modified_lines)

                # Użycie:
                modified_gcode4 = decrement_custom_command(modified_gcode3, depth_of_cutting_per_pass_int) #decrement_step do co ile ma się obniżać  frez



                def add_z_reset(generated_gcode):
                    lines = generated_gcode.split('\n')
                    modified_lines = []

                    for line in lines:
                        modified_lines.append(line)
                        if 'M5' in line:
                            modified_lines.append(f'G0 Z{floating_height_cone_int}') # G0 Z{} to wysokość dryfu dla frezu

                    return '\n'.join(modified_lines)

                # Użycie:
                modified_gcode5 = add_z_reset(modified_gcode4)


                def replace_z_value(g_code, new_z_value=-100):
                    new_g_code = []
                    min_z = None
                    # Znajdź wszystkie wartości Z i zaktualizuj najniższą wartość Z
                    for line in g_code.split('\n'):
                        if line.startswith('G0') or line.startswith('G1'):
                            if 'Z' in line:
                                parts = line.split('Z')
                                for part in parts[1:]:
                                    z_value_str = part.split()[0]
                                    if z_value_str:  # Sprawdź, czy znaleziono wartość Z
                                        z_value = float(z_value_str)
                                        if min_z is None or z_value < min_z:
                                            min_z = z_value
                    
                    # Zastąp najniższą wartość Z wartością new_z_value
                    for line in g_code.split('\n'):
                        if line.startswith('G0') or line.startswith('G1'):
                            if 'Z' in line:
                                parts = line.split('Z')
                                new_line = parts[0]
                                for part in parts[1:]:
                                    z_value_str = part.split()[0]
                                    if z_value_str:  # Sprawdź, czy znaleziono wartość Z
                                        z_value = float(z_value_str)
                                        if z_value == min_z:
                                            new_line += f'Z{new_z_value*-1}' + part[len(z_value_str):]
                                        else:
                                            new_line += 'Z' + z_value_str + part[len(z_value_str):]
                                new_g_code.append(new_line)
                            else:
                                new_g_code.append(line)
                        else:
                            new_g_code.append(line)
                    
                    return '\n'.join(new_g_code)

                # Przykładowe użycie
                modified_gcode6 = replace_z_value(modified_gcode5, total_depth_of_cutting_int)
                print(modified_gcode6)



                # zmienne do ilości usuwanych linii
                to_line = 29 + (quantity_of_copies_line_int - 1) * 14
                print("To jest linia to_line:", to_line)

                def remove_lines_range(generated_gcode, start_line, end_line):
                    lines = generated_gcode.split('\n')
                    modified_lines = []

                    for i, line in enumerate(lines, start=1):
                        if start_line <= i <= end_line:
                            continue  # Pomijamy linie z zakresu, które mają być usunięte
                        modified_lines.append(line)

                    return '\n'.join(modified_lines)


                # Przykładowe użycie
                modified_gcode7 = remove_lines_range(modified_gcode6, 6, to_line)


                # zmienne do ilości usuwanych linii reverse
                to_line_reverse = 25 + (quantity_of_copies_line_int - 1) * 6
                print("To jest linia to_line:", to_line)

                def remove_lines_range_reverse(generated_gcode, start_line, end_line):
                    lines = generated_gcode.split('\n')
                    total_lines = len(lines)
                    modified_lines = []

                    for i in range(total_lines - 1, -1, -1):
                        if start_line <= total_lines - i <= end_line:
                            continue  # Pomijamy linie z zakresu, które mają być usunięte
                        modified_lines.insert(0, lines[i])

                    return '\n'.join(modified_lines)





                # Przykładowe użycie
                modified_gcode8 = remove_lines_range_reverse(modified_gcode7, 2, to_line_reverse)


    
                # Ustaw wygenerowany G-kod w oknie dialogowym
                custom_dialog.set_generated_gcode(modified_gcode8)

                custom_dialog.exec_()

                print("Canceled generating G-code")
            

        print("Canceled generating G-code")

    def update(self, space_between_objects, explore_holes, parallel, optimization, accuracy, rotations, starting_point):
        global global_space_between_objects, global_explore_holes, global_parallel, global_optimization, global_accuracy, global_rotations, global_starting_point
        # Update global variables
        global_space_between_objects = space_between_objects
        global_explore_holes = explore_holes
        global_parallel = parallel
        global_optimization = optimization
        global_accuracy = accuracy # niższa wartość -> wyższa dokładność
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
       # print(f"Wygenerowane obroty: [{rotations_text}] rad")
        return rotations
    
    def apply_trans_and_rot(self, points, trans_x, trans_y, rotation):
        transformed_points = []
        cos_rot = np.cos(rotation)
        sin_rot = np.sin(rotation)
        for point in points:
            rotated_x = point[0] * cos_rot - point[1] * sin_rot
            rotated_y = point[0] * sin_rot + point[1] * cos_rot
            transformed_points.append((rotated_x + trans_x + self.volume.width() / 2, rotated_y + trans_y + self.volume.height() / 2))
        return transformed_points


    def configure_nesting_parameters(self, rotations):
        nfp_config = NfpConfig()
        # Sposób ułożenia obiektów
        alignment_map = {
            "CENTER": NfpConfig.Alignment.CENTER,
            "BOTTOM_LEFT": NfpConfig.Alignment.BOTTOM_LEFT,
            "BOTTOM_RIGHT": NfpConfig.Alignment.BOTTOM_RIGHT,
            "TOP_LEFT": NfpConfig.Alignment.TOP_LEFT,
            "TOP_RIGHT": NfpConfig.Alignment.TOP_RIGHT,
            "DONT_ALIGN": NfpConfig.Alignment.DONT_ALIGN
        }
        nfp_config.alignment = alignment_map.get(global_optimization, NfpConfig.Alignment.DONT_ALIGN)
        nfp_config.starting_point = alignment_map.get(global_starting_point, NfpConfig.Alignment.DONT_ALIGN)

        # Obroty obiektów
        if rotations is None or global_rotations == 0:
            nfp_config.rotations = []
        else:
            nfp_config.rotations = rotations

        # Dokładność
        nfp_config.accuracy = global_accuracy

        # Wielowątkowość
        nfp_config.parallel = global_parallel

        # Eksploracja otworów
        nfp_config.explore_holes = global_explore_holes

        return nfp_config
    
    def display_selected_layer(self, index):
        # Funkcja do wyświetlania wybranej warstwy
        for i, canvas in enumerate(self.canvas_layers):
            canvas.setVisible(i == index)  # Ustaw widoczność odpowiedniej warstwy

        pen = QPen(Qt.black)
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(2)
        pen.setCosmetic(True)

        font = QFont()
        min_val = int(min(self.volume.width(), self.volume.height()) / 100)
        font.setPointSize(min_val)

        self.scene.clear()

        # Sprawdź, czy index jest w zakresie i zapisz obiekt Figure do pliku SVG
        if 0 <= index < len(self.figures):
            fig = self.figures[index]
            svg_filename = "output.svg"  # Stała nazwa pliku
            fig.set_size_inches(self.volume.width() / 72, self.volume.height() / 72)
            fig.savefig(svg_filename, format='svg', bbox_inches='tight', pad_inches=0)
            # fig.set_size_inches(8, 8)
            print(f"SVG version '{index + 1}' saved as '{svg_filename}'.") 
            self.draw_nesting_box()
            pen.setColor(QColor('red').lighter(175))
            self.scene.addRect(self.figuresListCorrect[index][1], self.figuresListCorrect[index][2], self.figuresListCorrect[index][3], self.figuresListCorrect[index][4], pen)
            pen.setColor(Qt.black)
            label_flag = []
            collision_count = 0
            for figure in self.figuresListCorrect[index][0]:
                if figure.collides:
                    pen.setColor(QColor('red').lighter(150))
                    for i in range(len(figure.x_coords) - 1):
                        self.scene.addLine(figure.x_coords[i], figure.y_coords[i], figure.x_coords[i+1], figure.y_coords[i+1], pen)
                    if figure.index not in label_flag:
                        label = QGraphicsTextItem(f"{figure.index + 1}")
                        label.setFont(font)
                        label.setPos(figure.x_coords[0], figure.y_coords[0])
                        label.setDefaultTextColor(QColor('red').lighter(75))
                        self.scene.addItem(label)
                        label_flag.append(figure.index)
                        collision_count += 1
                else:
                    pen.setColor(Qt.black)
                    for i in range(len(figure.x_coords) - 1):
                        self.scene.addLine(figure.x_coords[i], figure.y_coords[i], figure.x_coords[i+1], figure.y_coords[i+1], pen)

            if collision_count > 0:
                self.summary_label.setStyleSheet("color: red")
                col_summary_text = f"Number of collisions detected: {collision_count}.\nConsider removing some of the nested objects"
            else:
                col_summary_text = "No collisions detected\n"
                self.summary_label.setStyleSheet("color: green")
            self.summary_label.setText(col_summary_text)


    def draw_nesting_box(self):
        font = QFont()
        min_val = int(min(self.volume.width(), self.volume.height()) / 100)
        font.setPointSize(min_val)

        pen = QPen(Qt.black)
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(2)
        pen.setCosmetic(True)

        # Calculate 10% of the width and height
        scale_width = self.volume.width() * 0.1
        scale_height = self.volume.height() * 0.1

        # Create a new pen for the grid lines
        grid_pen = QPen(Qt.lightGray)
        grid_pen.setColor(QColor('gray').lighter(180))
        grid_pen.setStyle(Qt.SolidLine)
        grid_pen.setWidth(1)
        grid_pen.setCosmetic(True)

        shorter_side = min(self.volume.width(), self.volume.height())
        scale = shorter_side * 0.1

        for i in range(int(self.volume.height() / shorter_side * 10), -1, -1):
            self.scene.addLine(0, (int(self.volume.height() / shorter_side * 10) - i) * scale, -min_val, (int(self.volume.height() / shorter_side * 10) - i) * scale, pen)
            label_value = i * 0.1 * shorter_side / 100
            label = QGraphicsTextItem(f"{label_value:.0f}mm")
            label.setFont(font)
            label.setPos(-label.boundingRect().width() - (1.5 * min_val), (int(self.volume.height() / shorter_side * 10) - i) * scale - (0.75 * min_val))
            self.scene.addItem(label)

            if i < int(self.volume.height() / shorter_side * 10) and self.grid_displayed:
                for j in range(1, 11):
                    self.scene.addLine(0, ((int(self.volume.height() / shorter_side * 10) - i) - j * 0.1) * scale, self.volume.width(), ((int(self.volume.height() / shorter_side * 10) - i) - j * 0.1) * scale, grid_pen)


        for i in range(int(self.volume.width() / shorter_side * 10) + 1):
            self.scene.addLine(i * scale, self.volume.height(), i * scale, self.volume.height() + min_val, pen)
            label_value = i * 0.1 * shorter_side / 100 
            label = QGraphicsTextItem(f"{label_value:.0f}mm")
            label.setFont(font)
            label.setPos(i * scale - label.boundingRect().width() / 2, self.volume.height() + (1.5 * min_val))
            self.scene.addItem(label)

            if i < int(self.volume.width() / shorter_side * 10) and self.grid_displayed:
                for j in range(1, 11):
                    self.scene.addLine((i + j * 0.1) * scale, 0, (i + j * 0.1) * scale, self.volume.height(), grid_pen)

        self.scene.addRect(0, 0, self.volume.width(), self.volume.height(), pen)

    def toggle_grid(self):
        self.grid_displayed = not self.grid_displayed
        self.scene.clear()
        index = self.layerComboBox.currentIndex()
        if index >= 0:
            self.draw_nesting_box()
            self.display_selected_layer(index)

    async def display_file(self, file_paths, width, height, checked_paths):
        start_time = time.time()
        self.figures.clear()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        # self.scene.clear()
        if any(var is None for var in [global_space_between_objects, global_optimization, global_accuracy, global_rotations, global_starting_point]):
            QMessageBox.critical(None, "Error", "Not all nesting parameters are configured.\nPlease configure all nesting parameters before calling the nesting function.")
            return

        self.figuresList = []
        self.figuresListCorrect = []

        self.progress_bar.setMaximum(global_rotations - 1)
        await asyncio.sleep(0)
        self.inputPoints = []
        file_to_parse = Parser(checked_paths)
        returned_values = file_to_parse.parse_svg()
        returned_input_points, returned_svg_points = returned_values
        self.inputPoints += returned_input_points
        self.volume = Box(width, height)
        self.canvas_layers = []
        self.layerComboBox.clear()
        self.best_configurations = []  # Lista do przechowywania najlepszych konfiguracji

        min_area = float('inf')

        if not self.check_fit_in_volume(self.inputPoints, width, height):
            return

        spacing = int(global_space_between_objects * self.svg_to_mm * 10)
        rotations = self.generate_rotations(global_rotations) if global_rotations > 0 else []

        nfp_config = self.configure_nesting_parameters(rotations)

        min_area = float('inf')
        min_area_rotation = 0
        min_area_index = -1
        
        for index, item in enumerate(self.inputPoints):
            print(item.isContourConvex())
            if not item.isContourConvex():
                box_points = []
                box = item.boundingBox()
                # print(box.minCorner().x(), box.minCorner().y(), box.maxCorner().x(), box.maxCorner().y())
                box_points.append(Point(box.minCorner().x(), box.minCorner().y()))
                box_points.append(Point(box.minCorner().x(), box.maxCorner().y()))
                box_points.append(Point(box.maxCorner().x(), box.maxCorner().y()))
                box_points.append(Point(box.maxCorner().x(), box.minCorner().y()))
                box_points.append(Point(box.minCorner().x(), box.minCorner().y()))
                self.inputPoints[index] = Item(box_points)

        last_collision_count = 0
        for index, rotation in enumerate(rotations):
            await asyncio.sleep(0)
            if self.stop_requested:
                print("Nesting process stopped.")
                self.stop_requested = False
                break

            self.figuresList = []

            nfp_config.rotations = [rotation]
            num_bins = nest(self.inputPoints, self.volume, spacing, nfp_config)
            
            pen = QPen(Qt.black)
            pen.setStyle(Qt.SolidLine)
            pen.setWidth(2)
            pen.setCosmetic(True)

            self.current_pos = (0, 0)

            self.progress_bar.setValue(index)

            # Prepare plot for visualization
            # fig.set_size_inches(self.volume.width() / 72, self.volume.height() / 72)
            fig = Figure(figsize=(self.volume.width() / 72, self.volume.height() / 72), tight_layout={'pad': 0})
            ax = fig.add_subplot(111)
            ax.set_aspect('equal')
            ax.set_xlim([0, self.volume.width()])
            ax.set_ylim([0, self.volume.height()])
            ax.set_xticks([])
            ax.set_yticks([])

            min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')

            best_area = float('inf')

            # Initialize summary text
            col_summary_text = ""
            summary_report = ""
            # List to store collision pairs
            seen_collisions = set()

            # Iterate through input points
            last_collision_count = 0
            for i, item1 in enumerate(self.inputPoints):
                await asyncio.sleep(0)
                transItem1 = item1.transformedShape()
                for j, item2 in enumerate(self.inputPoints):
                    transItem2 = item2.transformedShape()
                    if i < j and Item.intersects(transItem1, transItem2):  # Ensure i < j to avoid duplicates
                        collision_pair = (i, j) if i < j else (j, i)  # Ensure consistent pair order
                        if collision_pair not in seen_collisions:
                            seen_collisions.add(collision_pair)
                            # print(f"Collision detected between item {i} and item {j}")
                            # collision_count += 1
                            last_collision_count = len(seen_collisions)
                        else:
                            print(f"No collisions detected")


            for i, item in enumerate(self.inputPoints):
                await asyncio.sleep(0)

                # # testowe
                # x_values = []
                # y_values = []

                # transItem = item.transformedShape()

                # rows = len(transItem.toString().strip().split('\n')) - 1
                # for j in range(rows - 1):
                #     x_value = transItem.vertex(j).x() + self.volume.width() / 2
                #     y_value = transItem.vertex(j).y() + self.volume.height() / 2 
                #     x_values.append(x_value)
                #     y_values.append(y_value)
                # random_color = (random.random(), random.random(), random.random())
                # ax.plot(x_values, y_values, color=random_color, linewidth=1)

                
                paths = returned_svg_points[i].split('M')
                # paths = [path for path in paths if path]
                paths = ['M' + path for path in paths if path]
                
                for path in paths: 
                    parsed_path = parse_path(path)
                    item.resetTransformation()
                    x_points, y_points = [], []
                    for segment in parsed_path:
                        await asyncio.sleep(0)
                        # x_points, y_points = [], []
                        for t in np.linspace(0, 1, num=80):
                            point = segment.point(t)
                            transformed_point = self.apply_trans_and_rot([(point.real * 100 * self.svg_to_mm, point.imag * 100 * self.svg_to_mm)], item.translation().x(), item.translation().y(), item.rotation())[0]
                            x_points.append(transformed_point[0])
                            y_points.append(transformed_point[1])
                    
                        # Determine if the current item is involved in a collision
                        collides = any((i in pair) for pair in seen_collisions)
                        

                        self.figuresList.append(self.FigureList(x_coords=x_points, y_coords=y_points, collides=collides, index=i))

                    if collides:
                        ax.plot(x_points, y_points, color='red', linewidth=1)
                    else:
                        ax.plot(x_points, y_points, color='black', linewidth=1)


                    min_x, max_x = min(min_x, *x_points), max(max_x, *x_points)
                    min_y, max_y = min(min_y, *y_points), max(max_y, *y_points)
                        
                    if collides:
                        ax.text(np.mean(x_points), np.mean(y_points), str(i + 1), color='red', fontsize=12, ha='center', va='center')

            # Calculate the area of the bounding box
            bounding_box_width = max_x - min_x
            bounding_box_height = max_y - min_y
            bounding_box_area = bounding_box_width * bounding_box_height
            
            if bounding_box_area < min_area: #* 0.99:
                await asyncio.sleep(0)
                min_area = bounding_box_area
                self.best_configurations.append((rotation, bounding_box_area, index))
                min_area_rotation = rotation
                min_area_index = index

                
                # # self.scene.addLine(self.volume.width(), 0, self.volume.width(), self.volume.height(), pen)
                # # self.scene.addLine(self.volume.width(), self.volume.height(), 0, self.volume.height(), pen)
                # # self.scene.addLine(0, self.volume.height(), 0, 0, pen)
                # fig.set_size_inches(8, 8)
                # # Display the canvas only if it's the smallest bounding box found so far
                # canvas = FigureCanvas(fig)
                # #canvas.setVisible(False)  # Domyślnie niewidoczne
                # self.scene.addWidget(canvas)
                # canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                # self.canvas_layers.append(canvas)
                # #self.layerComboBox.addItem(f"Rotation {rotation:.2f} rad - Area {min_area:.2f}")



                # Draw the bounding box
                ax.add_patch(Rectangle((min_x, min_y), bounding_box_width, bounding_box_height, linewidth=1, edgecolor='r', facecolor='none'))

                self.figures.append(fig) 
                self.figuresListCorrect.append((self.figuresList, min_x, min_y, bounding_box_width, bounding_box_height))
                
                # Update collision report if new collisions were detected
                if last_collision_count == 0:
                    # No new collisions detected, maintain previous report
                    col_summary_text = "No collisions detected\n"
                    self.summary_label.setStyleSheet("color: green")
                else:
                    # Col detected
                    if last_collision_count > 0:
                        col_summary_text = f"Number of collisions detected: {last_collision_count + 1}.\nConsider removing some of the nested objects"
                        summary_report += "Detailed Collision Report:\n"
                        for pair in seen_collisions:
                            summary_report += f"  - Object {pair[0] + 1} collided with Object {pair[1] + 1} in nesting version {index + 1}\n "
                        self.summary_label.setStyleSheet("color: red")
                # Update the summary_label with the generated summary text
                self.summary_label.setText(col_summary_text)

                self.scene.clear()
                pen.setColor(QColor('red').lighter(175))
                self.scene.addRect(min_x, min_y, bounding_box_width, bounding_box_height, pen)
                pen.setColor(Qt.black)
                self.draw_nesting_box()
                font = QFont()
                min_val = int(min(self.volume.width(), self.volume.height()) / 100)
                font.setPointSize(min_val)
                label_flag = []
                for figure in self.figuresListCorrect[-1][0]:
                    if figure.collides:
                        pen.setColor(QColor('red').lighter(150))
                        for i in range(len(figure.x_coords) - 1):
                            self.scene.addLine(figure.x_coords[i], figure.y_coords[i], figure.x_coords[i+1], figure.y_coords[i+1], pen)
                        if figure.index not in label_flag:
                            label = QGraphicsTextItem(f"{figure.index + 1}")
                            label.setFont(font)
                            label.setPos(figure.x_coords[0], figure.y_coords[0])
                            label.setDefaultTextColor(QColor('red').lighter(75))
                            self.scene.addItem(label)
                            label_flag.append(figure.index)
                    else:
                        pen.setColor(Qt.black)
                        for i in range(len(figure.x_coords) - 1):
                            self.scene.addLine(figure.x_coords[i], figure.y_coords[i], figure.x_coords[i+1], figure.y_coords[i+1], pen)
                

                # # Update the scene and UI
                # self.scene.update()
                # QApplication.processEvents()

                # Zapisz SVG
                svg_filename = "output.svg"
                # fig.set_size_inches(self.volume.width() / 72, self.volume.height() / 72)
                # fig.savefig(svg_filename, format='svg', bbox_inches='tight', pad_inches=0)
                # fig.set_size_inches(8, 8)
            else:
                self.figuresList.pop()

            self.graphics_view.setRenderHint(QPainter.NonCosmeticDefaultPen)  # This line ensures that the line width remains constant when the view is scaled
            self.graphics_view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
            self.graphics_view.setTransformationAnchor(QGraphicsView.NoAnchor)  # This line disables the transformation anchor
            self.graphics_view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
            self.graphics_view.resetZoom()

        self.update_combobox_with_best_configurations()
        if min_area_index != -1:
            print(f"Minimum Bounding Box Area: {min_area:.2f} at Rotation {min_area_rotation:.2f} radians, Index {min_area_index}")
            #self.layerComboBox.setCurrentIndex(min_area_index)    
        end_time = time.time()  # Record the end time
        print(end_time - start_time)
            

    def update_combobox_with_best_configurations(self):
        # Sortowanie wyników według area od najmniejszej do największej
        self.best_configurations.sort(key=lambda x: x[1])
        #self.layerComboBox.clear()

        for i, (rotation, area, index) in enumerate(self.best_configurations):
            description = f"Version {i+1}"
            self.layerComboBox.addItem(description, userData=index)

        # Ustawienie najlepszej wersji jako domyślnej (najmniejsza area)
        if self.best_configurations:
            self.layerComboBox.setCurrentIndex(0)
            # self.display_selected_layer(0)

    def check_fit_in_volume(self, parsed_objects, width, height):
        global global_space_between_objects

        # Powiększ każdy obiekt o zadany bufor
        for item in parsed_objects:
            item.inflation(int(global_space_between_objects * 2))
        
        # Sumuj powierzchnie powiększonych obiektów
        total_required_area = sum(item.area() for item in parsed_objects)
        total_required_area += 48000000
        # Całkowita dostępna powierzchnia
        volume_area = width * height
        print("volume area:", volume_area)
        print("suma obiektów + powierzchnia między obiektami", total_required_area)
        
        # Sprawdź, czy wymagana powierzchnia nie przekracza dostępnej
        if total_required_area > volume_area:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("<font size='+2' color='red'>Błąd: Brak wystarczającej przestrzeni dla wszystkich obiektów.</font>")
            msg.setInformativeText(f"Minimalna wymagana powierzchnia: {total_required_area} jednostek kwadratowych.\n\n"
                                    "Suma powierzchni obiektów przekracza dostępną objętość. Proszę dostosować wymiary lub zmniejszyć liczbę obiektów.")
            msg.setWindowTitle("Błąd")
            msg.setStyleSheet("QMessageBox { background-color: white; }")
            msg.exec_()
            return False
        else:
            print("Powierzchnie poszczególnych obiektów:")
            for i, item in enumerate(parsed_objects):
                print(f"Obiekt {i + 1}: {item.area()}")  # Wyświetlanie powierzchni każdego obiektu
            return True
    
    def generate_gcode(self):
        # Open the tool parameters dialog
        self.open_tool_parameters_dialog_right()
    
    def format_x_ticks(self, x, pos):
        scaled_value = x / 100
        return f'{int(scaled_value)} mm' if scaled_value % 10 == 0 else ''

    def format_y_ticks(self, y, pos):
        scaled_value = y / 100
        return f'{int(scaled_value)} mm' if scaled_value % 10 == 0 else ''
