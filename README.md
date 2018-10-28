staticmapservice - A web service that generates static maps
===========================================================

About
-----
staticmapservice is a web service written in Python that generates static maps similar to the Maps Static API by Google. Essentially this software is a [Flask](http://flask.pocoo.org/) wrapper around the Python library [staticmap](https://github.com/komoot/staticmap). Please note that this software does not support all the features of staticmap, yet. At the moment, it can generate static maps based on XYZ tiles (e.g. [OpenStreetMap based data](https://wiki.openstreetmap.org/wiki/Tile_servers)) with circle markers, lines and polygons.

Usage
-----
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

This is a list of currently supported query parameters.

| Parameter | Meaning | Example |
| --- | --- | --- |
| w | Width of the map in pixels | w=400 |
| h | Height of the map in pixels | h=300 |
| z | Zoom level | z=10 |
| markers | Coordinates (a lat/lon pair), diameter (in pixels) and color (hexadecimal code, # encoded as %23) of a circle marker | markers=coords:48.25,11.22\|diam:10\|color:%233F33FF |
| lines | Coordinates (two lat/lon pairs), width (in pixels) and color (hexadecimal code, # encoded as %23) of a line | lines=coords:48.2,11.2;47.5,11\|width:4\|color:%23CD0000 |
| polygons | Coordinates (multiple lat/lon pairs), fill and outline color (hexadecimal codes, # encoded as %23) of a polygon | polygons=coords:48.2,11.2;47.5,11;47.9,12;48.2,11.2\|fcolor:%23CD0000\|ocolor:%23000000 |

License
-------
MIT