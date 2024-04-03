import xml.etree.ElementTree as ET
from xml.dom import minidom
from svg.path import parse_path, Line, CubicBezier, QuadraticBezier, Arc
from pynest2d import *
import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext, layout, svg
import os
import uuid
import re


class Parser():
    def __init__(self, file_path):
        super().__init__()
        self.inputPoints = []
        self.file_label = file_path
        self.svg_to_mm = 0.352777778

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
            x = float(rect.getAttribute('x')) * self.svg_to_mm
            y = float(rect.getAttribute('y')) * self.svg_to_mm
            width = float(rect.getAttribute('width')) * self.svg_to_mm
            height = float(rect.getAttribute('height')) * self.svg_to_mm
            points = [Point(int(x * 100), int(y * 100)),
                    Point(int((x + width) * 100), int(y * 100)),
                    Point(int((x + width) * 100), int((y + height) * 100)),
                    Point(int(x * 100), int((y + height) * 100))]
            self.inputPoints.append(Item(points))

        for polygon_str in polygon_strings:
            poly_str = polygon_str.split()
            numbers = [float(num_str) for item in poly_str for num_str in item.split(',')]
            poly_str = numbers
            points = []
            for i in range(0, len(poly_str) - 1, 2):
                points.append(Point(int(float(poly_str[i]) * self.svg_to_mm * 100), int(float(poly_str[i + 1]) * self.svg_to_mm * 100)))
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
        self.svg_parse_points.append(Point(int(line.start.real * self.svg_to_mm * 100), int(line.start.imag * self.svg_to_mm * 100)))

    def points_on_cubic_bezier(self, bezier):
        for t in range(0, 101, 5):  # Sample 20 points on the curve
            point = bezier.point(t / 100)
            self.svg_parse_points.append(Point(int(point.real * self.svg_to_mm * self.svg_to_mm * 100), int(point.imag * self.svg_to_mm * 100)))

    def points_on_quadratic_bezier(self, bezier):
        for t in range(0, 101, 5):  # Sample 20 points on the curve
            point = bezier.point(t / 100)
            self.svg_parse_points.append(Point(int(point.real * self.svg_to_mm * 100), int(point.imag * self.svg_to_mm * 100)))

    def points_on_arc(self, arc):
        for t in range(0, 101, 5):  # Sample 20 points on the arc
            point = arc.point(t / 100)
            self.svg_parse_points.append(Point(int(point.real * self.svg_to_mm * 100), int(point.imag * self.svg_to_mm * 100)))




    
    def dxf_to_svg(self):
        doc = ezdxf.readfile(self.file_label)
        msp = doc.modelspace()
        backend = svg.SVGBackend()
        Frontend(RenderContext(doc), backend).draw_layout(msp)
        svg_str = backend.get_string(layout.Page(0, 0))

        scale = int(self.parse_svg_dimensions(svg_str))
        svg_str = self.remove_first_rect_and_ungroup(svg_str, scale)

        random_string = str(uuid.uuid4())[:8]
        output_directory = os.path.join(os.getcwd(), "converted_dxf")
        os.makedirs(output_directory, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(self.file_label))[0]
        output_svg_file = os.path.join(output_directory, f"{base_name}_{random_string}.svg")
        
        with open(output_svg_file, "wt", encoding="utf8") as fp:
            fp.write(svg_str)

        self.file_label = output_svg_file
        return output_svg_file
        # self.inputPoints = self.parse_svg()
        # return self.inputPoints

    def remove_namespace(self, tree):
        for elem in tree.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        return tree

    def remove_first_rect_and_ungroup(self, svg_string, scale):
        root = ET.fromstring(svg_string)

        first_rect = root.find('.//{http://www.w3.org/2000/svg}rect')
        if first_rect is not None:
            root.remove(first_rect)

        groups = root.findall('.//{http://www.w3.org/2000/svg}g')
        for group in groups:
            paths = group.findall('.//{http://www.w3.org/2000/svg}path')
            if paths:
                for path in paths:
                    d = path.get('d')
                    new_d = self.scale_path(d, scale)
                    path.set('d', new_d)
                    root.append(path)
                root.remove(group)
        root = self.remove_namespace(root)
        modified_svg_string = ET.tostring(root, encoding='utf-8').decode('utf-8')

        return modified_svg_string
    
    def scale_path(self, path_d, scale):
        parts = path_d.split()
        new_parts = []
        numbers = [item for item in parts if item.isdigit() or (item.startswith('-') and item[1:].isdigit())]
        for i in range(len(parts)):
            if parts[i].isdigit() or (parts[i].startswith('-') and parts[i][1:].isdigit()):
                new_parts.append(str(int(parts[i]) / scale))
            else:
                new_parts.append(str(parts[i]))
        return ' '.join(new_parts)

    def parse_svg_dimensions(self, svg_path):
        width_mm = None
        height_mm = None
        # Regular expressions to match width and height attributes
        width_mm_match = re.search(r'width="([\d.]+)mm"', svg_path)
        height_mm_match = re.search(r'height="([\d.]+)mm"', svg_path)
        viewbox_match = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg_path)

        if width_mm_match:
            width_mm = float(width_mm_match.group(1))
        if height_mm_match:
            height_mm = float(height_mm_match.group(1))
        if viewbox_match:
            viewbox_width = float(viewbox_match.group(1))
            viewbox_height = float(viewbox_match.group(2))
            if width_mm is not None:
                scaleW_px = viewbox_width / float(width_mm) * self.svg_to_mm  # Convert mm to px
            if height_mm is not None:
                scaleH_px = viewbox_height / float(height_mm) * self.svg_to_mm  # Convert mm to px\
            scale = (scaleH_px + scaleW_px) / 2

        return scale


    