from flask import Flask, request, render_template
from backend.bicre_api import execute_bicre
from flask_googlemaps import GoogleMaps, Map
import os

bicre = Flask(__name__)
bicre.config['GOOGLEMAPS_KEY'] = os.environ.get('GOOGLE_MAPS_KEY')
GoogleMaps(bicre)

# When the submit button is pressed, send a post to '/' that contains the start and end locations.
# Return a json array containing step objects (conversion from list of dict to json array of json objects 
# already handled by Flask)
@bicre.route('/', methods=['POST', 'GET'])
def retrieve_route():
    route_map = Map(
        identifier='view-side',
        lat=42.361145, 
        lng=-71.057083)
    if request.method == 'POST':
        start = request.form['start_addr']
        end = request.form['end_addr']
        directions = execute_bicre(start, end)
        return render_template('homepage.html', 
                            directions=directions, 
                            key=os.environ.get('GOOGLE_MAPS_KEY'), 
                            map=route_map)
    elif request.method == 'GET':
        return render_template('homepage.html', 
                            key=os.environ.get('GOOGLE_MAPS_KEY'), 
                            map=route_map)