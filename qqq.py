from svgpathtools import svg2paths
import re

# Define the conversion factor from SVG user units to mm
SVG_TO_MM = 0.352778  # 1 SVG user unit = 0.352778 mm


# SVG path data
svg_data = """
<svg width="177.6mm" height="88.7mm" viewBox="0 0 1000000 499437">
    <def>
        <style>.C1 {stroke: #ff0000; stroke-width: 2815; stroke-opacity: 1.000; fill: none;
            fill-opacity: 1.000;}</style>
        <style>.C2 {stroke: #000000; stroke-width: 1971; stroke-opacity: 1.000; fill: none;
            fill-opacity: 1.000;}</style>
    </def>
    <path d="M237748,102035 L65271,58330 L31798,177525 L186553,266921 L238204,102035" class="C1" />
    <path d="M585400,72236 L444353,115941 L357142,209906 L487661,194007 L585400,72236" class="C1" />
    <path d="M294014,386712 L0,424457 L103302,490014 L204618,455646 L294014,386712" class="C1" />
    <path d="M627516,347577 L572488,159050 L499984,499352 L602690,430404 L628516,262577" class="C1" />
    <path d="M954905,355722 L924510,446310 L827763,474917 L988080,489015 L955904,355722" class="C1" />
    <path d="M800944,219641 L642415,178916 L673803,338836 L834120,353934 L800944,219641" class="C1" />
    <path d="M877428,59323 L741943,150103 L882593,232546 L1000000,122291 L877428,59323" class="C1" />
    <path d="M305292,88080 C315762,103965 362271,94949 401729,78147 C418533,70248 466158,56403 462767,39369 C458604,21605 400352,8909 350011,78147 C319957,94304 309650,118565 351141,152213" class="C2" />
    <path d="M261366,332872 C271836,348757 512046,472215 538004,459014 C554808,450115 540518,214077 539326,80763 C535163,-961 395438,-7924 357397,13827 C327343,30084 320893,64268 375136,78595" class="C2" />
</svg>

"""
# Parse the SVG path data
paths, _ = svg2paths(svg_data)

# Iterate over each path
for path in paths:
    # Iterate over each segment in the path
    for segment in path:
        # Extract coordinates and convert to mm
        start_x, start_y = segment.start.real * SVG_TO_MM, segment.start.imag * SVG_TO_MM
        end_x, end_y = segment.end.real * SVG_TO_MM, segment.end.imag * SVG_TO_MM
        # Print or store the coordinates
        print(f"Start: ({start_x:.2f}mm, {start_y:.2f}mm), End: ({end_x:.2f}mm, {end_y:.2f}mm)")
