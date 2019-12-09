from flask import Flask
import folium


START_POSITION = [44.4, 39.75]


app = Flask(__name__)
map = folium.Map(location=START_POSITION, zoom_start=9)
folium.Marker(location=START_POSITION).add_to(map)


@app.route('/')
def hello():
        return map._repr_html_()


if __name__ == '__main__':
        app.run(debug=True)
