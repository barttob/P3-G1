import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QHBoxLayout, QCheckBox, QLabel, QLineEdit, QMessageBox, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Polygon
from ezdxf import readfile
import xml.etree.ElementTree as ET
import svg.path
import numpy as np
from svg.path import parse_path
from ezdxf.addons import odafc
import shutil
import random
import string
from utils.parser import Parser


class LeftPart(QWidget):
    def __init__(self):
        super().__init__()

        # Inicjalizacja interfejsu użytkownika
        self.initUI()
        self.file_path_send = []

    def initUI(self):
        # Ustawienie layoutu pionowego
        layout = QVBoxLayout()

        # Przycisk do importowania plików DXF i SVG
        self.import_button = QPushButton('Importuj pliki')
        self.import_button.clicked.connect(self.import_files)
        layout.addWidget(self.import_button)

        # Utworzenie ramki dla wymiarów płaszczyzny roboczej
        dimension_frame = QGroupBox()
        dimension_layout = QVBoxLayout()

        # Ustawienie tytułu ramki z pogrubieniem za pomocą HTML
        dimension_frame.setTitle('Wymiary płaszczyzny roboczej')

        # Pole tekstowe dla szerokości
        self.width_label = QLabel('Szerokość (mm):')
        self.width_input = QLineEdit()
        self.width_input.setText("100")
        width_validator = QDoubleValidator()
        self.width_input.setValidator(width_validator)
        dimension_layout.addWidget(self.width_label)
        dimension_layout.addWidget(self.width_input)

        # Pole tekstowe dla wysokości
        self.height_label = QLabel('Wysokość (mm):')
        self.height_input = QLineEdit()
        self.height_input.setText("100")
        height_validator = QDoubleValidator()
        self.height_input.setValidator(height_validator)
        dimension_layout.addWidget(self.height_label)
        dimension_layout.addWidget(self.height_input)

        # Ustawienie układu dla ramki
        dimension_frame.setLayout(dimension_layout)

        # Dodanie ramki do głównego układu
        layout.addWidget(dimension_frame)

        # Utworzenie tabeli do wyświetlania danych
        self.table = QTableWidget()
        layout.addWidget(self.table)



        # Ustawienie nagłówków tabeli
        headers = ['Wizualizacja', 'Typ', 'Dane', 'Zaznacz', 'Opcje']
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Ustawienie dopasowania tabeli do maksymalnej dostępnej szerokości
        self.table.horizontalHeader().setStretchLastSection(True)

        # Przyciski 'Zaznacz wszystko' i 'Odznacz wszystko'
        btn_layout = QHBoxLayout()
        self.select_all_button = QPushButton('Zaznacz wszystko')
        self.select_all_button.clicked.connect(self.select_all_rows)
        self.deselect_all_button = QPushButton('Odznacz wszystko')
        self.deselect_all_button.clicked.connect(self.deselect_all_rows)
        self.clear_table_button = QPushButton('Wyczyść tabelę')  # Nowy przycisk
        self.clear_table_button.clicked.connect(self.clear_table)  # Nowa metoda
        self.display_file_button = QPushButton('Nesting')  # New button
        self.display_file_button.clicked.connect(self.display_selected_file)  # Connect button to method
        btn_layout.addWidget(self.select_all_button)
        btn_layout.addWidget(self.deselect_all_button)
        btn_layout.addWidget(self.clear_table_button)  # Dodanie przycisku do układu
        btn_layout.addWidget(self.display_file_button)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def clear_table(self):
        self.table.clearContents()  
        self.table.setRowCount(0)
        self.file_path_send = []  

    def import_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, 'Wybierz pliki', '.', 'DXF Files (*.dxf);;DWG Files (*.dwg);;SVG Files (*.svg)')
        for file_path in file_paths:
            self.file_path_send += file_paths
            if file_path.lower().endswith('.dxf'):
                self.read_and_display_dxf(file_path)
            elif file_path.lower().endswith('.svg'):
                self.read_and_display_svg(file_path)
            elif file_path.lower().endswith('.dwg'):
                self.convert_and_display_dwg(file_path)

    def read_and_display_dxf(self, file_path):
        try:
            file_to_convert = Parser(file_path)
            self.file_path_send.pop()
            converted_file_path = file_to_convert.dxf_to_svg()
            self.read_and_display_svg(converted_file_path)
            self.file_path_send.append(converted_file_path)
            # # Otwarcie pliku DXF
            # doc = readfile(file_path)

            

            # # Iteracja przez obiekty w przestrzeni modelu
            # for entity in doc.modelspace():
            #     # Tworzenie miniatury figury
            #     figure_canvas = self.create_figure(entity)

            #     # Pobranie danych o figury
            #     entity_type = entity.dxftype()
            #     entity_data = self.get_entity_data(entity)

            #     # Dodanie wiersza do tabeli
            #     row_position = self.table.rowCount()
            #     self.table.insertRow(row_position)

            #     # Wstawienie miniatury figury do pierwszej kolumny
            #     self.table.setCellWidget(row_position, 0, figure_canvas)

            #     # Wstawienie danych o figury do pozostałych kolumn
            #     self.table.setItem(row_position, 1, QTableWidgetItem(entity_type))
            #     self.table.setItem(row_position, 2, QTableWidgetItem(str(entity_data)))

            #     # Dodanie checkboxa do zaznaczania wiersza
            #     checkbox_item = QCheckBox()
            #     self.table.setCellWidget(row_position, 3, checkbox_item)

            #     # Ustawienie stałego rozmiaru dla komórki z miniaturą
            #     self.table.verticalHeader().setDefaultSectionSize(100)

        except Exception as e:
            print("Błąd odczytu pliku DXF:", e)

    def read_and_display_svg(self, file_path):
        try:
            # Open the SVG file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Iterate through elements in the SVG file
            for element in root.iter():
                # Check if the element is a path, rectangle, or polygon
                if element.tag.endswith('path') or element.tag.endswith('rect') or element.tag.endswith('polygon'):
                    # Create a thumbnail of the figure
                    figure_canvas = self.create_svg_figure(element)

                    # Add a row to the table
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)

                    # Insert the thumbnail into the first column
                    self.table.setCellWidget(row_position, 0, figure_canvas)

                    # Insert the type of element into the second column
                    if element.tag.endswith('path'):
                        element_type = 'SVG Path'
                    elif element.tag.endswith('rect'):
                        element_type = 'SVG Rectangle'
                    elif element.tag.endswith('polygon'):
                        element_type = 'SVG Polygon'
                    self.table.setItem(row_position, 1, QTableWidgetItem(element_type))

                    # Insert data (path, rectangle properties, or polygon points) into the third column
                    if element.tag.endswith('path'):
                        self.table.setItem(row_position, 2, QTableWidgetItem(element.attrib['d']))
                    elif element.tag.endswith('rect'):
                        rect_data = f"x: {element.attrib['x']}, y: {element.attrib['y']}, width: {element.attrib['width']}, height: {element.attrib['height']}"
                        self.table.setItem(row_position, 2, QTableWidgetItem(rect_data))
                    elif element.tag.endswith('polygon'):
                        self.table.setItem(row_position, 2, QTableWidgetItem(element.attrib['points']))

                    # Add a checkbox to select the row
                    checkbox_item = QCheckBox()
                    self.table.setCellWidget(row_position, 3, checkbox_item)

                    # Set a fixed size for the thumbnail cell
                    self.table.verticalHeader().setDefaultSectionSize(100)

        except Exception as e:
            print("Error reading SVG file:", e)


    def create_svg_figure(self, element):
        # Tworzenie nowej figury Matplotlib
        fig = Figure(figsize=(2, 2))
        ax = fig.add_subplot(111)

        # Rysowanie figury
        self.draw_svg_element(ax, element)

        # Konwersja figury do formatu odpowiedniego dla wyświetlenia w tabeli
        canvas = FigureCanvas(fig)
        canvas.draw()

        return canvas
    
    def draw_svg_element(self, ax, element):
        if element.tag.endswith('path'):
            # Drawing paths
            path_data = element.attrib['d']
            path = parse_path(path_data)

            # Initialize lists to store path points
            x_points = []
            y_points = []

            for segment in path:
                for t in np.linspace(0, 1, num=100):
                    point = segment.point(t)
                    x_points.append(point.real)
                    y_points.append(point.imag)

            ax.plot(x_points, y_points, color='black')
        elif element.tag.endswith('rect'):
            # Drawing rectangles
            x = float(element.attrib['x'])
            y = float(element.attrib['y'])
            width = float(element.attrib['width'])
            height = float(element.attrib['height'])
            rect = Rectangle((x, y), width, height, edgecolor='black', facecolor='none')
            ax.add_patch(rect)
        elif element.tag.endswith('polygon'):
            # Drawing polygons
            points_str = element.attrib['points']
            points = [tuple(map(float, points_str.split()[i:i+2])) for i in range(0, len(points_str.split()), 2)]
            polygon = Polygon(points, closed=True, edgecolor='black', facecolor='none')
            ax.add_patch(polygon)

        ax.set_xticks([])
        ax.set_yticks([])

    def create_figure(self, entity):
        # Tworzenie nowej figury Matplotlib
        fig = Figure(figsize=(2, 2))
        ax = fig.add_subplot(111)

        # Rysowanie figury
        self.draw_entity(ax, entity)

        # Konwersja figury do formatu odpowiedniego dla wyświetlenia w tabeli
        canvas = FigureCanvas(fig)
        canvas.draw()

        return canvas
    
    # def draw_entity(self, ax, entity):
    #     if entity.dxftype() == 'SPLINE':
    #         # Przetwarzanie krzywej składanej (spline)
    #         control_points = list(entity.control_points)
    #         x = [p[0] for p in control_points]
    #         y = [p[1] for p in control_points]
    #         ax.plot(x, y, color='black')
    #     elif entity.dxftype() == 'LINE':
    #         # Przetwarzanie linii
    #         start_point = entity.dxf.start
    #         end_point = entity.dxf.end
    #         ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='black')
    #     elif entity.dxftype() == 'LWPOLYLINE':
    #         # Przetwarzanie polilinii
    #         points = list(entity.points())
    #         x = [p[0] for p in points]
    #         y = [p[1] for p in points]
    #         ax.plot(x, y, color='black')
    #     elif entity.dxftype() == 'CIRCLE':
    #         # Przetwarzanie okręgów
    #         center = entity.dxf.center
    #         radius = entity.dxftype().radius
    #         circle = plt.Circle((center[0], center[1]), radius, fill=False, color='black')
    #         ax.add_artist(circle)
    #     elif entity.dxftype() == 'TEXT':
    #         # Przetwarzanie tekstu
    #         text = entity.dxf.text
    #         insertion_point = entity.dxf.insert
    #         ax.text(insertion_point[0], insertion_point[1], text, color='black')
    #     # Dodaj obsługę innych typów obiektów tutaj...

    def get_entity_data(self, entity):
        # Funkcja do pobrania danych o figury z pliku DXF
        # Tutaj można dodać dodatkowe dane o figury
        return 'Dodatkowe dane o figury'

    def select_all_rows(self):
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.cellWidget(row, 3)
            checkbox_item.setChecked(True)

    def deselect_all_rows(self):
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.cellWidget(row, 3)
            checkbox_item.setChecked(False)

    def display_selected_file(self):
        width_text = self.width_input.text()
        height_text = self.height_input.text()

        # Sprawdzenie, czy pola szerokości i wysokości są puste
        if not width_text.strip() and not height_text.strip():
            # Jeśli pola są puste, wyświetlamy okno dialogowe z komunikatem
            QMessageBox.warning(self, "Błąd", "Pola szerokości i wysokości nie mogą być puste.")
        else:
            # Jeśli pola nie są puste, sprawdzamy, czy zawierają jedynie cyfry lub wartości ujemne
            if width_text.replace('mm', '').isnumeric() and height_text.replace('mm', '').isnumeric():
                width = int(float(width_text) * 100)
                height = int(float(height_text) * 100)
                # Dodatkowa walidacja: Sprawdzamy, czy szerokość i wysokość są większe niż zero
                if width > 0 and height > 0:
                    # Wywołanie metody wyświetlającej pliki, ponieważ pola są poprawnie uzupełnione
                    self.right_part.display_file(self.file_path_send, width, height)
                else:
                    QMessageBox.warning(self, "Błąd", "Szerokość i wysokość muszą być większe od zera.")
            else:
                # Jeśli pola zawierają niedozwolone znaki, wyświetlamy okno dialogowe z odpowiednim komunikatem
                QMessageBox.warning(self, "Błąd", "Podane wartości szerokości i wysokości muszą być liczbami.")

    def convert_and_display_dwg(self, file_path):
        try:
            # Pobierz ścieżkę do katalogu projektu
            project_dir = os.getcwd()
            print(project_dir)

            # Utwórz ścieżkę do folderu tymczasowego
            temp_folder = os.path.join(project_dir, 'temp')

            # Sprawdź czy folder już istnieje, jeśli nie - utwórz go
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)
                print(f"Utworzono folder tymczasowy: {temp_folder}")
            else:
                print(f"Folder tymczasowy już istnieje: {temp_folder}")     

            os.environ['XDG_RUNTIME_DIR'] = '/tmp/runtime-root'

            file_name = os.path.basename(file_path)

            # Utwórz losową nazwę dla pliku tymczasowego
            random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            temp_file_name, temp_file_ext = os.path.splitext(file_name)
            temp_file_path = os.path.join(temp_folder, f"{temp_file_name}_{random_suffix}{temp_file_ext}")

            shutil.copy2(file_path, temp_file_path)

            # Konwersja pliku DWG do DXF przy użyciu ODA File Converter
            odafc.convert(temp_file_path, version='ACAD2018', audit=True)

            # Odnajdywanie skonwertowanego pliku DXF
            dxf_files = [f for f in os.listdir(temp_folder) if f.endswith('.dxf')]
            if len(dxf_files) > 0:
                dxf_file_path = os.path.join(temp_folder, dxf_files[0])
                self.file_path_send.pop()
                self.file_path_send.append(dxf_file_path)
                self.read_and_display_dxf(dxf_file_path)
            else:
                print("Brak pliku DXF po konwersji.")

        except Exception as e:
            print("Błąd konwersji pliku DWG:", e)
