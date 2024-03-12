from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QComboBox, QSpinBox, QSizePolicy, QFormLayout


class ConfigTab(QWidget):
    def __init__(self):
        super().__init__()

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
        horizontal_layout.addWidget(QPushButton("Ustaw domyślne"))

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

        # Typ optymalizacji
        label_optimization = QLabel("Typ optymalizacji:")
        label_optimization.setStyleSheet("font-size: 12px;")
        optimization_lineedit = QLineEdit()
        optimization_lineedit.setFixedWidth(100)
        optimization_lineedit.setStyleSheet("background-color: white;")
        form_layout.addRow(label_optimization, optimization_lineedit)

        form_layout.addRow(QLabel(""))

        # Ilość obrotów obiektu
        label_rotations = QLabel("Ilość obrotów obiektu:")
        label_rotations.setStyleSheet("font-size: 12px;")
        rotations_spinbox = QSpinBox()
        rotations_spinbox.setFixedWidth(100)
        rotations_spinbox.setStyleSheet("background-color: white;")
        form_layout.addRow(label_rotations, rotations_spinbox)

        form_layout.addRow(QLabel(""))

        # Toleracja krzywizny
        label_tolerance = QLabel("Toleracja krzywizny:")
        label_tolerance.setStyleSheet("font-size: 12px;")
        tolerance_lineedit = QLineEdit()
        tolerance_lineedit.setFixedWidth(100)
        tolerance_lineedit.setStyleSheet("background-color: white;")
        form_layout.addRow(label_tolerance, tolerance_lineedit)

        form_layout.addRow(QLabel(""))

        # Użyj przybliżenia krawędzi
        use_edge_label = QLabel("Użyj przybliżenia krawędzi:")
        use_edge_label.setStyleSheet("font-size: 12px;")
        use_edge_checkbox = QCheckBox()
        form_layout.addRow(use_edge_label, use_edge_checkbox)

        form_layout.addRow(QLabel(""))

        # Liczba rdzeni
        label_cores = QLabel("Liczba rdzeni:")
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
        tolerance_lineedit = QLineEdit()
        tolerance_lineedit.setFixedWidth(100)
        tolerance_lineedit.setStyleSheet("background-color: white;")
        form_layout.addRow(label_typeoftool, tolerance_lineedit)

        form_layout.addRow(QLabel(""))

        # Scal wspólne krawędzie
        use_mergecommonedges = QLabel("Scal wspólne krawędzie:")
        use_mergecommonedges.setStyleSheet("font-size: 12px;")
        use_edge_checkbox = QCheckBox()
        form_layout.addRow(use_mergecommonedges, use_edge_checkbox)

        form_layout.addRow(QLabel(""))

        # Przestrzeń między obiektami
        label_spacebetweenobjects = QLabel("Przestrzeń między obiektami:")
        label_spacebetweenobjects.setStyleSheet("font-size: 12px;")
        tolerance_lineedit = QLineEdit()
        tolerance_lineedit.setFixedWidth(100)
        tolerance_lineedit.setStyleSheet("background-color: white;")
        form_layout.addRow(label_spacebetweenobjects, tolerance_lineedit)

        form_layout.addRow(QLabel(""))

        # Współczynnik optymalizacji
        label_optimizationfactor = QLabel("Współczynnik optymalizacji:")
        label_optimizationfactor.setStyleSheet("font-size: 12px;")
        tolerance_lineedit = QLineEdit()
        tolerance_lineedit.setFixedWidth(100)
        tolerance_lineedit.setStyleSheet("background-color: white;")
        form_layout.addRow(label_optimizationfactor, tolerance_lineedit)


        form_layout.addRow(QLabel(""))
        form_layout.addRow(QLabel(""))

        
        # Regulacja meta-heurystyczna
        label_metaheuristicregulation = QLabel("<b>Regulacja meta-heurystyczna:<b>")
        label_metaheuristicregulation.setStyleSheet("font-size: 16px;")
        form_layout.addRow(label_metaheuristicregulation)

        form_layout.addRow(QLabel(""))

        # Populacja algorytmu genetycznego
        label_geneticAlgPopulation = QLabel("Populacja algorytmu genetycznego:")
        label_geneticAlgPopulation.setStyleSheet("font-size: 12px;")
        tolerance_lineedit = QLineEdit()
        tolerance_lineedit.setFixedWidth(100)
        tolerance_lineedit.setStyleSheet("background-color: white;")
        form_layout.addRow(label_geneticAlgPopulation, tolerance_lineedit)

        form_layout.addRow(QLabel(""))

        # Wskaźnik mutacji algorytmu genetycznego
        label_geneticAlgMutationRate = QLabel("Wskaźnik mutacji algorytmu genetycznego:")
        label_geneticAlgMutationRate.setStyleSheet("font-size: 12px;")
        tolerance_lineedit = QLineEdit()
        tolerance_lineedit.setFixedWidth(100)
        tolerance_lineedit.setStyleSheet("background-color: white;")
        form_layout.addRow(label_geneticAlgMutationRate, tolerance_lineedit)


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
