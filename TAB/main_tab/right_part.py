
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
import random
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pynest2d import NfpConfig, nest, Box
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

        self.probing_depth_label = QLabel("Głębokość sondowania:")  # brak w gcodzie
        self.probing_depth_edit = QLineEdit()
        self.layout.addWidget(self.probing_depth_label)
        self.layout.addWidget(self.probing_depth_edit)

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

        self.cutting_height_label = QLabel("Wysokość cięcia:")
        self.cutting_height_edit = QLineEdit()
        self.layout.addWidget(self.cutting_height_label)
        self.layout.addWidget(self.cutting_height_edit)

        self.piercing_height_label = QLabel("Wysokość przebicia:")
        self.piercing_height_edit = QLineEdit()
        self.layout.addWidget(self.piercing_height_label)
        self.layout.addWidget(self.piercing_height_edit)

        self.piercing_time_label = QLabel("Czas przebicia:")
        self.piercing_time_edit = QLineEdit()
        self.layout.addWidget(self.piercing_time_label)
        self.layout.addWidget(self.piercing_time_edit)

        self.floating_height_label = QLabel("Czas dryfu:")
        self.floating_height_edit = QLineEdit()
        self.layout.addWidget(self.floating_height_label)
        self.layout.addWidget(self.floating_height_edit)






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
            self.depth_label.setVisible(True)
            self.depth_edit.setVisible(True)
            self.depth_edit.setText(global_saved_parameters['cutting_depth'])
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


class RightPart(QWidget):
    rotation_displayed = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()  # Layout to arrange widgets vertically

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        layout.addWidget(self.progress_bar)

        # Graphics View
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        layout.addWidget(self.graphics_view)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()  # Layout to arrange buttons horizontally

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

    
    def request_stop(self):
        self.stop_requested = True
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

            elif (global_saved_parameters['type_tool']) == "plazma":
                # tutaj generowanie G-codu dla plazmy

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





                # Ustaw wygenerowany G-kod w oknie dialogowym
                custom_dialog.set_generated_gcode(generated_gcode)

                custom_dialog.exec_()

                print("Canceled generating G-code")


            elif (global_saved_parameters['type_tool']) == "stożek":
                
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
        print(f"Wygenerowane obroty: [{rotations_text}] rad")
        return rotations
    def apply_trans_and_rot(self, points, trans_x, trans_y, rotation):
        transformed_points = []
        cos_rot = np.cos(rotation)
        sin_rot = np.sin(rotation)
        for point in points:
            rotated_x = point[0] * cos_rot - point[1] * sin_rot
            rotated_y = point[0] * sin_rot + point[1] * cos_rot
            transformed_points.append((rotated_x + trans_x, rotated_y + trans_y))
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
    
    
    def display_file(self, file_paths, width, height, checked_paths):
        if any(var is None for var in [global_space_between_objects, global_optimization, global_accuracy, global_rotations, global_starting_point]):
            QMessageBox.critical(None, "Error", "Not all nesting parameters are configured.\nPlease configure all nesting parameters before calling the nesting function.")
            return

        self.progress_bar.setMaximum(global_rotations - 1)
        self.inputPoints = []
        file_to_parse = Parser(checked_paths)
        returned_values = file_to_parse.parse_svg()
        returned_input_points, returned_svg_points = returned_values
        self.inputPoints += returned_input_points
        self.volume = Box(width, height)

        if not self.check_fit_in_volume(self.inputPoints, width, height):
            return

        spacing = int(global_space_between_objects)
        rotations = self.generate_rotations(global_rotations) if global_rotations > 0 else []

        nfp_config = self.configure_nesting_parameters(rotations)

        min_area = float('inf')
        min_area_rotation = 0
        min_area_index = -1
        
        for index, rotation in enumerate(rotations):
            if self.stop_requested:
                print("Nesting process stopped.")
                self.stop_requested = False
                break
           
            nfp_config.rotations = [rotation]
            num_bins = nest(self.inputPoints, self.volume, spacing, nfp_config)
            self.progress_bar.setValue(index)
            fig = Figure(figsize=(8, 8), tight_layout={'pad': 0})
            ax = fig.add_subplot(111)
            ax.set_aspect('equal')
            ax.set_xlim([-self.volume.width() / 2, self.volume.width() / 2])
            ax.set_ylim([-self.volume.height() / 2, self.volume.height() / 2])
            ax.set_xticks([])
            ax.set_yticks([])

            min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')

            for i, item in enumerate(self.inputPoints):
                parsed_path = parse_path(returned_svg_points[i])
                item.resetTransformation()

                x_points, y_points = [], []
                for segment in parsed_path:
                    for t in np.linspace(0, 1, num=80):
                        point = segment.point(t)
                        transformed_point = self.apply_trans_and_rot([(point.real * 100 * self.svg_to_mm, point.imag * 100 * self.svg_to_mm)], item.translation().x(), item.translation().y(), item.rotation())[0]
                        x_points.append(transformed_point[0])
                        y_points.append(transformed_point[1])

                ax.plot(x_points, y_points, color='black', linewidth=1)
                min_x, max_x = min(min_x, *x_points), max(max_x, *x_points)
                min_y, max_y = min(min_y, *y_points), max(max_y, *y_points)

            # Calculate the area of the bounding box
            bounding_box_width = max_x - min_x
            bounding_box_height = max_y - min_y
            bounding_box_area = bounding_box_width * bounding_box_height
            
            if bounding_box_area < min_area:
                min_area = bounding_box_area
                min_area_rotation = rotation
                min_area_index = index

                # Draw the bounding box
                ax.add_patch(Rectangle((min_x, min_y), bounding_box_width, bounding_box_height, linewidth=1, edgecolor='r', facecolor='none'))

                # Display the canvas only if it's the smallest bounding box found so far
                canvas = FigureCanvas(fig)
                self.scene.addWidget(canvas)
                canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                canvas.updateGeometry()
                
                self.rotation_displayed.emit(rotation)
                print(f"Displaying rotation: {rotation:.2f} radians - New minimum area: {min_area:.2f} at Index {min_area_index}")
                self.scene.update()
                QApplication.processEvents()
                svg_filename = "output.svg"
                fig.savefig(svg_filename, format='svg', bbox_inches='tight', pad_inches=0)
                

        if min_area_index != -1:  # Ensure there was at least one update
            print(f"Minimum Bounding Box Area: {min_area:.2f} at Rotation {min_area_rotation:.2f} radians, Index {min_area_index}")

    def check_fit_in_volume(self, parsed_objects, width, height):
        total_area = sum(obj.area() for obj in parsed_objects)
        print("Suma powierzchni obiektów:", -total_area) 
        volume_area = width * height
        if -total_area > volume_area:
            min_area = -total_area - volume_area
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("<font size='+2' color='red'>Błąd: Brak wystarczającej przestrzeni dla wszystkich obiektów.</font>")
            msg.setInformativeText(f"Minimalna wymagana powierzchnia: {min_area} jednostek kwadratowych.\n\n"
                                    "Suma powierzchni obiektów przekracza dostępną objętość. Proszę dostosować wymiary lub zmniejszyć liczbę obiektów.")
            msg.setWindowTitle("Błąd")
            msg.setStyleSheet("QMessageBox { background-color: white; }")
            msg.exec_()
            return False
        else:
            print("Powierzchnie poszczególnych obiektów:")
            for i, obj in enumerate(parsed_objects):
                print(f"Obiekt {i + 1}: {obj.area()}")
        return True
    
    def generate_gcode(self):
        # Open the tool parameters dialog
        self.open_tool_parameters_dialog_right()