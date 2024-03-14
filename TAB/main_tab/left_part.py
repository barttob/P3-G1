import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ezdxf import readfile
import xml.etree.ElementTree as ET
import svg.path
import numpy as np
from svg.path import parse_path


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
        file_paths, _ = QFileDialog.getOpenFileNames(self, 'Wybierz pliki', '.', 'DXF Files (*.dxf);;SVG Files (*.svg)')
        for file_path in file_paths:
            self.file_path_send += file_paths
            if file_path.lower().endswith('.dxf'):
                self.read_and_display_dxf(file_path)
            elif file_path.lower().endswith('.svg'):
                self.read_and_display_svg(file_path)

    def read_and_display_dxf(self, file_path):
        try:
            # Otwarcie pliku DXF
            doc = readfile(file_path)

            

            # Iteracja przez obiekty w przestrzeni modelu
            for entity in doc.modelspace():
                # Tworzenie miniatury figury
                figure_canvas = self.create_figure(entity)

                # Pobranie danych o figury
                entity_type = entity.dxftype()
                entity_data = self.get_entity_data(entity)

                # Dodanie wiersza do tabeli
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)

                # Wstawienie miniatury figury do pierwszej kolumny
                self.table.setCellWidget(row_position, 0, figure_canvas)

                # Wstawienie danych o figury do pozostałych kolumn
                self.table.setItem(row_position, 1, QTableWidgetItem(entity_type))
                self.table.setItem(row_position, 2, QTableWidgetItem(str(entity_data)))

                # Dodanie checkboxa do zaznaczania wiersza
                checkbox_item = QCheckBox()
                self.table.setCellWidget(row_position, 3, checkbox_item)

                # Ustawienie stałego rozmiaru dla komórki z miniaturą
                self.table.verticalHeader().setDefaultSectionSize(100)

        except Exception as e:
            print("Błąd odczytu pliku DXF:", e)

    def read_and_display_svg(self, file_path):
        try:
            # Otwarcie pliku SVG
            tree = ET.parse(file_path)
            root = tree.getroot()

            

            # Iteracja przez elementy w pliku SVG
            for element in root.iter():
                # Sprawdzenie czy element jest rysunkiem (path)
                if element.tag.endswith('path'):
                    # Tworzenie miniatury figury
                    figure_canvas = self.create_svg_figure(element)

                    # Dodanie wiersza do tabeli
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)

                    # Wstawienie miniatury figury do pierwszej kolumny
                    self.table.setCellWidget(row_position, 0, figure_canvas)

                    # Wstawienie typu elementu do drugiej kolumny
                    self.table.setItem(row_position, 1, QTableWidgetItem('SVG Path'))

                    # Wstawienie danych (ścieżki) do trzeciej kolumny
                    self.table.setItem(row_position, 2, QTableWidgetItem(element.attrib['d']))

                    # Dodanie checkboxa do zaznaczania wiersza
                    checkbox_item = QCheckBox()
                    self.table.setCellWidget(row_position, 3, checkbox_item)

                    # Ustawienie stałego rozmiaru dla komórki z miniaturą
                    self.table.verticalHeader().setDefaultSectionSize(100)

        except Exception as e:
            print("Błąd odczytu pliku SVG:", e)

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
        # Pobranie danych o ścieżce z elementu SVG i narysowanie jej na wykresie
        path_data = element.attrib['d']
        path = parse_path(path_data)

        # Inicjalizacja list do przechowywania punktów ścieżki
        x_points = []
        y_points = []

        for segment in path:
            # Iteracja przez segmenty ścieżki
            for t in np.linspace(0, 1, num=100):
                # Pobranie współrzędnych punktu na ścieżce dla danego parametru t
                point = segment.point(t)
                x_points.append(point.real)
                y_points.append(point.imag)

        ax.plot(x_points, y_points, color='black')

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
    
    def draw_entity(self, ax, entity):
        if entity.dxftype() == 'SPLINE':
            # Przetwarzanie krzywej składanej (spline)
            control_points = list(entity.control_points)
            x = [p[0] for p in control_points]
            y = [p[1] for p in control_points]
            ax.plot(x, y, color='black')
        elif entity.dxftype() == 'LINE':
            # Przetwarzanie linii
            start_point = entity.dxf.start
            end_point = entity.dxf.end
            ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='black')
        elif entity.dxftype() == 'LWPOLYLINE':
            # Przetwarzanie polilinii
            points = list(entity.points())
            x = [p[0] for p in points]
            y = [p[1] for p in points]
            ax.plot(x, y, color='black')
        elif entity.dxftype() == 'CIRCLE':
            # Przetwarzanie okręgów
            center = entity.dxf.center
            radius = entity.dxftype().radius
            circle = plt.Circle((center[0], center[1]), radius, fill=False, color='black')
            ax.add_artist(circle)
        elif entity.dxftype() == 'TEXT':
            # Przetwarzanie tekstu
            text = entity.dxf.text
            insertion_point = entity.dxf.insert
            ax.text(insertion_point[0], insertion_point[1], text, color='black')
        # Dodaj obsługę innych typów obiektów tutaj...

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
        self.right_part.display_file(self.file_path_send)

