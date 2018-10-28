from flask import Flask, request, send_file
from io import BytesIO
from staticmap import StaticMap, CircleMarker

app = Flask(__name__)

@app.route('/')
def create_map():
    try:
        width = int(request.args.get('w'))
        height = int(request.args.get('h'))
        zoom = int(request.args.get('z'))

        m = StaticMap(width, height, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')

        if 'markers' in request.args:
            for marker in request.args.getlist('markers'):
                marker_properties = dict(item.split(':') for item in marker.split('|'))
                marker_lat = float(marker_properties['coords'].split(',')[0])
                marker_lon = float(marker_properties['coords'].split(',')[1])
                marker_color = marker_properties['color']
                marker_size = int(marker_properties['size'])
                marker_object = CircleMarker((marker_lon, marker_lat), marker_color, marker_size)
                m.add_marker(marker_object)

        image = m.render(zoom=zoom)

        return serve_image(image)

    except:
        return ('Something went wrong during the creation of your map. Please check your query parameters. A working example is /?w=400&h=300&z=7&mlat=48.2&mlon=11.2&msiz=12&mcol=%23CD0000.')

def serve_image(image):
    image_io = BytesIO()
    image.save(image_io, format='PNG')
    image_io.seek(0)
    return send_file(image_io, mimetype='image/png')