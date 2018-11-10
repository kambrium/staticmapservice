from flask import Flask, request, send_file
from io import BytesIO
from staticmap import CircleMarker, IconMarker, Line, Polygon, StaticMap
import re

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def create_map():
    try:
        width = int(request.args.get('w', default = app.config['DEFAULT_WIDTH']))
        if width > int(app.config['MAX_WIDTH']):
            return 'Width out of range', 400
    except:
        return 'Could not process width', 400
    
    try:
        height = int(request.args.get('h', default = app.config['DEFAULT_HEIGHT']))
        if height > int(app.config['MAX_HEIGHT']):
            return 'Height out of range', 400
    except:
        return 'Could not process height', 400

    try:
        zoom = int(request.args.get('z', default = app.config['DEFAULT_ZOOM']))
        if zoom > int(app.config['MAX_ZOOM']):
            return 'Zoom out of range', 400
    except:
        return 'Could not process zoom', 400

    m = StaticMap(width, height, url_template=app.config['TILE_SERVER'])

    if any(x in request.args for x in ('markers', 'lines', 'polygons', 'icons')):
        for marker in request.args.getlist('markers'):
            try:
                marker_properties = dict(item.split(':') for item in marker.split('|'))
                marker_lat = float(marker_properties['coords'].split(',')[0])
                marker_lon = float(marker_properties['coords'].split(',')[1])
                marker_color = marker_properties['color']
                check_hex_code(marker_color)
                marker_diameter = int(marker_properties['diam'])
                marker_object = CircleMarker((marker_lon, marker_lat), marker_color, marker_diameter)
                m.add_marker(marker_object)
            except:
                return 'Could not process markers', 400

        for line in request.args.getlist('lines'):
            try:
                line_properties = dict(item.split(':') for item in line.split('|'))
                line_coordinates = []
                for coord in line_properties['coords'].split(';'):
                    line_coordinate = []
                    line_coordinate.append(float(coord.split(',')[1]))
                    line_coordinate.append(float(coord.split(',')[0]))
                    line_coordinates.append(line_coordinate)
                line_color = line_properties['color']
                check_hex_code(line_color)
                line_width = int(line_properties['width'])
                line_object = Line(line_coordinates, line_color, line_width)
                m.add_line(line_object)
            except:
                return 'Could not process lines', 400

        for polygon in request.args.getlist('polygons'):
            try:
                polygon_properties = dict(item.split(':') for item in polygon.split('|'))
                polygon_coordinates = []
                for coord in polygon_properties['coords'].split(';'):
                    polygon_coordinate = []
                    polygon_coordinate.append(float(coord.split(',')[1]))
                    polygon_coordinate.append(float(coord.split(',')[0]))
                    polygon_coordinates.append(polygon_coordinate)
                polygon_fill_color = polygon_properties['fcolor']
                check_hex_code(polygon_fill_color)
                polygon_outline_color = polygon_properties['ocolor']
                check_hex_code(polygon_outline_color)
                polygon_object = Polygon(polygon_coordinates, polygon_fill_color, polygon_outline_color)
                m.add_polygon(polygon_object)
            except:
                return 'Could not process polygons', 400
    
        for icon in request.args.getlist('icons'):
            try:
                icon_properties = dict(item.split(':') for item in icon.split('|'))
                icon_lat = float(icon_properties['coords'].split(',')[0])
                icon_lon = float(icon_properties['coords'].split(',')[1])
                icon_name = icon_properties['name']
                icon_offset_x = int(icon_properties['offx'])
                icon_offset_y = int(icon_properties['offy'])
                icon_object = IconMarker((icon_lon, icon_lat), './icons/{0}.png'.format(icon_name), icon_offset_x, icon_offset_y)
                m.add_marker(icon_object)
            except:
                return 'Could not process icons', 400
    
    else:
        return 'Could not find markers and/or lines and/or polygons and/or icons', 400

    image = m.render(zoom=zoom)

    return serve_image(image)

def serve_image(image):
    image_io = BytesIO()
    image.save(image_io, format='PNG')
    image_io.seek(0)
    return send_file(image_io, mimetype='image/png')

def check_hex_code(color):
    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):                      
        pass
    else:
        raise