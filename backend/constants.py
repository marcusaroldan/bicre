import os
import googlemaps
from enum import Enum
from requests.auth import HTTPBasicAuth

# API Keys from Environment Variables
MBTA_KEY = os.environ.get('MBTA_KEY')
GOOGLE_KEY = os.environ.get('GOOGLE_MAPS_KEY')

# Travel Mode Enum for parsing JSON Responses
TRAVEL_MODE = Enum('travel_mode', ['driving', 'bicycling', 'transit', 'walking'])

# Client for calls to Google Maps APIs
GOOGLE_CLIENT = googlemaps.Client(key=GOOGLE_KEY)

# Bounds constant for more precise address lookup
northeast = '43.146489,-69.681923'
southwest = '41.2131168,-72.258425'
LOOKUP_BOUNDS = {'northeast': northeast, 'southwest': southwest}

# MBTA API Auth
MBTA_AUTH = HTTPBasicAuth('key', MBTA_KEY)