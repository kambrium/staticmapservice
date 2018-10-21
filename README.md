staticmapservice - A web service that generates static maps
===========================================================

About
-----
staticmapservice is a web service written in Python that generates static maps similar to the Maps Static API by Google. Essentially this software is a simple [Flask](http://flask.pocoo.org/) wrapper around the Python library [staticmap](https://github.com/komoot/staticmap). Please note that this software does not support all the features of staticmap, yet. At the moment, it can generate static maps based on [OpenStreetMaps](https://openstreetmap.org) tiles with one circle marker.

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
    http://127.0.0.1:5000/?w=400&h=300&z=7&mlat=48.2&mlon=11.2&msiz=12&mcol=%23CD0000
    ```
    As a response you should get a static map of southern Germany with a red marker next to the city of Munich. See below for a detailed list of currently supported query parameters.

Query parameters
----------------

This is a list of currently supported query parameters.

| Parameter | Meaning |
| --- | --- |
| w | Width of the map |
| h | Height of the map |
| z | Zoom level |
| mlat | Latitude of marker |
| mlon | Longitude of marker |
| msiz | Size of marker |
| mcol | Color of marker as Hex code (# encoded as %23) |

License
-------
MIT
