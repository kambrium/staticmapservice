from flask import Flask, request, send_file
from io import BytesIO
from staticmap import CircleMarker, IconMarker, Line, Polygon, StaticMap
import re

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def create_map():
    """Main method where map is put together"""

    # Holds the amount of points (p), nodes (n) and vertices (v) at the present time
    pnv = 0

    # General properties of the map: width, height and zoom level
    try:
        width = int(request.args.get('w', default=app.config['DEFAULT_WIDTH']))
        if width > int(app.config['MAX_WIDTH']):
            return 'Width out of range', 400
    except:
        return 'Could not process width', 400

    try:
        height = int(
            request.args.get('h', default=app.config['DEFAULT_HEIGHT']))
        if height > int(app.config['MAX_HEIGHT']):
            return 'Height out of range', 400
    except:
        return 'Could not process height', 400

    try:
        zoom = int(request.args.get('z', default=app.config['DEFAULT_ZOOM']))
        if zoom > int(app.config['MAX_ZOOM']):
            return 'Zoom out of range', 400
    except:
        return 'Could not process zoom', 400

    center = None
    center_lon = request.args.get("center_lon", default=None)
    center_lat = request.args.get("center_lat", default=None)

    if center_lat and center_lon:
        center = (center_lon, center_lat)

    # Create static map object
    static_map = StaticMap(width, height,
                           url_template=app.config['TILE_SERVER'],
                           reverse_y=app.config['IS_TMS'])

    # Add polygons, polylines, markers and icons to the map
    if any(x in request.args for x in ('marker', 'line', 'polygon', 'icon')):
        for p in request.args.getlist('polygon'):
            try:
                polygon, updated_pnv = process_polygon(p, pnv)
                pnv = updated_pnv
                static_map.add_polygon(polygon)
            except PnvError:
                return 'Exceeded maximum amount of points, nodes and vertices', 400
            except:
                return 'Could not process polygon', 400

        for l in request.args.getlist('line'):
            try:
                segments, updated_pnv = process_line(l, pnv)
                pnv = updated_pnv
                # Special case polylines: Add each segment of polyline to map
                for s in segments:
                    static_map.add_line(s)
            except PnvError:
                return 'Exceeded maximum amount of points, nodes and vertices', 400
            except:
                return 'Could not process line', 400

        for i in request.args.getlist('icon'):
            try:
                icon, updated_pnv = process_icon(i, pnv)
                pnv = updated_pnv
                static_map.add_marker(icon)
            except PnvError:
                return 'Exceeded maximum amount of points, nodes and vertices', 400
            except:
                return 'Could not process icon', 400

        for m in request.args.getlist('marker'):
            try:
                marker, updated_pnv = process_marker(m, pnv)
                pnv = updated_pnv
                static_map.add_marker(marker)
            except PnvError:
                return 'Exceeded maximum amount of points, nodes and vertices', 400
            except:
                return 'Could not process marker', 400
    else:
        return 'Could not find markers and/or lines and/or polygons and/or icons', 400

    # Render the map
    image = static_map.render(zoom=zoom, center=center)
    return serve_image(image)


def process_marker(m, pnv):
    """Creates a CircleMarker object with the properties from the request"""

    m_properties = dict(item.split(':') for item in m.split('|'))

    m_color = m_properties['color']
    check_hex_code(m_color)
    m_diameter = int(m_properties['diam'])

    m_lat = float(m_properties['coords'].split(',')[0])
    m_lon = float(m_properties['coords'].split(',')[1])

    pnv = pnv_counter(pnv)

    return CircleMarker((m_lon, m_lat), m_color, m_diameter), pnv


def process_line(l, pnv):
    """Creates a list of Line objects with the properties from the request"""

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
        pnv = pnv_counter(pnv)
        s_coordinate = []
        s_coordinate.append(float(coord.split(',')[1]))
        s_coordinate.append(float(coord.split(',')[0]))

        # Polyline handling
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

    return l_segments, pnv


def process_polygon(p, pnv):
    """Creates a Polygon object with the properties from the request"""

    p_properties = dict(item.split(':') for item in p.split('|'))

    p_fill_color = p_properties['fcolor']
    check_hex_code(p_fill_color)
    p_outline_color = p_properties['ocolor']
    check_hex_code(p_outline_color)

    p_coordinates = []

    for coord in p_properties['coords'].split(';'):
        pnv = pnv_counter(pnv)
        p_coordinate = []
        p_coordinate.append(float(coord.split(',')[1]))
        p_coordinate.append(float(coord.split(',')[0]))
        p_coordinates.append(p_coordinate)

    return Polygon(p_coordinates, p_fill_color, p_outline_color), pnv


def process_icon(i, pnv):
    """Creates an IconMarker object with the properties from the request"""

    i_properties = dict(item.split(':') for item in i.split('|'))

    i_name = i_properties['name']
    i_offset_x = int(i_properties['offx'])
    i_offset_y = int(i_properties['offy'])

    i_lat = float(i_properties['coords'].split(',')[0])
    i_lon = float(i_properties['coords'].split(',')[1])

    pnv = pnv_counter(pnv)

    return IconMarker((i_lon, i_lat), './icons/{0}.png'.format(i_name),
                      i_offset_x, i_offset_y), pnv


def serve_image(image):
    """Saves map in a stream and serves it"""

    image_io = BytesIO()
    image.save(image_io, format='PNG')
    image_io.seek(0)

    return send_file(image_io, mimetype='image/png')


def check_hex_code(color):
    """Checks if the given string is a hex color code"""

    assert re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)


def pnv_counter(pnv):
    """Checks if the amount of points, nodes and vertices in the request is below the maximum value"""

    pnv += 1
    if pnv <= int(app.config['MAX_PNV']):
        return pnv
    else:
        raise PnvError


class PnvError(Exception):
    """Raised when the amount of points, nodes and vertices in the request is higher than the max value"""

    pass
