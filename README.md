staticmapservice - A web service that generates static maps
===========================================================

![staticmapservice logo](logo.png)

About
-----
staticmapservice is a web service written in Python that generates static maps similar to the Maps Static API by Google. Essentially this software is a [Flask](http://flask.pocoo.org/) wrapper around the Python library [staticmap](https://github.com/komoot/staticmap). At the moment, this software can generate static maps based on XYZ tiles (e.g. [OpenStreetMap based data](https://wiki.openstreetmap.org/wiki/Tile_servers)) with circle markers, lines, polygons and icons.

Quick start
-----------
1. Create a venv and activate it.
    ```
    python3 -m venv /path/to/venv/of/staticmapservice
    source /path/to/venv/of/staticmapservice/bin/activate
    ```
2. Clone staticmapservice and change to the application directory.
    ```
    git clone https://github.com/kambrium/staticmapservice
    cd staticmapservice
    ```
3. Install requirements.
    ```
    pip install -r requirements.txt
    ```
4. Export the FLASK_APP variable and run the software.
    ```
    export FLASK_APP=staticmapservice.py
    flask run
    ```
5. In your browser, send a request with some query parameters to the API. Here's an example that should work:
    ```
    http://127.0.0.1:5000/?w=400&h=300&z=9&markers=coords:48.25,11.22|diam:10|color:%233F33FF
    ```
    As a response you should get a static map of southern Bavaria with a blue marker next to the city of Munich. See below for a detailed list of currently supported query parameters.

Query parameters
----------------
This is a list of currently supported query parameters. Please see below for working example requests.

| Parameter | Meaning |
| --- | --- |
| w | Width of the map (in pixels) |
| h | Height of the map (in pixels) |
| z | Zoom level |
| markers | Properties of a circle marker separated by `\|`: coordinates (`coords`, one lat/lon pair), diameter (`diam`, in pixels) and color (`color`, hexadecimal code, # encoded as %23) |
| lines | Properties of a line separated by `\|`: coordinates (`coords`, two lat/lon pairs), width (`width`, in pixels) and color (`color`, hexadecimal code, # encoded as %23) |
| polygons | Properties of a polygon separated by `\|`: coordinates (`coords`, multiple lat/lon pairs), fill and outline color (`fcolor`, `ocolor`, hexadecimal codes, # encoded as %23) |
| icons | Properties of an icon marker separated by `\|`: coordinates (`coords`, one lat/lon pair), name of the icon (`name`, must be identical with the name of the icon file to be displayed, icons must be stored in the folder ./icons) and offset (`offx`, `offy`, in pixels) |

Examples
--------
Here are some examples how to use staticmapservice.

### Map with marker
The following request creates a 400 pixels wide and 300 pixels high map. The zoom level is 9. A marker is set at 48.25 (latitude) and 11.22 (longitude). The marker has a diameter of 10 pixels and the color #3F33FF (blue).
```
http://127.0.0.1:5000/?w=400&h=300&z=9&markers=coords:48.25,11.22|diam:10|color:%233F33FF
```

### Map with line
The following request creates a 500 pixels wide and 500 pixels high map. The zoom level is 8. A line will be drawn between a point at 48.2 (latitude), 11.2 (longitude) and another point at 47.5, 11. The line has a width of 4 pixels and the color #CD0000 (red).
```
http://127.0.0.1:5000/?w=500&h=500&z=8&lines=coords:48.2,11.2;47.5,11|width:4|color:%23CD0000
```

### Map with polygon
The following request creates a 400 pixels wide and 600 pixels high map. The zoom level is 5. A polygon will be drawn between the three points 48.2 (latitude), 11.2 (longitude), 47.5, 11 and 47.9, 12. The polygon is filled with the color #CD0000 (red) and its outline is #000000 (black).
```
http://127.0.0.1:5000/?w=400&h=600&z=5&polygons=coords:48.2,11.2;47.5,11;47.9,12;48.2,11.2\|fcolor:%23CD0000\|ocolor:%23000000
```

### Map with icon
The following request creates a 400 pixels wide and 300 pixels high map. The zoom level is 9. A flag icon is set at 48.25 (latitude) and 11.22 (longitude). The offset of the icon is 15 pixels to the right and 10 pixels upwards.
```
http://127.0.0.1:5000/?w=400&h=300&z=9&icons=coords:48.25,11.22|offx:15|offy:10|name:flag
```

### Using defaults
Some parameters get default values from the configuration file (see below). That's why this is a valid request:
```
http://127.0.0.1:5000/?markers=coords:48.25,11.22|diam:10|color:%233F33FF
```

### Multiple markers, lines, polygons and/or icons
The application can handle multiple markers, lines, polygons and/or icons per map. The following request creates a map with a marker and a line.
```
http://127.0.0.1:5000/?markers=coords:48.25,11.22|diam:10|color:%233F33FF&lines=coords:48.2,11.2;47.5,11|width:4|color:%23CD0000
```

Configuration
-------------
This application can be configured with the `config.py` file. Examples for configurable parameters are the maximum size of a map or the URL of the tile server. See the file `config.py` for a complete list of all configurable parameters.

License
-------
MIT