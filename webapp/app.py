from flask import Flask
import folium
import json
import os


app = Flask(__name__)


# in future it will be algorithm
def markers_generator(range=10):
    """ range - searching radius for places """
    with open(os.path.join('data', 'ready50dots.json'), 'r', encoding='utf-8') as file:
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
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)