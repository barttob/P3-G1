from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt
import xml.etree.ElementTree as ET
from xml.dom import minidom
import svg.path
import matplotlib.pyplot as plt
from pynest2d import *
import time

class RightPart(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label)
        
        # Create QGraphicsView and QGraphicsScene for embedding matplotlib plot
        self.graphics_view = QGraphicsView()
        layout.addWidget(self.graphics_view)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        self.setLayout(layout)
        self.inputPoints = []
        self.volume = Box(150000, 150000)
        self.initUI()
        
    def initUI(self):
        pass

    def display_file(self, file_path):
        self.file_label.setText(f"Selected file: {file_path}")
        doc = minidom.parse(file_path)
        path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]

        for path_str in path_strings:
            path = svg.path.parse_path(path_str)
            points = []
            for segment in path:
                if segment.start is not None:
                    points.append(Point(int(segment.start.real * 100), int(segment.start.imag  * 100)))
                if segment.end is not None:
                    points.append(Point(int(segment.end.real  * 100), int(segment.end.imag  * 100)))
            item = Item(points)
            self.inputPoints.append(item)

        num_bins = nest(self.inputPoints, self.volume)
        
        # Clear the scene before adding new items
        self.scene.clear()

        # Create a figure and axes for matplotlib plot
        fig, ax = plt.subplots(figsize=(8, 6), dpi=150)  # Increase figure size and DPI

        for item in self.inputPoints:
            x_values = []
            y_values = []
            transItem = item.transformedShape()
            rows = len(transItem.toString().strip().split('\n')) - 1
            for i in range(rows - 1):
                x_value = transItem.vertex(i).x()
                y_value = transItem.vertex(i).y()
                x_values.append(x_value)
                y_values.append(y_value)
            ax.plot(x_values, y_values, color='black', linewidth=1)  # Adjust linewidth

        # Set plot limits
        ax.set_xlim((-self.volume.width())/2, self.volume.width()/2)
        ax.set_ylim((-self.volume.height())/2, self.volume.height()/2)
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')  # Set equal aspect ratio

        # Save the figure to a temporary file
        tmp_file = "/tmp/plot.png"
        fig.savefig(tmp_file, format="png", transparent=True, bbox_inches="tight", pad_inches=0)

        # Load the saved image to QPixmap
        pixmap = QPixmap(tmp_file)

        # Add the QPixmap to QGraphicsScene
        self.scene.addPixmap(pixmap)

        # Set plot aspect ratio
        self.graphics_view.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.graphics_view.fitInView(0, 0, pixmap.width(), pixmap.height(), Qt.KeepAspectRatio)

        # Delete the matplotlib figure to release resources
        plt.close(fig)
