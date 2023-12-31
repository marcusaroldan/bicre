import os
import requests
import googlemaps
import json
from requests.auth import HTTPBasicAuth

# API Keys from Environment Variables
MBTA_KEY = os.environ.get('MBTA_KEY')
GOOGLE_KEY = os.environ.get('GOOGLE_MAPS_KEY')

gcode = googlemaps.Client(key=GOOGLE_KEY)

# address_to_Place_ID:
#   Given a human readable address, retrieve Place ID using Geocoding API
#   String (Address) --> Dict: String --> String (Formatted Address, Place ID)
def address_to_Place_ID(address):
    geocode_result = gcode.geocode(address=address)
    place_id = geocode_result[0].get('place_id')
    formatted_address = geocode_result[0].get('formatted_address')
    return {'formatted_address': formatted_address, 'place_id': place_id}

def main():
    address = '181 Becon Street Boston MA'
    print(address_to_Place_ID(address=address))

if __name__ == '__main__':
    main()