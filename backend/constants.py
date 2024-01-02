import os
import googlemaps
from enum import Enum

# API Keys from Environment Variables
MBTA_KEY = os.environ.get('MBTA_KEY')
GOOGLE_KEY = os.environ.get('GOOGLE_MAPS_KEY')

# Travel Mode Enum for parsing JSON Responses
TRAVEL_MODE = Enum('travel_mode', ['driving', 'bicycling', 'transit', 'walking'])

# Client for calls to Google Maps APIs
GOOGLE_CLIENT = googlemaps.Client(key=GOOGLE_KEY)