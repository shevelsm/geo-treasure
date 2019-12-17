import json
import os

import folium
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from webapp.model import Point


app = Flask(__name__)
app.config.from_pyfile("config.py")
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


# in future it will be algorithm
def markers_generator(range=10):
    """ range - searching radius for places """
    with open(os.path.join('data', 'ready50dots.json'), 'r', 
                                                    encoding='utf-8') as file:
        markers_data = json.loads(file.read())
    return markers_data


@app.route('/')
def index():
    # in future get start_position as argument
    start_position = [44.4, 39.75]
    folium_map = folium.Map(location=start_position, zoom_start=9)
    for marker in markers_generator():
        folium.Marker([marker['y'], marker['x']], popup=marker['description'],
                        tooltip='Click for more').add_to(folium_map)
    return render_template('index.html', folium_map=folium_map._repr_html_())


if __name__ == '__main__':
    app.run(debug=True)
