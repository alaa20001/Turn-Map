import osmnx as ox
import folium
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json

appmap = Flask(__name__)
CORS(appmap)

# تحميل الأماكن من ملف JSON
def load_famous_places():
    current_dir = os.path.dirname(__file__)
    filename = os.path.join(current_dir, 'famous_places.json')
    
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# تحميل الأماكن الشهيرة
famous_places = load_famous_places()

@appmap.route('/')
def home():
    current_location = request.args.get('current_location', default='32.8933, 13.2046').split(',')
    destination = request.args.get('destination', default='32.8997, 13.2160').split(',')
    
    current_coords = (float(current_location[0]), float(current_location[1]))
    destination_coords = (float(destination[0]), float(destination[1]))
    graph = ox.graph_from_point(current_coords, dist=10000, network_type='drive')
    orig = ox.nearest_nodes(graph, current_coords[1], current_coords[0])
    dest = ox.nearest_nodes(graph, destination_coords[1], destination_coords[0])

    route = ox.shortest_path(graph, orig, dest)
    route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]

    route_coords_json = json.dumps(route_coords)

    return render_template('apphtml.html', route_coords=route_coords_json)

@appmap.route('/places')
def get_places():
    return jsonify(famous_places)

# المسار لتقديم `favicon.ico`
@appmap.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(appmap.root_path),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    appmap.run(host='0.0.0.0',port=5000)