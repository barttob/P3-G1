import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QHBoxLayout, QCheckBox, QLabel, QLineEdit, QMessageBox, QGroupBox, QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtXml import QDomDocument
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
from TAB.config_tab import ConfigTab
from TAB.main_tab.right_part import RightPart
from ezdxf.addons import odafc
import shutil
import random
import string
from utils.parser import Parser
from shapely.geometry import Point, Polygon, LineString


class LeftPart(QWidget):
    def __init__(self):
        super().__init__()

        # Inicjalizacja interfejsu użytkownika
        self.initUI()
        self.file_path_send = []
        self.right_part = RightPart()

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
        file_paths, _ = QFileDialog.getOpenFileNames(self, 'Wybierz pliki', '.', ' (*.dxf *.dwg *.svg);;DXF Files (*.dxf);;DWG Files (*.dwg);;SVG Files (*.svg)')
        for file_path in file_paths:
            self.file_path_send += file_paths
            if file_path.lower().endswith('.dxf'):
                self.read_and_display_dxf(file_path)
            elif file_path.lower().endswith('.svg'):
                self.analize_svg(file_path)
            elif file_path.lower().endswith('.dwg'):
                self.convert_and_display_dwg(file_path)

    def analize_svg(self, file_path_or_root):
            try:
                if isinstance(file_path_or_root, str):
                    tree = ET.parse(file_path_or_root)
                    root = tree.getroot()
                else:
                    root = file_path_or_root

                # Sprawdzenie obecności grup w pliku SVG
                has_groups = any(element.tag == '{http://www.w3.org/2000/svg}g' for element in root.iter())

                if has_groups:
                    print("Są grupy")
                    for group in root.findall('.//{http://www.w3.org/2000/svg}g'):
                        self.process_group_dialog(group)
                else:
                    self.read_and_display_svg(root)

            except Exception as e:
                print("Błąd odczytu pliku SVG:", e)
   
   
    def process_group_dialog(self, group):
       
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText("Czy narysować grupę w całości?")
        msg_box.setWindowTitle("Process Group")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        response = msg_box.exec_()

        if response == QMessageBox.Yes:
            self.process_group(group)
        else:
            root = ET.Element("root")  
            root.extend(list(group))  

            self.analize_svg(root)

    def process_group(self, group):
        try:
            # Pobranie wszystkich elementów ścieżki w grupie
            paths = [element for element in group.iter() if element.tag.endswith('path')]

            # Tworzenie miniatury figury dla wszystkich ścieżek w grupie
            figure_canvas = self.create_svg_figure(paths)

            # Dodanie wiersza do tabeli
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            # Wstawienie miniatury figury do pierwszej kolumny
            self.table.setCellWidget(row_position, 0, figure_canvas)

            # Wstawienie typu elementu do drugiej kolumny
            self.table.setItem(row_position, 1, QTableWidgetItem('SVG Group'))

            # Wstawienie danych (ścieżki) do trzeciej kolumny - pusty string, bo to cała grupa
            self.table.setItem(row_position, 2, QTableWidgetItem(''))

            # Dodanie checkboxa do zaznaczania wiersza
            checkbox_item = QCheckBox()
            self.table.setCellWidget(row_position, 3, checkbox_item)

            # Ustawienie stałego rozmiaru dla komórki z miniaturą
            self.table.verticalHeader().setDefaultSectionSize(145)

        except Exception as e:
            print("Błąd przetwarzania grupy SVG:", e)




    def read_and_display_svg(self, root):
            try:
                
                # Pobranie wszystkich elementów ścieżki i linii
                paths_and_lines = [element for element in root.iter() if element.tag.endswith('path') or element.tag.endswith('line')]

                # Grupowanie elementów ścieżki i linii wg. ich współrzędnych początkowych i końcowych
                path_line_groups = {}
                for element in paths_and_lines:
                    if element.tag.endswith('line'):
                        # Pominięcie pojedynczych linii, zostaną one połączone z innymi liniami mającymi wspólne punkty końcowe
                        continue
                    start_point, end_point = self.get_start_and_end_points(element)
                    if (start_point, end_point) in path_line_groups:
                        path_line_groups[(start_point, end_point)].append(element)
                    else:
                        path_line_groups[(start_point, end_point)] = [element]

                # Łączenie pojedynczych linii z innymi liniami mającymi wspólne punkty końcowe
                lines_to_merge = []
                for element in paths_and_lines:
                    if element.tag.endswith('line'):
                        start_point = self.get_start_point(element)
                        end_point = self.get_end_point(element)
                        for group_key, group_elements in path_line_groups.items():
                            if start_point == group_key[1]:
                                lines_to_merge.append((element, group_elements))
                            elif end_point == group_key[0]:
                                lines_to_merge.append((group_elements, element))

                for line1, line2 in lines_to_merge:
                    path_line_groups.pop((self.get_start_point(line1), self.get_end_point(line1)), None)
                    path_line_groups.pop((self.get_start_point(line2), self.get_end_point(line2)), None)
                    merged_line = line1 + line2
                    start_point = self.get_start_point(line1)
                    end_point = self.get_end_point(line2)
                    path_line_groups[(start_point, end_point)] = merged_line

                # Iteracja przez grupy elementów ścieżki i łączone linie
                for group in path_line_groups.values():
                    # Pominięcie grupy, jeśli zawiera tylko linie
                    if all(element.tag.endswith('line') for element in group):
                        continue

                    # Tworzenie miniatury figury
                    figure_canvas = self.create_svg_figure(group)

                    # Dodanie wiersza do tabeli
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)

                    # Wstawienie miniatury figury do pierwszej kolumny
                    self.table.setCellWidget(row_position, 0, figure_canvas)

                    # Wstawienie typu elementu do drugiej kolumny
                    self.table.setItem(row_position, 1, QTableWidgetItem('SVG Path'))

                    # Wstawienie danych (ścieżki) do trzeciej kolumny
                    path_data = ' '.join(path.attrib['d'] for path in group)
                    self.table.setItem(row_position, 2, QTableWidgetItem(path_data))

                    # Dodanie checkboxa do zaznaczania wiersza
                    checkbox_item = QCheckBox()
                    self.table.setCellWidget(row_position, 3, checkbox_item)

                    # Ustawienie stałego rozmiaru dla komórki z miniaturą
                    self.table.verticalHeader().setDefaultSectionSize(145)

            except Exception as e:
                print("Błąd odczytu pliku SVG:", e)


    def create_svg_figure(self, paths):
        # Tworzenie nowej figury Matplotlib
        fig = Figure(figsize=(2, 2))
        ax = fig.add_subplot(111)

        # Rysowanie ścieżek
        for path in paths:
            self.draw_svg_element(ax, path)

        # Konwersja figury do formatu odpowiedniego dla wyświetlenia w tabeli
        canvas = FigureCanvas(fig)
        canvas.draw()

        return canvas


    def draw_svg_element(self, ax, path):
        # Pobranie danych o ścieżce z elementu SVG i narysowanie jej na wykresie
        path_data = path.attrib['d']
        path = parse_path(path_data)

        # Rysowanie ścieżki
        for segment in path:
            x_points = []
            y_points = []

            # Iteracja przez punkty segmentu
            for t in np.linspace(0, 1, num=100):
                # Pobranie współrzędnych punktu na ścieżce dla danego parametru t
                point = segment.point(t)
                x_points.append(point.real)
                y_points.append(point.imag)

            # Narysowanie linii dla tego segmentu
            ax.plot(x_points, y_points, color='black')

        ax.set_xticks([])
        ax.set_yticks([])


    def get_start_and_end_points(self, path):
        # Pobranie danych o ścieżce z elementu SVG
        path_data = path.attrib['d']
        path = parse_path(path_data)

        # Pobranie współrzędnych punktu początkowego i końcowego ścieżki
        start_point = path.point(0)
        end_point = path.point(1)
        return start_point, end_point
   
    def get_end_point(self, path):
        # Pobranie danych o ścieżce z elementu SVG
        path_data = path.attrib['d']
        path = parse_path(path_data)

        # Pobranie współrzędnych punktu końcowego ścieżki
        end_point = path.point(1)
        return end_point

    def get_start_point(self, path):
        # Pobranie danych o ścieżce z elementu SVG
        path_data = path.attrib['d']
        path = parse_path(path_data)

        # Pobranie współrzędnych punktu początkowego ścieżki
        start_point = path.point(0)
        return start_point

    def is_polygon(self, element):
        return element.tag.endswith('polygon') or (element.tag.endswith('path') and 'd' in element.attrib)

    def is_line(self, element):
        return element.tag.endswith('line') or element.tag.endswith('polyline')

    def is_image(self, element):
        return element.tag.endswith('image')

    def check_spatial_relationships(self, elements):
        polygons = []
        lines = []
        images = []
        other_elements = []
        # Podział elementów na różne typy
        for element in elements:
            if self.is_polygon(element):
                polygons.append(element)
            elif self.is_line(element):
                lines.append(element)
            elif self.is_image(element):
                images.append(element)
            else:
                other_elements.append(element)

        # Sprawdzenie relacji przestrzennych między różnymi typami elementów
        self.check_polygon_relations(polygons, lines)
        self.check_polygon_relations(polygons, images)
        self.check_line_relations(lines, images)
        self.check_other_relations(other_elements)

    def check_other_relations(self, other_elements):
        # Sprawdzenie relacji przestrzennych między innymi typami elementów
        for element1 in other_elements:
            for element2 in other_elements:
                if element1 != element2:
                    if self.intersects(element1, element2):
                        print(f"Relacja przestrzenna między {element1.tag} a {element2.tag}: Przecinają się.")
                    else:
                        print(f"Relacja przestrzenna między {element1.tag} a {element2.tag}: Brak przecięcia.")

    def check_polygon_relations(self, polygons, other_elements):
        for polygon in polygons:
            for other_element in other_elements:
                if self.is_polygon(other_element):
                    if self.inside(polygon, other_element):
                        print(f"{other_element.tag} znajduje się wewnątrz wielokąta {polygon.tag}.")
                    elif self.intersects(polygon, other_element):
                        print(f"{other_element.tag} przecina się z wielokątem {polygon.tag}.")
                    else:
                        print(f"Brak relacji przestrzennej między {other_element.tag} a wielokątem {polygon.tag}.")
                elif self.is_line(other_element):
                    if self.line_inside_polygon(polygon, other_element):
                        print(f"Linia znajduje się wewnątrz wielokąta {polygon.tag}.")
                    elif self.line_intersects_polygon(polygon, other_element):
                        print(f"Linia przecina się z wielokątem {polygon.tag}.")
                    else:
                        print(f"Brak relacji przestrzennej między linią a wielokątem {polygon.tag}.")
                elif self.is_image(other_element):
                    if self.image_inside_polygon(polygon, other_element):
                        print(f"Obraz znajduje się wewnątrz wielokąta {polygon.tag}.")
                    else:
                        print(f"Brak relacji przestrzennej między obrazem a wielokątem {polygon.tag}.")

    def line_inside_polygon(self, polygon, line):
        # Sprawdzenie czy wszystkie punkty linii znajdują się wewnątrz wielokąta
        line_points = self.get_points(line)
        polygon_points = self.get_points(polygon)
        for point in line_points:
            if not Point(point).within(Polygon(polygon_points)):
                return False
        return True

    def line_intersects_polygon(self, polygon, line):
        # Sprawdzenie czy linia przecina się z którymkolwiek bokiem wielokąta
        line_points = self.get_points(line)
        polygon_points = self.get_points(polygon)
        for i in range(len(polygon_points)):
            p1 = polygon_points[i]
            p2 = polygon_points[(i + 1) % len(polygon_points)]
            segment = LineString([p1, p2])
            line_segment = LineString(line_points)
            if segment.intersects(line_segment):
                return True
        return False

    def image_inside_polygon(self, polygon, image):
        # Sprawdzenie czy lewy górny róg obrazu znajduje się wewnątrz wielokąta
        image_point = self.get_point(image)
        polygon_points = self.get_points(polygon)
        return Point(image_point).within(Polygon(polygon_points))


    def check_line_relations(self, lines, other_elements):
        for line in lines:
            for other_element in other_elements:
                if self.intersects(line, other_element):
                    print(f"{other_element.tag} przecina się z linią.")
                else:
                    print("Brak relacji przestrzennej między elementami.")

    def intersects(self, element1, element2):
        # Wczytanie współrzędnych punktów
        points1 = self.get_points(element1)
        points2 = self.get_points(element2)

        # Sprawdzenie czy punkty końcowe jednej linii są takie same jak punkty początkowe innej linii
        if points1[-1] == points2[0]:
            return True

        # Sprawdzenie czy linie się przecinają
        line1 = LineString(points1)
        line2 = LineString(points2)
        return line1.intersects(line2)

    def inside(self, polygon, element):
        # Wczytanie współrzędnych punktów wielokąta
        polygon_points = self.get_points(polygon)
        polygon_shape = Polygon(polygon_points)

        # Wczytanie współrzędnych punktu elementu
        element_point = self.get_point(element)

        return polygon_shape.contains(element_point)

    def get_points(self, element):
        if self.is_polygon(element) or self.is_line(element):
            # W przypadku wielokąta lub linii pobieramy współrzędne punktów z atrybutu 'points'
            points_str = element.attrib['points']
            points = [tuple(map(float, point.split(','))) for point in points_str.split()]
        elif self.is_image(element):
            # W przypadku obrazu pobieramy współrzędne jego lewego górnego rogu
            x = float(element.attrib['x'])
            y = float(element.attrib['y'])
            points = [(x, y)]
        else:
            # Dla innych typów elementów zwracamy pusty zbiór punktów
            points = []
        return points

    def get_point(self, element):
        if self.is_image(element):
            # W przypadku obrazu pobieramy współrzędne jego lewego górnego rogu
            x = float(element.attrib['x'])
            y = float(element.attrib['y'])
            point = Point(x, y)
        else:
            # Dla innych typów elementów zwracamy pusty punkt
            point = Point(0, 0)
        return point

    
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
                print("Brak skonwertowanego pliku DXF.")

        except Exception as e:
            print("Błąd konwersji pliku DWG:", e)