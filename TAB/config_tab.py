from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QComboBox, QSpinBox, QSizePolicy, QFormLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from TAB.main_tab.right_part import RightPart  # Import klasy RightPart

class ConfigTab(QWidget):

    def __init__(self, right_part):
        super().__init__()
        self.right_part = right_part
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)        

        # Lewa połowa 
        left_half = QWidget(self)
        left_half.setStyleSheet("background-color: rgb(142, 191, 250);")
        left_layout = QVBoxLayout(left_half)
        main_layout.addWidget(left_half, stretch=20)

        # QFormLayout dla równego ułożenia pól
        form_layout = QFormLayout()
        left_layout.addLayout(form_layout)

        form_layout.addRow(QLabel(""))
        form_layout.addRow(QLabel(""))

        # Konfiguracja nestingu
        label_nestConfiguration = QLabel("<b>Konfiguracja nestigu:<b>")
        label_nestConfiguration.setStyleSheet("font-size: 16px;")

        # Poziomy układ dla etykiety i przycisku
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(label_nestConfiguration)
        default_button = QPushButton("Ustaw domyślne")
        default_button.clicked.connect(self.set_default_values)  # Połączenie zdarzenia kliknięcia przycisku z funkcją
        horizontal_layout.addWidget(default_button)

        # Dodanie poziomego układu do layoutu formularza
        form_layout.addRow(horizontal_layout)

        form_layout.addRow(QLabel(""))

        # Jednostka miary
        label_unit = QLabel("Jednostka miary:")
        label_unit.setStyleSheet("font-size: 12px;")
        unit_combobox = QComboBox()
        unit_combobox.addItem("mm")
        unit_combobox.addItem("cale")
        unit_combobox.setFixedWidth(100)
        unit_combobox.setStyleSheet("background-color: white;")
        form_layout.addRow(label_unit, unit_combobox)

        form_layout.addRow(QLabel(""))

        # Sposób wyrownania obiektow
        label_optimization = QLabel("Sposob wyrownania obiektow:")
        label_optimization.setStyleSheet("font-size: 12px;")

        self.optimization_combobox = QComboBox()
        self.optimization_combobox.addItem("CENTER")
        self.optimization_combobox.addItem("BOTTOM_LEFT")
        self.optimization_combobox.addItem("BOTTOM_RIGHT")
        self.optimization_combobox.addItem("TOP_LEFT")
        self.optimization_combobox.addItem("TOP_RIGHT")
        self.optimization_combobox.addItem("DONT_ALIGN")
        self.optimization_combobox.setFixedWidth(130)
        self.optimization_combobox.setStyleSheet("background-color: white;")
        form_layout.addRow(label_optimization, self.optimization_combobox)
        form_layout.addRow(QLabel(""))

        # Początkowy punkt
        label_starting_point = QLabel("Początkowy punkt:")
        label_starting_point.setStyleSheet("font-size: 12px;")

        self.starting_point_combobox = QComboBox()
        self.starting_point_combobox.addItems(["CENTER", "BOTTOM_LEFT", "BOTTOM_RIGHT", "TOP_LEFT", "TOP_RIGHT", "DONT_ALIGN"])
        self.starting_point_combobox.setFixedWidth(130)
        self.starting_point_combobox.setStyleSheet("background-color: white;")
        form_layout.addRow(label_starting_point, self.starting_point_combobox)
        form_layout.addRow(QLabel(""))

        # Ilość obrotów obiektu
        label_rotations = QLabel("Ilość obrotów obiektu:")
        label_rotations.setStyleSheet("font-size: 12px;")

        self.rotations_combobox = QComboBox()
        self.rotations_combobox.addItem("0")
        self.rotations_combobox.addItem("1")
        self.rotations_combobox.addItem("2")
        self.rotations_combobox.addItem("3")
        self.rotations_combobox.addItem("4")
        self.rotations_combobox.addItem("5")
        self.rotations_combobox.addItem("6")
        self.rotations_combobox.addItem("7")
        self.rotations_combobox.addItem("8")
        self.rotations_combobox.setFixedWidth(100)
        self.rotations_combobox.setStyleSheet("background-color: white;")
        form_layout.addRow(label_rotations, self.rotations_combobox)
        form_layout.addRow(QLabel(""))

        # Toleracja krzywizny
        label_tolerance = QLabel("Toleracja krzywizny:")
        label_tolerance.setStyleSheet("font-size: 12px;")
        self.tolerance_lineedit = QLineEdit()
        self.tolerance_lineedit.setFixedWidth(100)
        self.tolerance_lineedit.setStyleSheet("background-color: white;")
        form_layout.addRow(label_tolerance, self.tolerance_lineedit)

        form_layout.addRow(QLabel(""))

        # Użyj przybliżenia krawędzi
        use_edge_label = QLabel("Użyj przybliżenia krawędzi:")
        use_edge_label.setStyleSheet("font-size: 12px;")
        use_edge_checkbox = QCheckBox()
        use_edge_checkbox.setCheckState(Qt.Unchecked)
        form_layout.addRow(use_edge_label, use_edge_checkbox)

        form_layout.addRow(QLabel(""))

        # Liczba rdzeni
        label_cores = QLabel("Liczba rdzeni procesora:")
        label_cores.setStyleSheet("font-size: 12px;")
        cores_spinbox = QSpinBox()
        cores_spinbox.setFixedWidth(100)
        cores_spinbox.setStyleSheet("background-color: white;")
        form_layout.addRow(label_cores, cores_spinbox)


        form_layout.addRow(QLabel(""))
        form_layout.addRow(QLabel(""))

        # Konfiguracja narzędzi
        label_toolsConfiguration = QLabel("<b>Konfiguracja narzędzi:<b>")
        label_toolsConfiguration.setStyleSheet("font-size: 16px;")
        form_layout.addRow(label_toolsConfiguration)

        form_layout.addRow(QLabel(""))

        # Rodzaj narzędzia
        label_typeoftool = QLabel("Rodzaj narzędzia:")
        label_typeoftool.setStyleSheet("font-size: 12px;")
        self.tolerance_lineedit = QLineEdit()
        self.tolerance_lineedit.setFixedWidth(100)
        self.tolerance_lineedit.setStyleSheet("background-color: white;")
        form_layout.addRow(label_typeoftool, self.tolerance_lineedit)

        form_layout.addRow(QLabel(""))

        # Scal wspólne krawędzie
        use_mergecommonedges = QLabel("Scal wspólne krawędzie:")
        use_mergecommonedges.setStyleSheet("font-size: 12px;")
        use_edge_checkbox = QCheckBox()
        use_edge_checkbox.setCheckState(Qt.Unchecked)
        form_layout.addRow(use_mergecommonedges, use_edge_checkbox)

        form_layout.addRow(QLabel(""))

        # Przestrzeń między obiektami
        self.label_spacebetweenobjects = QLabel("Przestrzeń między obiektami:")
        self.label_spacebetweenobjects.setStyleSheet("font-size: 12px;")
        self.space_between_objects_lineedit = QLineEdit()
        self.space_between_objects_lineedit.setFixedWidth(100)
        self.space_between_objects_lineedit.setStyleSheet("background-color: white;")
        
        form_layout.addRow(self.label_spacebetweenobjects, self.space_between_objects_lineedit)

        form_layout.addRow(QLabel(""))

        # Dokladnosc optymalizacji
        label_optimizationfactor = QLabel("Dokładność optymalizacji:")
        label_optimizationfactor.setStyleSheet("font-size: 12px;")
        self.accuracy_lineedit = QLineEdit()
        self.accuracy_lineedit.setFixedWidth(100)
        self.accuracy_lineedit.setStyleSheet("background-color: white;")
        self.accuracy_lineedit.setToolTip("0.0 - 1.0")
        form_layout.addRow(label_optimizationfactor, self.accuracy_lineedit)


        form_layout.addRow(QLabel(""))
        form_layout.addRow(QLabel(""))

        
        # Regulacja meta-heurystyczna
        # label_metaheuristicregulation = QLabel("<b>Regulacja meta-heurystyczna:<b>")
        # label_metaheuristicregulation.setStyleSheet("font-size: 16px;")
        # form_layout.addRow(label_metaheuristicregulation)

        # form_layout.addRow(QLabel(""))

        # Populacja algorytmu genetycznego
        # label_geneticAlgPopulation = QLabel("Populacja algorytmu genetycznego:")
        # label_geneticAlgPopulation.setStyleSheet("font-size: 12px;")
        # tolerance_lineedit = QLineEdit()
        # tolerance_lineedit.setFixedWidth(100)
        # tolerance_lineedit.setStyleSheet("background-color: white;")
        # form_layout.addRow(label_geneticAlgPopulation, tolerance_lineedit)

        # form_layout.addRow(QLabel(""))

        # Wskaźnik mutacji algorytmu genetycznego
        # label_geneticAlgMutationRate = QLabel("Wskaźnik mutacji algorytmu genetycznego:")
        # label_geneticAlgMutationRate.setStyleSheet("font-size: 12px;")
        # tolerance_lineedit = QLineEdit()
        # tolerance_lineedit.setFixedWidth(100)
        # tolerance_lineedit.setStyleSheet("background-color: white;")
        # form_layout.addRow(label_geneticAlgMutationRate, tolerance_lineedit)

        # Regulacja heurystyczna
        label_hardwareConfiguration = QLabel("<b>Regulacja heurystyczna:<b>")
        label_hardwareConfiguration.setStyleSheet("font-size: 16px;")
        form_layout.addRow(label_hardwareConfiguration)

        form_layout.addRow(QLabel(""))

        # Czy explorować otwory XD
        label_explore_holes = QLabel("Explorować otwory:")
        label_explore_holes.setStyleSheet("font-size: 12px;")

        self.explore_holes_checkbox = QCheckBox()
        self.explore_holes_checkbox.setCheckState(Qt.Unchecked)  # domyslna FALSE
        self.explore_holes_checkbox.setStyleSheet("""
            font-size: 12px;
        """)

        form_layout.addRow(label_explore_holes, self.explore_holes_checkbox)
        form_layout.addRow(QLabel(""))


        # Czy uruchomić wątki równoległe
        label_parallel = QLabel("Czy uruchomić wątki równoległe:")
        label_parallel.setStyleSheet("font-size: 12px;")

        self.parallel_checkbox = QCheckBox()
        self.parallel_checkbox.setCheckState(Qt.Checked) # domyslna TRUE
        self.parallel_checkbox.setStyleSheet("""
            font-size: 12px;
        """)

        form_layout.addRow(label_parallel, self.parallel_checkbox)
        form_layout.addRow(QLabel(""))

        # Przycisk "Zatwierdź"
        self.submit_button = QPushButton("Zatwierdź")
        self.submit_button.clicked.connect(self.submit_value)
        form_layout.addRow(self.submit_button)

        # Prawa połowa (biała)
        right_half = QWidget(self)
        right_half.setStyleSheet("background-color: white;")
        right_layout = QVBoxLayout(right_half)
        label_right = QLabel("Tu będą ustawienia konfiguracyjne - prawa połowa")
        right_layout.addWidget(label_right)
        right_half.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        main_layout.addWidget(right_half, stretch=80)

        layout = QVBoxLayout()
        #self.setLayout(layout)

        label = QLabel("Prawa strona ustawień konfiguracyjnych")
        layout.addWidget(label)

    def set_default_values(self):
        # Ustawienie wartości domyślnych dla poszczególnych elementów
        self.space_between_objects_lineedit.setText("500")
        self.explore_holes_checkbox.setChecked(False)
        self.parallel_checkbox.setChecked(True)
        self.optimization_combobox.setCurrentIndex(0)
        self.accuracy_lineedit.setText("0.65")
        self.rotations_combobox.setCurrentIndex(4)
        self.starting_point_combobox.setCurrentIndex(0)

    def submit_value(self):
        # Get the text from line edits and comboboxes
        space_between_objects_text = self.space_between_objects_lineedit.text()
        accuracy_text = self.accuracy_lineedit.text()

        # space_between_objects = float(self.space_between_objects_lineedit.text())
        explore_holes = self.explore_holes_checkbox.isChecked()
        parallel = self.parallel_checkbox.isChecked()
        optimization = self.optimization_combobox.currentText()
        # accuracy = float(self.accuracy_lineedit.text())
        rotations = int(self.rotations_combobox.currentText())
        starting_point = self.starting_point_combobox.currentText()

        # Validate the input for space_between_objects
        try:
            space_between_objects = float(space_between_objects_text)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Space between objects must be a valid number.")
            return

        # Validate the input for accuracy
        try:
            accuracy = float(accuracy_text)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Accuracy must be a valid number.")
            return
        
        # Przekazanie wszystkich wartości do funkcji update w right_part
        self.right_part.update(space_between_objects, explore_holes, parallel, optimization, accuracy, rotations, starting_point)
        QMessageBox.information(self, "Success", "Configuration updated successfully.")


