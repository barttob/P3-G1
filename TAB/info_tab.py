from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene, QPushButton, QTextEdit, QFileDialog, QSlider
from PyQt5.QtGui import QPainter, QPen, QColor, QTextCursor, QBrush
from PyQt5.QtCore import Qt, QRectF

class InfoTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Visualization of G-code")
        layout.addWidget(label)

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
        self.current_pos = (0, 0)  # Initialize current position

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
        pen.setWidth(2)
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

            if 'X' in params:
                new_x = params['X']
                new_y = params.get('Y', self.current_pos[1])

                if solid_line:
                    pen.setStyle(Qt.SolidLine)
                else:
                    pen.setStyle(Qt.DotLine)
                self.scene.addLine(self.current_pos[0], self.current_pos[1], new_x, new_y, pen)
                self.current_pos = (new_x, new_y)
            elif 'Y' in params:
                new_x = params.get('X', self.current_pos[0])
                new_y = params['Y']

                if solid_line:
                    pen.setStyle(Qt.SolidLine)
                else:
                    pen.setStyle(Qt.DotLine)
                self.scene.addLine(self.current_pos[0], self.current_pos[1], new_x, new_y, pen)
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
            
            if 'X' in params:
                new_x = params['X']
                new_y = params.get('Y', self.current_pos[1])

                if solid_line:
                    gray_pen.setStyle(Qt.SolidLine)
                else:
                    gray_pen.setStyle(Qt.DotLine)
                self.scene.addLine(self.current_pos[0], self.current_pos[1], new_x, new_y, gray_pen)
                self.current_pos = (new_x, new_y)
            elif 'Y' in params:
                new_x = params.get('X', self.current_pos[0])
                new_y = params['Y']

                if solid_line:
                    gray_pen.setStyle(Qt.SolidLine)
                else:
                    gray_pen.setStyle(Qt.DotLine)
                self.scene.addLine(self.current_pos[0], self.current_pos[1], new_x, new_y, gray_pen)
                self.current_pos = (new_x, new_y)




    def update_visualization(self, value):
        # Update the visualization based on the slider's value
        progress = value
        self.visualize_gcode(self.gcode_text, progress)
