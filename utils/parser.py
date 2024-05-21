import xml.etree.ElementTree as ET
from xml.dom import minidom
from svg.path import parse_path, Path, Line, CubicBezier, QuadraticBezier, Arc, Close, Move
from pynest2d import *
import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext, layout, svg
import os
import uuid
import re
import numpy as np

import matplotlib.pyplot as plt


class Parser():
    def __init__(self, file_path):
        super().__init__()
        self.inputPoints = []
        self.svg_path_send = []
        self.svg_paths = file_path
        self.file_label = file_path
        self.svg_to_mm = 0.352777778

    def parse_svg(self):
        self.svg_points = []
        path_strings = []

        for path in self.svg_paths:
            occurrences = re.findall("path", path)
            if len(occurrences) > 1:
                path_strings.append(path)
            else:
                path_strings.append(self.extract_d_attribute(path))
            
        if not len(occurrences) > 1:
            path_strings = self.biggest_as_first(path_strings)

        for path_str in path_strings:

            occurrences = re.findall("path", path_str)
            if len(occurrences) > 1:
                splitted_svg_path = path_str.split("\n")
                splitted_path_strings = self.extract_multi_d_attribute(splitted_svg_path)
                self.svg_parse_points = []
                self.svg_path_send.append(" ".join(splitted_path_strings))
                for splitted_str in splitted_path_strings:
                    path = parse_path(splitted_str)
                    self.extract_points_from_path(path)
                item = Item(self.svg_parse_points)
                self.inputPoints.append(item)
            else:
                # path_str = self.scale_path(path_str, 2)
                path = parse_path(path_str)
                # vertices = path
                self.svg_parse_points = []
                self.svg_points = []
                self.extract_points_from_path(path)

                self.svg_path_send.append(path_str)
                self.svg_parse_points = []
                for vertex in self.svg_points:
                    self.svg_parse_points.append(Point(int(vertex[0]), int(vertex[1])))
                item = Item(self.svg_parse_points)
                self.inputPoints.append(item)

        return (self.inputPoints, self.svg_path_send)


    def extract_d_attribute(self, path_string):
        # Assuming the input path_string is in the format provided
        start_index = path_string.find('d="') + 3
        end_index = path_string.find('"', start_index)
        return path_string[start_index:end_index]
    
    def extract_multi_d_attribute(self, svg_paths):
        d_tags = []
        for path in svg_paths:
            match = re.search(r'd="(.*?)"', path)
            if match:
                d_tags.append(match.group(1))
        return d_tags

    
    def extract_points_from_path(self, path):
        i = 0
        for segment in path:
            # print(segment)
            if isinstance(segment, Line):
                self.points_on_line(segment)
            elif isinstance(segment, CubicBezier):
                self.points_on_cubic_bezier(segment)
            elif isinstance(segment, QuadraticBezier):
                self.points_on_quadratic_bezier(segment)
            elif isinstance(segment, Arc):
                self.points_on_arc(segment)
            elif isinstance(segment, Close):
                # print((int(segment.start.real * self.svg_to_mm * 100), int(segment.start.imag * self.svg_to_mm * 100)) == self.first)
                self.svg_parse_points.append(Point(self.first[0], self.first[1]))
                # self.svg_parse_points.append(Point(int(segment.start.real * self.svg_to_mm * 100), int(segment.start.imag * self.svg_to_mm * 100)))
                self.svg_points.append(self.first)
                # self.svg_points.append((int(segment.start.real * self.svg_to_mm * 100), int(segment.start.imag * self.svg_to_mm * 100)))
            elif isinstance(segment, Move):
                if i > 1:
                    break
                else:
                    self.first = (int(segment.start.real * self.svg_to_mm * 100), int(segment.start.imag * self.svg_to_mm * 100))

            i+=1

    def points_on_line(self, line):
        self.svg_parse_points.append(Point(int(line.start.real * self.svg_to_mm * 100), int(line.start.imag * self.svg_to_mm * 100)))
        # self.svg_parse_points.append(Point(int(line.end.real * self.svg_to_mm * 100), int(line.end.imag * self.svg_to_mm * 100)))
        self.svg_points.append((int(line.start.real * self.svg_to_mm * 100), int(line.start.imag * self.svg_to_mm * 100)))

    def points_on_cubic_bezier(self, bezier):
        for t in range(0, 101, 5):  # Sample 20 points on the curve
            point = bezier.point(t / 100)
            # print(point)
            self.svg_parse_points.append(Point(int(point.real * self.svg_to_mm * 100), int(point.imag * self.svg_to_mm * 100)))
            self.svg_points.append((int(point.real * self.svg_to_mm * 100), int(point.imag * self.svg_to_mm * 100)))

    def points_on_quadratic_bezier(self, bezier):
        for t in range(0, 101, 5):  # Sample 20 points on the curve
            point = bezier.point(t / 100)
            self.svg_parse_points.append(Point(int(point.real * self.svg_to_mm * 100), int(point.imag * self.svg_to_mm * 100)))

    def points_on_arc(self, arc):
        for t in range(0, 101, 5):  # Sample 20 points on the arc
            point = arc.point(t / 100)
            self.svg_parse_points.append(Point(int(point.real * self.svg_to_mm * 100), int(point.imag * self.svg_to_mm * 100)))



    def ungroup_and_apply_transform(self, svg_string, scale):
            root = ET.fromstring(svg_string)

            # Find all groups in the SVG
            groups = root.findall('.//{http://www.w3.org/2000/svg}g')

            for group in groups:
                # Retrieve group transformation attributes
                transform_attr = group.get('transform')
                if transform_attr:
                    # Apply group transformation to all child elements
                    for child in group:
                        child_transform = child.get('transform')
                        if child_transform:
                            # Combine group transformation with child transformation
                            combined_transform = transform_attr + ' ' + child_transform
                            child.set('transform', combined_transform)
                        else:
                            child.set('transform', transform_attr)

                    # Remove the group element
                    group.getparent().remove(group)

            # Scale all paths in the SVG
            paths = root.findall('.//{http://www.w3.org/2000/svg}path')
            for path in paths:
                d = path.get('d')
                new_d = self.scale_path(d, scale)
                path.set('d', new_d)

            root = self.remove_namespace(root)
            modified_svg_string = ET.tostring(root, encoding='utf-8').decode('utf-8')

            return modified_svg_string


    
    def dxf_to_svg(self):
        doc = ezdxf.readfile(self.file_label)
        msp = doc.modelspace()
        backend = svg.SVGBackend()
        Frontend(RenderContext(doc), backend).draw_layout(msp)
        svg_str = backend.get_string(layout.Page(0, 0))

        scale = int(self.parse_svg_dimensions(svg_str))
        svg_str = self.remove_first_rect_and_ungroup(svg_str, scale)
        svg_str = self.remove_c1_paths(svg_str)

        root = ET.fromstring(svg_str)
        index = 0
        for styles in root.findall('def'):
            for style in styles.findall('style'):
                index += 1
            if index > 1:
                paths = root.findall('path')
                trans_paths = []
                for path in paths:
                    trans_path = self.biggest_as_outer(path.attrib['d'])
                    trans_paths.append('<path d="' + trans_path + '" class="' + path.attrib['class'] + '" />')
                
                svg_header_match = re.match(r'(<svg.*?<def>.*?</def>)', svg_str, re.DOTALL)
                svg_header = svg_header_match.group(1) if svg_header_match else ''  
                svg_footer = '</svg>'

                svg_str = ''.join(svg_header)
                svg_str += ''.join(trans_paths)
                svg_str += ''.join(svg_footer)


        # svg_str = self.biggest_as_outer(svg_str)

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

    def remove_c1_paths(self, svg_str):
        root = ET.fromstring(svg_str)

        index = 0
        for styles in root.findall('def'):
            for style in styles.findall('style'):
                index += 1

        if index > 1:
            for path in root.findall('path'):
                if 'class' in path.attrib and path.attrib['class'] == 'C1':
                    root.remove(path)

        return ET.tostring(root, encoding='utf-8').decode('utf-8')

    def remove_namespace(self, tree):
        for elem in tree.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        return tree
    

    def biggest_as_first(self, svg_string):
        # root = ET.fromstring(svg_string)
        # paths = root.findall('path')
        parsed_segments = [(path, parse_path(path), self.calculate_bounding_box(parse_path(path))) for path in svg_string]
        sorted_segments = sorted(parsed_segments, key=lambda x: self.calculate_area(x[2]), reverse=True)

        sorted_paths = []
        for seg in sorted_segments:
            sorted_paths.append(seg[0])

        return sorted_paths

    def biggest_as_outer(self, svg_string):
        path_segment_pattern = re.compile(r'(M[^MZ]+Z)')
        path_segments = path_segment_pattern.findall(svg_string)
        parsed_segments = [(segment, parse_path(segment), self.calculate_bounding_box(parse_path(segment))) for segment in path_segments]
        sorted_segments = sorted(parsed_segments, key=lambda x: self.calculate_area(x[2]), reverse=True)
        sorted_path_data = ' '.join([seg[0] for seg in sorted_segments])
        return sorted_path_data


    def calculate_bounding_box(self, path):
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for segment in path:
            if isinstance(segment, (Line, CubicBezier, QuadraticBezier, Arc)):
                points = [segment.start, segment.end]
                if hasattr(segment, 'control1'):
                    points.append(segment.control1)
                if hasattr(segment, 'control2'):
                    points.append(segment.control2)
                for point in points:
                    min_x = min(min_x, point.real)
                    min_y = min(min_y, point.imag)
                    max_x = max(max_x, point.real)
                    max_y = max(max_y, point.imag)
        
        return (min_x, min_y, max_x, max_y)


    def calculate_area(self, bbox):
        min_x, min_y, max_x, max_y = bbox
        return (max_x - min_x) * (max_y - min_y)
        
    

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


    