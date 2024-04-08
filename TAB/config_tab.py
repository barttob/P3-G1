<<<<<<< HEAD
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QComboBox, QSpinBox, QSizePolicy, QFormLayout, QMessageBox, QSlider
=======
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QComboBox, QSpinBox, QSizePolicy, QFormLayout, QMessageBox, QDialogButtonBox, QDialog
>>>>>>> g_code_parameters_extension
from PyQt5.QtCore import pyqtSignal, Qt
from TAB.main_tab.right_part import RightPart  # Import klasy RightPart

class ConfigTab(QWidget):

    def __init__(self, right_part):
        super().__init__()
        self.right_part = right_part
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)     
        self.tool_parameters = {}   

        # Lewa połowa 
        left_half = QWidget(self)
        left_half.setStyleSheet("background-color: rgb(142, 191, 250);")
        left_layout = QVBoxLayout(left_half)
        main_layout.addWidget(left_half, stretch=20)


        # Combo box to select tool
        self.tool_label = QLabel("Wybierz narzędzie:")
        self.tool_combobox = QComboBox()
        self.tool_combobox.addItems(["laser", "plazma", "stożek"])
        left_layout.addWidget(self.tool_label)
        left_layout.addWidget(self.tool_combobox)


        # Button to open tool parameters dialog
        self.open_tool_parameters_button = QPushButton("Otwórz parametry narzędzia")
        self.open_tool_parameters_button.clicked.connect(self.open_tool_parameters_dialog)
        left_layout.addWidget(self.open_tool_parameters_button)

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
        self.rotations_slider = QSlider(Qt.Horizontal)
        self.rotations_slider.setMinimum(0)
        self.rotations_slider.setMaximum(360)
        self.rotations_slider.setTickInterval(30)  # Odstęp między znacznikami
        form_layout.addRow(label_rotations, self.rotations_slider)
        form_layout.addRow(QLabel(""))

        # Utwórz etykietę do wyświetlania wartości suwaka
        self.rotations_value_label = QLabel('0')
        self.rotations_value_label.setAlignment(Qt.AlignCenter)

        # Połącz sygnał valueChanged suwaka z metodą update_rotation_label
        self.rotations_slider.valueChanged.connect(self.update_rotation_label)

        # Dodaj etykietę i suwak do układu poziomego
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.rotations_value_label)
        horizontal_layout.addWidget(self.rotations_slider)

        # Dodaj etykietę dla slidera do layoutu formularza
        form_layout.addRow(label_rotations, horizontal_layout)

        form_layout.addRow(QLabel(""))

        # Toleracja krzywizny
        # label_tolerance = QLabel("Toleracja krzywizny:")
        # label_tolerance.setStyleSheet("font-size: 12px;")
        # self.tolerance_lineedit = QLineEdit()
        # self.tolerance_lineedit.setFixedWidth(100)
        # self.tolerance_lineedit.setStyleSheet("background-color: white;")
        # form_layout.addRow(label_tolerance, self.tolerance_lineedit)

        # form_layout.addRow(QLabel(""))

        # Użyj przybliżenia krawędzi
        # use_edge_label = QLabel("Użyj przybliżenia krawędzi:")
        # use_edge_label.setStyleSheet("font-size: 12px;")
        # use_edge_checkbox = QCheckBox()
        # use_edge_checkbox.setCheckState(Qt.Unchecked)
        # form_layout.addRow(use_edge_label, use_edge_checkbox)

        # form_layout.addRow(QLabel(""))

        # Liczba rdzeni
        # label_cores = QLabel("Liczba rdzeni procesora:")
        # label_cores.setStyleSheet("font-size: 12px;")
        # cores_spinbox = QSpinBox()
        # cores_spinbox.setFixedWidth(100)
        # cores_spinbox.setStyleSheet("background-color: white;")
        # form_layout.addRow(label_cores, cores_spinbox)


        # form_layout.addRow(QLabel(""))
        # form_layout.addRow(QLabel(""))

        # Konfiguracja narzędzi
        label_toolsConfiguration = QLabel("<b>Konfiguracja narzędzi:<b>")
        label_toolsConfiguration.setStyleSheet("font-size: 16px;")
        form_layout.addRow(label_toolsConfiguration)

        form_layout.addRow(QLabel(""))

        # Rodzaj narzędzia
        label_tool = QLabel("Rodzaj narzędzia:")
        label_tool.setStyleSheet("font-size: 12px;")
        self.tool_combobox = QComboBox()
        self.tool_combobox.addItem("Laser")
        self.tool_combobox.addItem("Plazma")
        self.tool_combobox.addItem("Stożkowy")
        self.tool_combobox.setFixedWidth(130)
        self.tool_combobox.setStyleSheet("background-color: white;")
        self.tool_combobox.currentIndexChanged.connect(self.update_space_between_objects)
        form_layout.addRow(label_tool, self.tool_combobox)

        form_layout.addRow(QLabel(""))

        # Checkbox to enable/disable editing
        self.spacing_checkbox = QCheckBox("Ręczna regulacja przestrzeni")
        self.spacing_checkbox.setChecked(False)  # Initially unchecked
        self.spacing_checkbox.stateChanged.connect(self.toggle_spacing_editable)
        form_layout.addRow(self.spacing_checkbox)  # Add checkbox to toggle edit mode

        # Przestrzeń między obiektami
        self.label_spacebetweenobjects = QLabel("Przestrzeń między obiektami:")
        self.label_spacebetweenobjects.setStyleSheet("font-size: 12px;")
        self.space_between_objects_lineedit = QLineEdit()
        self.space_between_objects_lineedit.setFixedWidth(100)
        self.space_between_objects_lineedit.setStyleSheet("background-color: white;")
        self.space_between_objects_lineedit.setReadOnly(True)  # Set initially read-only
        
        form_layout.addRow(self.label_spacebetweenobjects, self.space_between_objects_lineedit)

        # Call toggle_spacing_editable initially to set correct style
        self.toggle_spacing_editable(self.spacing_checkbox.isChecked())
        
        form_layout.addRow(QLabel(""))

        # Scal wspólne krawędzie
        # use_mergecommonedges = QLabel("Scal wspólne krawędzie:")
        # use_mergecommonedges.setStyleSheet("font-size: 12px;")
        # use_edge_checkbox = QCheckBox()
        # use_edge_checkbox.setCheckState(Qt.Unchecked)
        # form_layout.addRow(use_mergecommonedges, use_edge_checkbox)

        # form_layout.addRow(QLabel(""))

        # Regulacja heurystyczna
        label_hardwareConfiguration = QLabel("<b>Regulacja heurystyczna:<b>")
        label_hardwareConfiguration.setStyleSheet("font-size: 16px;")
        form_layout.addRow(label_hardwareConfiguration)

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


        # Czy wykorzystac wielowatkowosc
        label_parallel = QLabel("Wielowątkowość:")
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
        self.space_between_objects_lineedit.setText("0.3")
        self.explore_holes_checkbox.setChecked(False)
        self.parallel_checkbox.setChecked(True)
        self.optimization_combobox.setCurrentIndex(0)
        self.accuracy_lineedit.setText("0.65")
        #self.rotations_combobox.setCurrentIndex(4)
        self.starting_point_combobox.setCurrentIndex(0)
        self.rotations_slider.setValue(4)
        self.tool_combobox.setCurrentIndex(0)


    def open_tool_parameters_dialog(self):
        tool = self.tool_combobox.currentText()
        self.dialog = QDialog()  # Tworzenie okna dialogowego i przypisanie do atrybutu self.dialog

        form_layout = QFormLayout(self.dialog)  # Użyj self.dialog zamiast dialog

        if tool == "laser":
            # Tworzymy lub aktualizujemy słownik parametrów dla lasera
            self.tool_parameters['laser'] = {
                'type_tool': tool,  # Dodaj pole type_tool
                'cutting_speed': QLineEdit(),
                'speed_movement': QLineEdit(),
                'cutting_depth': QLineEdit(),
                'downtime': QLineEdit(),
                'unit': QComboBox(),  # Dodaj QComboBox
                'custom_header': QLineEdit(),
                'custom_footer': QLineEdit()
            }
            
            # Dodaj elementy do QComboBox
            self.tool_parameters['laser']['unit'].addItems(["mm", "cale"])  # Dodaj elementy do QComboBox

            form_layout.addRow("Prędkość cięcia:", self.tool_parameters['laser']['cutting_speed'])
            form_layout.addRow("Prędkość ruchu:", self.tool_parameters['laser']['speed_movement'])
            form_layout.addRow("Głębokość cięcia:", self.tool_parameters['laser']['cutting_depth'])
            form_layout.addRow("Czas przestoju:", self.tool_parameters['laser']['downtime'])
            form_layout.addRow("Jednostka:", self.tool_parameters['laser']['unit'])
            form_layout.addRow("Niestandardowy nagłówek:", self.tool_parameters['laser']['custom_header'])
            form_layout.addRow("Niestandardowy stopka:", self.tool_parameters['laser']['custom_footer'])

            # Set default values for all parameters
            default_button = QPushButton("Ustaw domyślne")
            default_button.clicked.connect(lambda: self.set_default_values_for_tools('laser'))
            form_layout.addRow(default_button)
        elif tool == "plazma":
            # Podobnie jak dla lasera, tworzymy lub aktualizujemy słownik parametrów dla plazmy
            self.tool_parameters['plazma'] = {
                'type_tool': tool,  # Dodaj pole type_tool
                'plasma_power': QLineEdit(),
                'plasma_speed': QLineEdit()
            }

            form_layout.addRow("Moc plazmy:", self.tool_parameters['plazma']['plasma_power'])
            form_layout.addRow("Prędkość plazmy:", self.tool_parameters['plazma']['plasma_speed'])

            # Set default values for all parameters
            default_button = QPushButton("Ustaw domyślne")
            default_button.clicked.connect(lambda: self.set_default_values_for_tools('plazma'))
            form_layout.addRow(default_button)
        elif tool == "stożek":
            # Analogicznie dla stożka
            self.tool_parameters['stożek'] = {
                'type_tool': tool,  # Dodaj pole type_tool
                'cone_power': QLineEdit(),
                'cone_speed': QLineEdit()
            }

            form_layout.addRow("Moc stożka:", self.tool_parameters['stożek']['cone_power'])
            form_layout.addRow("Prędkość stożka:", self.tool_parameters['stożek']['cone_speed'])

            # Set default values for all parameters
            default_button = QPushButton("Ustaw domyślne")
            default_button.clicked.connect(lambda: self.set_default_values_for_tools('stożek'))
            form_layout.addRow(default_button)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save_parameters)
        button_box.rejected.connect(self.dialog.reject)

        form_layout.addRow(button_box)

        if self.dialog.exec_():
            # Do something with the parameters entered in the dialog
            pass



    def set_default_values_for_tools(self, tool):
        # Tutaj ustawiamy domyślne wartości dla danego narzędzia
        if tool == "laser":
            self.tool_parameters['laser']['cutting_speed'].setText("103")
            self.tool_parameters['laser']['speed_movement'].setText("10")
            self.tool_parameters['laser']['cutting_depth'].setText("12")
            self.tool_parameters['laser']['downtime'].setText("29")
            self.tool_parameters['laser']['unit'].setCurrentIndex(0)
            self.tool_parameters['laser']['custom_header'].setText("M10")
            self.tool_parameters['laser']['custom_footer'].setText("M24")
        elif tool == "plazma":
            self.tool_parameters['plazma']['plasma_power'].setText("34")
            self.tool_parameters['plazma']['plasma_speed'].setText("25")
        elif tool == "stożek":
            self.tool_parameters['stożek']['cone_power'].setText("123")
            self.tool_parameters['stożek']['cone_speed'].setText("23")

    def save_parameters(self):
        tool = self.tool_combobox.currentText()
        current_tool_params = self.tool_parameters.get(tool)
        
        if current_tool_params:
            # Zapisz parametry dla aktualnie wybranego narzędzia
            saved_params = {'type_tool': tool}  # Utwórz słownik dla zapisanych parametrów, włączając typ narzędzia
            for param_name, param_widget in current_tool_params.items():
                if isinstance(param_widget, QLineEdit):
                    saved_params[param_name] = param_widget.text()
                elif isinstance(param_widget, QComboBox):
                    saved_params[param_name] = param_widget.currentText()

            self.saved_parameters = saved_params
            print("Zapisane parametry:", self.saved_parameters)  # Wyświetlenie zapisanych parametrów w konsoli

            # Utwórz listę narzędzi do usunięcia
            tools_to_remove = []
            for other_tool in list(self.tool_parameters.keys()):  # Utwórz kopię kluczy słownika przed iteracją
                if other_tool != tool:
                    # Dodaj narzędzie do listy narzędzi do usunięcia
                    tools_to_remove.append(other_tool)
            
            # Iteruj po liście narzędzi do usunięcia i usuń je ze słownika
            for tool_to_remove in tools_to_remove:
                self.tool_parameters.pop(tool_to_remove)

        # Wyświetl kolejne okno dialogowe z zawartością słownika
        self.display_dictionary_dialog(self.saved_parameters)

    def display_dictionary_dialog(self, saved_params):
        # Utwórz nowe okno dialogowe
        dictionary_dialog = QDialog()
        layout = QFormLayout(dictionary_dialog)

        # Wyświetl zawartość słownika
        for key, value in saved_params.items():
            label = QLabel(key)
            field = QLabel(str(value))
            layout.addRow(label, field)

        dictionary_dialog.exec_()



        # Przekazanie parametrów do right part
        #self.right_part.sended_tool_param(self.saved_parameters)



      






    ###############################################################################

    def submit_value(self):
        # Sprawdź, czy saved_parameters nie jest puste
        if not hasattr(self, 'saved_parameters') or not self.saved_parameters:
            QMessageBox.information(self, "Błąd", "Uzupełnij parametry narzędzia.")
            return

        # Get the text from line edits and comboboxes
        space_between_objects_text = self.space_between_objects_lineedit.text()
        accuracy_text = self.accuracy_lineedit.text()

<<<<<<< HEAD
        # space_between_objects = float(self.space_between_objects_lineedit.text())
        explore_holes = self.explore_holes_checkbox.isChecked()
        parallel = self.parallel_checkbox.isChecked()
        optimization = self.optimization_combobox.currentText()
        # accuracy = float(self.accuracy_lineedit.text())
        #rotations = int(self.rotations_combobox.currentText())
        starting_point = self.starting_point_combobox.currentText()
        rotations = self.rotations_slider.value()

=======
>>>>>>> g_code_parameters_extension
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

        # space_between_objects = float(self.space_between_objects_lineedit.text())
        explore_holes = self.explore_holes_checkbox.isChecked()
        parallel = self.parallel_checkbox.isChecked()
        optimization = self.optimization_combobox.currentText()
        # accuracy = float(self.accuracy_lineedit.text())
        rotations = int(self.rotations_combobox.currentText())
        starting_point = self.starting_point_combobox.currentText()

        # Przekazanie wszystkich wartości do funkcji update w right_part
        self.right_part.update(space_between_objects, explore_holes, parallel, optimization, accuracy, rotations, starting_point)

        # Przekazanie parametrów ustawień narzędzia do right part do funkcji
        self.right_part.sended_tool_param(self.saved_parameters)

        QMessageBox.information(self, "Success", "Configuration updated successfully.")
    
    def update_rotation_label(self, value):
        # Metoda wywoływana za każdym razem, gdy wartość suwaka się zmienia
        self.rotations_value_label.setText(str(value))

    def update_space_between_objects(self, index):
        if index == 0:  # Laser
            self.space_between_objects_lineedit.setText("0.3")
        elif index == 1:  # Plazma
            self.space_between_objects_lineedit.setText("4")
        elif index == 2:  # Stożkowy
            self.space_between_objects_lineedit.setText("20")
    
    def toggle_spacing_editable(self, state):
        if state == Qt.Checked:
            self.space_between_objects_lineedit.setReadOnly(False)
            self.space_between_objects_lineedit.setStyleSheet("background-color: white;")  # Set editable background color
        else:
            self.space_between_objects_lineedit.setReadOnly(True)
            self.space_between_objects_lineedit.setStyleSheet("background-color: lightgrey;")  # Set read-only background color



