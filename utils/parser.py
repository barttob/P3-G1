import xml.etree.ElementTree as ET
from xml.dom import minidom
from svg.path import parse_path, Line, CubicBezier, QuadraticBezier, Arc
from pynest2d import *
import ezdxf

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
            self.svg_parse_points = []
            self.extract_points_from_path(path)
            item = Item(self.svg_parse_points)
            self.inputPoints.append(item)
        print(self.inputPoints[0])
        print(self.inputPoints[1])
        return self.inputPoints
    
    def extract_points_from_path(self, path):
        for segment in path:
                if isinstance(segment, Line):
                    self.points_on_line(segment)
                elif isinstance(segment, CubicBezier):
                    self.points_on_cubic_bezier(segment)
                elif isinstance(segment, QuadraticBezier):
                    self.points_on_quadratic_bezier(segment)
                elif isinstance(segment, Arc):
                    self.points_on_arc(segment)

    def points_on_line(self, line):
        self.svg_parse_points.append(Point(int(line.start.real * 100), int(line.end.real * 100)))

    def points_on_cubic_bezier(self, bezier):
        for t in range(0, 101, 5):  # Sample 20 points on the curve
            point = bezier.point(t / 100)
            self.svg_parse_points.append(Point(int(point.real * 100), int(point.imag * 100)))

    def points_on_quadratic_bezier(self, bezier):
        for t in range(0, 101, 5):  # Sample 20 points on the curve
            point = bezier.point(t / 100)
            self.svg_parse_points.append(Point(int(point.real * 100), int(point.imag * 100)))

    def points_on_arc(self, arc):
        for t in range(0, 101, 5):  # Sample 20 points on the arc
            point = arc.point(t / 100)
            self.svg_parse_points.append(Point(int(point.real * 100), int(point.imag * 100)))




    
    def parse_dxf(self):
        doc = ezdxf.readfile(self.file_label)
        msp = doc.modelspace()
        
        for entity in msp:
            if entity.dxftype() == 'LINE':
                start_point = entity.dxf.start
                end_point = entity.dxf.end
                points = [Point(int(start_point[0] * 100), int(start_point[1] * 100)), 
                        Point(int(end_point[0] * 100), int(end_point[1] * 100))]
                item = Item(points)
                self.inputPoints.append(item)
            elif entity.dxftype() == 'SPLINE':
                control_points = entity.control_points
                for i in range(len(control_points) - 1):
                    start_point = control_points[i][:2]  # x, y coordinates of control points
                    end_point = control_points[i + 1][:2]
                    points = [Point(int(start_point[0] * 100), int(start_point[1] * 100)), 
                            Point(int(end_point[0] * 100), int(end_point[1] * 100))]
                    item = Item(points)
                    self.inputPoints.append(item)
                    
        return self.inputPoints

    