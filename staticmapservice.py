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

    static_map = StaticMap(width, height, url_template=app.config['TILE_SERVER'])

    if any(x in request.args for x in ('marker', 'line', 'polygon', 'icon')):
        for m in request.args.getlist('marker'):
            try:
                marker = process_marker(m)
                static_map.add_marker(marker)
            except:
                return 'Could not process marker', 400

        for l in request.args.getlist('line'):
            try:
                segments = process_line(l)
                for s in segments:
                    static_map.add_line(s)
            except:
                return 'Could not process line', 400

        for p in request.args.getlist('polygon'):
            try:
                polygon = process_polygon(p)
                static_map.add_polygon(polygon)
            except:
                return 'Could not process polygon', 400
    
        for i in request.args.getlist('icon'):
            try:
                icon = process_icon(i)
                static_map.add_marker(icon)
            except:
                return 'Could not process icon', 400
    else:
        return 'Could not find markers and/or lines and/or polygons and/or icons', 400

    image = static_map.render(zoom=zoom)

    return serve_image(image)

def process_marker(m):
    m_properties = dict(item.split(':') for item in m.split('|'))
    
    m_color = m_properties['color']
    check_hex_code(m_color)
    m_diameter = int(m_properties['diam'])

    m_lat = float(m_properties['coords'].split(',')[0])
    m_lon = float(m_properties['coords'].split(',')[1])

    return CircleMarker((m_lon, m_lat), m_color, m_diameter)

def process_line(l):
    l_properties = dict(item.split(':') for item in l.split('|'))

    l_coords = l_properties['coords'].split(';')
    assert len(l_coords) > 1

    l_color = l_properties['color']
    check_hex_code(l_color)
    l_width = int(l_properties['width'])

    l_segments = []
    s_coordinates = []
    i = 0

    for coord in l_coords:
        s_coordinate = []
        s_coordinate.append(float(coord.split(',')[1]))
        s_coordinate.append(float(coord.split(',')[0]))

        if i == 0:
            s_coordinates.append(s_coordinate)
        elif i == 1:
            s_coordinates.append(s_coordinate)
            coord_for_next_loop = s_coordinate
        else:
            s_coordinates.append(coord_for_next_loop)
            s_coordinates.append(s_coordinate)
            coord_for_next_loop = s_coordinate

        if len(s_coordinates) % 2 == 0:
            l_segment = Line(s_coordinates, l_color, l_width)
            l_segments.append(l_segment)
            s_coordinates = []

        i += 1

    return l_segments

def process_polygon(p):
    p_properties = dict(item.split(':') for item in p.split('|'))
    
    p_fill_color = p_properties['fcolor']
    check_hex_code(p_fill_color)
    p_outline_color = p_properties['ocolor']
    check_hex_code(p_outline_color)

    p_coordinates = []

    for coord in p_properties['coords'].split(';'):
        p_coordinate = []
        p_coordinate.append(float(coord.split(',')[1]))
        p_coordinate.append(float(coord.split(',')[0]))
        p_coordinates.append(p_coordinate)
    
    return Polygon(p_coordinates, p_fill_color, p_outline_color)

def process_icon(i):
    i_properties = dict(item.split(':') for item in i.split('|'))
    
    i_name = i_properties['name']
    i_offset_x = int(i_properties['offx'])
    i_offset_y = int(i_properties['offy'])

    i_lat = float(i_properties['coords'].split(',')[0])
    i_lon = float(i_properties['coords'].split(',')[1])

    return IconMarker((i_lon, i_lat), './icons/{0}.png'.format(i_name), i_offset_x, i_offset_y)

def serve_image(image):
    image_io = BytesIO()
    image.save(image_io, format='PNG')
    image_io.seek(0)
    
    return send_file(image_io, mimetype='image/png')

def check_hex_code(color):
    assert re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)