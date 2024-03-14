import xml.etree.ElementTree as ET
from xml.dom import minidom
from svg.path import parse_path, Line
from pynest2d import *

class Parser():
    def __init__(self, file_path):
        super().__init__()
        self.inputPoints = []
        self.file_label = file_path

    def parse_svg(self):
        doc = minidom.parse(self.file_label)
        path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]

        for path_str in path_strings:
            print(path_str)
            path = parse_path(path_str)
            print(path)
            points = []
            for segment in path:
                if isinstance(segment, Line):
                    points.append(Point(int(segment.start.real * 100), int(segment.end.real * 100)))
                # if segment.end is not None:
                #     points.append(Point(int(segment.end.real  * 100), int(segment.end.imag  * 100)))
            item = Item(points)
            self.inputPoints.append(item)
        print(self.inputPoints[0])
        print(self.inputPoints[1])
        return self.inputPoints
    
    def parse_dxf(self):
        pass

    