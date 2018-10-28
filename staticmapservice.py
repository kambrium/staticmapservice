from flask import Flask, request, send_file
from io import BytesIO
from staticmap import CircleMarker, Line, Polygon, StaticMap

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def create_map():
    try:
        width = int(request.args.get('w'))
        height = int(request.args.get('h'))
        zoom = int(request.args.get('z'))

        m = StaticMap(width, height, url_template=app.config['TILE_SERVER'])

        if 'markers' in request.args:
            for marker in request.args.getlist('markers'):
                marker_properties = dict(item.split(':') for item in marker.split('|'))
                marker_lat = float(marker_properties['coords'].split(',')[0])
                marker_lon = float(marker_properties['coords'].split(',')[1])
                marker_color = marker_properties['color']
                marker_diameter = int(marker_properties['diam'])
                marker_object = CircleMarker((marker_lon, marker_lat), marker_color, marker_diameter)
                m.add_marker(marker_object)

        if 'lines' in request.args:
            for line in request.args.getlist('lines'):
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

        if 'polygons' in request.args:
            for polygon in request.args.getlist('polygons'):
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

        image = m.render(zoom=zoom)

        return serve_image(image)

    except:
        return (app.config['INFO_TEXT'])

def serve_image(image):
    image_io = BytesIO()
    image.save(image_io, format='PNG')
    image_io.seek(0)
    return send_file(image_io, mimetype='image/png')