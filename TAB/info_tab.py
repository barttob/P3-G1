from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene, QPushButton, QTextEdit, QFileDialog, QSlider
from PyQt5.QtGui import QPainter, QPen, QColor, QTextCursor, QBrush
from PyQt5.QtCore import Qt, QRectF

class InfoTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a QGraphicsView for visualization
        self.graphics_view = QGraphicsView()
        layout.addWidget(self.graphics_view)

        # Add a slider to control the visualization progress
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(100)  # Start with full visualization
        layout.addWidget(self.slider)
        
        import_button = QPushButton("Import G-code from file")
        import_button.clicked.connect(self.import_gcode)
        layout.addWidget(import_button)

        # Create a QGraphicsScene
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        self.slider.valueChanged.connect(self.update_visualization)

        # Initialize gcode_text attribute
        self.gcode_text = ""
        self.current_pos = (0, 0)  # Initialize current position\
        
        self.cut_time = 0
        self.speed = 0
        self.total_cutting_time = 0
        self.total_movement_time = 0
        self.total_distance_traveled = 0
        self.speed_sum = 0
        self.num_lines = 0

        self.stats_labels = {
            "Total Execution Time": QLabel("Całklowity czas pracy: 0 min"),
            "Total Cutting Time": QLabel("Czas cięcia: 0 min"),
            "Average Speed": QLabel("Średnia prędkość: 0 mm/min")
        }
        
        for label in self.stats_labels.values():
            layout.addWidget(label)

    def import_gcode(self):
        # Open a file dialog to select a G-code file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open G-code file", "", "G-code Files (*.gcode *.txt)")

        if file_path:
            # Read the contents of the file and set it to the QTextEdit
            with open(file_path, 'r') as file:
                self.gcode_text = file.read()

            self.visualize_gcode(self.gcode_text)

    def visualize_gcode(self, gcode_text, progress=100):
        # Clear the current scene
        self.scene.clear()

        pen = QPen(Qt.black)
        pen.setWidth(3)
        self.current_pos = (0, 0)

        gray_pen = QPen(Qt.lightGray)
        gray_pen.setWidth(2)

        # Set a custom dash pattern for the gray pen (dotted line with bigger spaces)
        dash_pattern = [4, 12]  # [length of dash, length of space]
        gray_pen.setDashPattern(dash_pattern)

        # Split the G-code text into lines
        lines = gcode_text.split('\n')

        # Calculate how many lines to visualize based on the progress
        num_lines = len(lines)
        lines_to_visualize = int(num_lines * progress / 100)

        # Tracks whether the current line is solid or dotted
        solid_line = True

        self.cut_time = 0
        self.speed = 0
        self.total_cutting_time = 0
        self.total_movement_time = 0
        self.total_distance_traveled = 0
        self.speed_sum = 0
        self.num_lines = 0

        for i, line in enumerate(lines[:lines_to_visualize]):
            # Split each line into parts
            parts = line[:-1].split()
            if not parts:
                continue

            # Parse the command and parameters
            command = parts[0]
            if command == 'M3':
                solid_line = True
            elif command == 'M5':
                solid_line = False
                continue  # Skip drawing if it's an M5 command
            elif command != 'G1':  # Skip lines that are not G1 commands
                continue

            params = {part[0]: float(part[1:]) for part in parts[1:]} if len(parts) > 1 else {}

            self.num_lines += 1
            if 'F' in params:
                self.speed = params['F']
            self.speed_sum += self.speed
                # print(self.speed)
                

            if 'X' in params:
                new_x = params['X']
                new_y = params.get('Y', self.current_pos[1])

                if solid_line:
                    pen.setStyle(Qt.SolidLine)
                    pen.setColor(Qt.black)
                else:
                    pen.setStyle(Qt.DotLine)
                    pen.setColor(Qt.red)
                self.scene.addLine(self.current_pos[0], self.current_pos[1], new_x, new_y, pen)
                diff_x = new_x - self.current_pos[0]
                diff_y = new_y - self.current_pos[1]
                self.total_cutting_time += (((diff_x)**2 + (diff_y)**2)**0.5) * self.speed / 100
                if solid_line:
                    self.cut_time += (((diff_x)**2 + (diff_y)**2)**0.5) * self.speed / 100
                self.current_pos = (new_x, new_y)
            elif 'Y' in params:
                new_x = params.get('X', self.current_pos[0])
                new_y = params['Y']

                if solid_line:
                    pen.setStyle(Qt.SolidLine)
                    pen.setColor(Qt.black)
                else:
                    pen.setStyle(Qt.DotLine)
                    pen.setColor(Qt.red)
                self.scene.addLine(self.current_pos[0], self.current_pos[1], new_x, new_y, pen)
                diff_x = new_x - self.current_pos[0]
                diff_y = new_y - self.current_pos[1]
                self.total_cutting_time += (((diff_x)**2 + (diff_y)**2)**0.5) * self.speed / 100
                if solid_line:
                    self.cut_time += (((diff_x)**2 + (diff_y)**2)**0.5) * self.speed / 100
                self.current_pos = (new_x, new_y)

            if i == lines_to_visualize - 1:
                circle_pen = QPen(Qt.black)
                circle_brush = QBrush(Qt.black)
                self.scene.addEllipse(new_x - 5, new_y - 5, 10, 10, circle_pen, circle_brush)

        for line in lines[lines_to_visualize:]:
            # Split each line into parts
            parts = line[:-1].split()
            if not parts:
                continue

            # Parse the command and parameters
            command = parts[0]
            if command == 'M3':
                solid_line = True
            elif command == 'M5':
                solid_line = False
                continue  # Skip drawing if it's an M5 command
            elif command != 'G1':  # Skip lines that are not G1 commands
                continue
            
            params = {part[0]: float(part[1:]) for part in parts[1:]} if len(parts) > 1 else {}

            self.num_lines += 1
            if 'F' in params:
                self.speed = params['F']
            self.speed_sum += self.speed
                # print(self.speed)
            
            if 'X' in params:
                new_x = params['X']
                new_y = params.get('Y', self.current_pos[1])

                if solid_line:
                    gray_pen.setStyle(Qt.SolidLine)
                    # gray_pen.setColor(Qt.lightGray)
                else:
                    gray_pen.setStyle(Qt.DotLine)
                    # gray_pen.setColor(Qt.lightRed)
                self.scene.addLine(self.current_pos[0], self.current_pos[1], new_x, new_y, gray_pen)
                diff_x = new_x - self.current_pos[0]
                diff_y = new_y - self.current_pos[1]
                self.total_cutting_time += (((diff_x)**2 + (diff_y)**2)**0.5) * self.speed / 100
                if solid_line:
                    self.cut_time += (((diff_x)**2 + (diff_y)**2)**0.5) * self.speed / 100
                self.current_pos = (new_x, new_y)
            elif 'Y' in params:
                new_x = params.get('X', self.current_pos[0])
                new_y = params['Y']

                if solid_line:
                    gray_pen.setStyle(Qt.SolidLine)
                    # gray_pen.setColor(Qt.lightGray)
                else:
                    gray_pen.setStyle(Qt.DotLine)
                    # gray_pen.setColor(Qt.lightRed)
                self.scene.addLine(self.current_pos[0], self.current_pos[1], new_x, new_y, gray_pen)
                diff_x = new_x - self.current_pos[0]
                diff_y = new_y - self.current_pos[1]
                self.total_cutting_time += (((diff_x)**2 + (diff_y)**2)**0.5) * self.speed / 100
                if solid_line:
                    self.cut_time += (((diff_x)**2 + (diff_y)**2)**0.5) * self.speed / 100
                self.current_pos = (new_x, new_y)
        
        self.stats_labels["Total Execution Time"].setText("Całkowity czas pracy: {} min".format(int(self.total_cutting_time  / 60)))
        self.stats_labels["Total Cutting Time"].setText("Czas cięcia: {} min".format(int(self.cut_time / 60)))
        self.stats_labels["Average Speed"].setText("Średnia prędkość: {:.2f} mm/min".format(self.speed_sum / self.num_lines))



    def update_visualization(self, value):
        # Update the visualization based on the slider's value
        progress = value
        self.visualize_gcode(self.gcode_text, progress)