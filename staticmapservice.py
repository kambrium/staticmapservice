from flask import Flask, request, send_file
from io import BytesIO
from staticmap import CircleMarker, Line, Polygon, StaticMap

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

    if ('markers' or 'lines' or 'polygons') in request.args:
        for marker in request.args.getlist('markers'):
            try:
                marker_properties = dict(item.split(':') for item in marker.split('|'))
                marker_lat = float(marker_properties['coords'].split(',')[0])
                marker_lon = float(marker_properties['coords'].split(',')[1])
                marker_color = marker_properties['color']
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
                polygon_outline_color = polygon_properties['ocolor']
                polygon_object = Polygon(polygon_coordinates, polygon_fill_color, polygon_outline_color)
                m.add_polygon(polygon_object)
            except:
                return 'Could not process polygons', 400
    else:
        return 'Could not find markers and/or lines and/or polygons', 400

    image = m.render(zoom=zoom)

    return serve_image(image)

def serve_image(image):
    image_io = BytesIO()
    image.save(image_io, format='PNG')
    image_io.seek(0)
    return send_file(image_io, mimetype='image/png')