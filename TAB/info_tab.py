from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene, QPushButton, QTextEdit, QFileDialog, QSlider, QHBoxLayout
from PyQt5.QtGui import QPainter, QPen, QColor, QTextCursor, QBrush
from PyQt5.QtCore import Qt, QRectF, QTimer


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

        if 0.05 < newScale < 100:  # Ogranicz zakres skalowania np. od 0.05x do 10x
            self.scale(scaleFactor, scaleFactor)
    
    def resetZoom(self):
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

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

class InfoTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a QGraphicsView for visualization
        self.graphics_view = ZoomableGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        layout.addWidget(self.graphics_view)

        # Add a slider to control the visualization progress
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(100)  # Start with full visualization
        layout.addWidget(self.slider)
        
        button_layout = QHBoxLayout()

        import_button = QPushButton("Import G-code from file")
        import_button.clicked.connect(self.import_gcode)
        button_layout.addWidget(import_button)

        # Add a button to start automatic slider movement
        self.auto_move_button = QPushButton("Start Auto Move")
        button_layout.addWidget(self.auto_move_button)
        self.auto_move_button.clicked.connect(self.start_auto_move)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        # Create a QGraphicsScene
        # self.scene = QGraphicsScene()
        # self.graphics_view.setScene(self.scene)

        # self.graphics_view = ZoomableGraphicsView()
        # self.scene = QGraphicsScene()
        # self.graphics_view.setScene(self.scene)
        # layout.addWidget(self.graphics_view)

        self.slider.valueChanged.connect(self.update_visualization)

        # Initialize gcode_text attribute
        self.gcode_text = ""
        self.current_pos = (0, 0)  # Initialize current position
        self.slider.setEnabled(bool(self.gcode_text))
        
        self.cut_time = 0
        self.speed = 0
        self.total_cutting_time = 0
        self.total_movement_time = 0
        self.total_distance_traveled = 0
        self.speed_sum = 0
        self.num_lines = 1

        self.stats_labels = {
            "Total Execution Time": QLabel("Całklowity czas pracy: 0 min"),
            "Total Cutting Time": QLabel("Czas cięcia: 0 min"),
            "Average Speed": QLabel("Średnia prędkość: 0 mm/s"),
            "Total Distance": QLabel("Całkowita długość ruchu: 0 mm"),
            "Cutting Distance": QLabel("Całkowita długość cięcia: 0 mm")
        }
        
        for label in self.stats_labels.values():
            layout.addWidget(label)

        # Timer for automatic slider movement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.increment_slider_value)

        

    def start_auto_move(self):
        if self.timer.isActive():
            self.timer.stop()
            self.auto_move_button.setText("Start Auto Move")
        else:
            self.slider.setValue(0)
            self.timer.start(100)  # Adjust the interval (milliseconds) as needed for the desired speed
            self.auto_move_button.setText("Stop Auto Move")

    def increment_slider_value(self):
        # Increment the slider's value and stop the timer when it reaches the maximum value
        if self.slider.value() < self.slider.maximum():
            self.slider.setValue(self.slider.value() + 1)
        else:
            self.timer.stop()

    def import_gcode(self):
        # Open a file dialog to select a G-code file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open G-code file", "", "G-code Files (*.gcode *.txt)")

        if file_path:
            # Read the contents of the file and set it to the QTextEdit
            with open(file_path, 'r') as file:
                self.gcode_text = file.read()

            self.visualize_gcode(self.gcode_text)

    def set_gcode_text(self, gcode_text):
        # Set the G-code text and visualize it
        self.gcode_text = gcode_text
        self.visualize_gcode(gcode_text)

    def visualize_gcode(self, gcode_text, progress=100):
        self.slider.setEnabled(bool(self.gcode_text))
        # Clear the current scene
        self.scene.clear()

        pen = QPen(Qt.black)
        pen.setWidth(3)
        pen.setCosmetic(True)
        self.current_pos = (0, 0)

        gray_pen = QPen(Qt.lightGray)
        gray_pen.setWidth(2)
        gray_pen.setCosmetic(True)

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
        self.total_distance = 0
        self.cutting_distance = 0
        self.speed_sum = 0
        self.num_lines = 0

        prev_x, prev_y = None, None
        for i, line in enumerate(lines[:lines_to_visualize]):
            # Split each line into parts
            parts = line[:-1].split()
            if not parts:
                continue

            # Parse the command and parameters
            command = parts[0]
            # print(command)
            if command == 'M3' or command == 'M30' or command == 'M300':
                solid_line = True
                # print(solid_line)
            elif command == 'M5':
                solid_line = False
                # print(solid_line)
                continue  # Skip drawing if it's an M5 command
            elif command != 'G1':  # Skip lines that are not G1 commands
                continue


            if command.startswith('G') or command.startswith('M'):
                params = {part[0]: float(part[1:]) for part in parts[1:]} if len(parts) > 1 else {}

            self.num_lines += 1
            if 'F' in params and solid_line == False and 'Z' not in params:
                self.speed = params['F']
            self.speed_sum += self.speed
                # print(self.speed)
                

            if 'X' in params:
                new_x = params['X']
                new_y = params.get('Y', self.current_pos[1])
                new_x = new_x / 100
                new_y = new_y / 100

                if prev_x != new_x or prev_y != new_y:
                    if solid_line:
                        pen.setStyle(Qt.SolidLine)
                        pen.setColor(Qt.black)
                    else:
                        pen.setStyle(Qt.DotLine)
                        pen.setColor(Qt.red)
                    self.scene.addLine(self.current_pos[0], self.current_pos[1], new_x, new_y, pen)
                    diff_x = new_x - self.current_pos[0]
                    diff_y = new_y - self.current_pos[1]
                    if self.speed != 0:
                        self.total_cutting_time += (((diff_x)**2 + (diff_y)**2)**0.5) / self.speed
                        self.total_distance += (((diff_x)**2 + (diff_y)**2)**0.5)
                        if solid_line:
                            self.cut_time += (((diff_x)**2 + (diff_y)**2)**0.5) / self.speed
                            self.cutting_distance += (((diff_x)**2 + (diff_y)**2)**0.5)
                    self.current_pos = (new_x, new_y)
                prev_x, prev_y = new_x, new_y
            elif 'Y' in params:
                new_x = params.get('X', self.current_pos[0])
                new_y = params['Y']
                new_x = new_x / 100
                new_y = new_y / 100

                if prev_x != new_x or prev_y != new_y:
                    if solid_line:
                        pen.setStyle(Qt.SolidLine)
                        pen.setColor(Qt.black)
                    else:
                        pen.setStyle(Qt.DotLine)
                        pen.setColor(Qt.red)
                    self.scene.addLine(self.current_pos[0], self.current_pos[1], new_x, new_y, pen)
                    diff_x = new_x - self.current_pos[0]
                    diff_y = new_y - self.current_pos[1]
                    if self.speed != 0:
                        self.total_cutting_time += (((diff_x)**2 + (diff_y)**2)**0.5) / self.speed
                        self.total_distance += (((diff_x)**2 + (diff_y)**2)**0.5)
                        if solid_line:
                            self.cut_time += (((diff_x)**2 + (diff_y)**2)**0.5) / self.speed
                            self.cutting_distance += (((diff_x)**2 + (diff_y)**2)**0.5)
                    self.current_pos = (new_x, new_y)
                prev_x, prev_y = new_x, new_y
            # if i == lines_to_visualize - 1:
            #     circle_pen = QPen(Qt.black)
            #     circle_brush = QBrush(Qt.black)
            #     self.scene.addEllipse(new_x - 5, new_y - 5, 10, 10, circle_pen, circle_brush)
        

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

            if command.startswith('G') or command.startswith('M'):
                params = {part[0]: float(part[1:]) for part in parts[1:]} if len(parts) > 1 else {}

            self.num_lines += 1
            if 'F' in params and solid_line == False:
                self.speed = params['F']
            self.speed_sum += self.speed
                # print(self.speed)

            if 'X' in params:
                new_x = params['X']
                new_y = params.get('Y', self.current_pos[1])
                new_x = new_x / 100
                new_y = new_y / 100

                if prev_x != new_x or prev_y != new_y:
                    if solid_line:
                        gray_pen.setStyle(Qt.SolidLine)
                        # gray_pen.setColor(Qt.lightGray)
                    else:
                        gray_pen.setStyle(Qt.DotLine)
                        # gray_pen.setColor(Qt.lightRed)
                    self.scene.addLine(self.current_pos[0], self.current_pos[1], new_x, new_y, gray_pen)
                    diff_x = new_x - self.current_pos[0]
                    diff_y = new_y - self.current_pos[1]
                    if self.speed != 0:
                        self.total_cutting_time += (((diff_x)**2 + (diff_y)**2)**0.5) / self.speed
                        self.total_distance += (((diff_x)**2 + (diff_y)**2)**0.5) 
                        if solid_line:
                            self.cut_time += (((diff_x)**2 + (diff_y)**2)**0.5) / self.speed
                            self.cutting_distance += (((diff_x)**2 + (diff_y)**2)**0.5)
                    self.current_pos = (new_x, new_y)
                prev_x, prev_y = new_x, new_y
            elif 'Y' in params:
                new_x = params.get('X', self.current_pos[0])
                new_y = params['Y']
                new_x = new_x / 100
                new_y = new_y / 100

                if prev_x != new_x or prev_y != new_y:
                    if solid_line:
                        gray_pen.setStyle(Qt.SolidLine)
                        # gray_pen.setColor(Qt.lightGray)
                    else:
                        gray_pen.setStyle(Qt.DotLine)
                        # gray_pen.setColor(Qt.lightRed)
                    self.scene.addLine(self.current_pos[0], self.current_pos[1], new_x, new_y, gray_pen)
                    diff_x = new_x - self.current_pos[0]
                    diff_y = new_y - self.current_pos[1]
                    if self.speed != 0:
                        self.total_cutting_time += (((diff_x)**2 + (diff_y)**2)**0.5) / self.speed
                        self.total_distance += (((diff_x)**2 + (diff_y)**2)**0.5)
                        if solid_line:
                            self.cut_time += (((diff_x)**2 + (diff_y)**2)**0.5) / self.speed
                            self.cutting_distance += (((diff_x)**2 + (diff_y)**2)**0.5)
                    self.current_pos = (new_x, new_y)
                prev_x, prev_y = new_x, new_y

        self.graphics_view.setRenderHint(QPainter.NonCosmeticDefaultPen)  # This line ensures that the line width remains constant when the view is scaled
        self.graphics_view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.graphics_view.setTransformationAnchor(QGraphicsView.NoAnchor)  # This line disables the transformation anchor
        self.graphics_view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        
        total_execution_time = int(self.total_cutting_time)
        total_execution_minutes = total_execution_time // 60
        total_execution_seconds = total_execution_time % 60
        self.stats_labels["Total Execution Time"].setText("Całkowity czas pracy: {} min {} sec".format(total_execution_minutes, total_execution_seconds))

        cutting_time = int(self.cut_time)
        cutting_minutes = cutting_time // 60
        cutting_seconds = cutting_time % 60
        self.stats_labels["Total Cutting Time"].setText("Czas cięcia: {} min {} sec".format(cutting_minutes, cutting_seconds))
        
        self.stats_labels["Average Speed"].setText("Średnia prędkość: {:.2f} mm/s".format(self.speed_sum / self.num_lines))
        self.stats_labels["Total Distance"].setText("Całkowita długość ruchu: {:.0f} mm".format(self.total_distance))
        self.stats_labels["Cutting Distance"].setText("Całkowita długość cięcia: {:.0f} mm".format(self.cutting_distance))



    def update_visualization(self, value):
        # Update the visualization based on the slider's value
        progress = value
        self.visualize_gcode(self.gcode_text, progress)
        # self.graphics_view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)