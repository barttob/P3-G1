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
        rect_strings = [rect for rect in doc.getElementsByTagName('rect')]
        polygon_strings = [polygon.getAttribute('points') for polygon in doc.getElementsByTagName('polygon')]


        for path_str in path_strings:
            path = parse_path(path_str)
            self.svg_parse_points = []
            self.extract_points_from_path(path)
            item = Item(self.svg_parse_points)
            self.inputPoints.append(item)

        for rect in rect_strings:
            x = float(rect.getAttribute('x'))
            y = float(rect.getAttribute('y'))
            width = float(rect.getAttribute('width'))
            height = float(rect.getAttribute('height'))
            points = [Point(int(x * 100), int(y * 100)),
                    Point(int((x + width) * 100), int(y * 100)),
                    Point(int((x + width) * 100), int((y + height) * 100)),
                    Point(int(x * 100), int((y + height) * 100))]
            self.inputPoints.append(Item(points))

        for polygon_str in polygon_strings:
            poly_str = polygon_str.split()
            points = []
            for i in range(0, len(poly_str) - 2, 2):
                points.append(Point(int(float(poly_str[i]) * 100), int(float(poly_str[i + 1]) * 100)))
            self.inputPoints.append(Item(points))

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
            points = []
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
                    points.append(Point(int(start_point[0] * 100), int(start_point[1] * 100)))
                item = Item(points)
                self.inputPoints.append(item)
            elif entity.dxftype() == 'LWPOLYLINE':
                for vertex in entity.vertices:
                    points.append(Point(int(vertex.dxf.location[0] * 100), int(vertex.dxf.location[1] * 100)))
                item = Item(points)
                self.inputPoints.append(item)
            elif entity.dxftype() == 'CIRCLE':
                center = entity.dxf.center
                radius = entity.dxf.radius
                num_segments = 36
                for i in range(num_segments):
                    angle = i * (2 * math.pi / num_segments)
                    x = center[0] + radius * math.cos(angle)
                    y = center[1] + radius * math.sin(angle)
                    points.append(Point(int(x * 100), int(y * 100)))
                item = Item(points)
                self.inputPoints.append(item)
                        
        return self.inputPoints

    