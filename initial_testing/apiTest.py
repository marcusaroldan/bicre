import requests
import json
import os
from requests.auth import HTTPBasicAuth


MBTA_KEY = os.environ.get('MBTA_KEY')
MBTA_URI = 'https://api-v3.mbta.com'
GOOGLE_MAPS_KEY = os.environ.get('GOOGLE_MAPS_KEY')
GOOGLE_MAPS_URI = 'https://maps.googleapis.com/maps/api/directions/json?'


mbta_headers = {'X-API-Key': MBTA_KEY}
google_headers = dict()
google_headers.update({'origin': '181+Beacon+Street+Boston+MA'})
google_headers.update({'destination': 'Northeastern+University+Boston+MA'})
google_headers.update({'mode': 'transit'})
google_headers.update({'key': GOOGLE_MAPS_KEY})

# response = requests.get(f'{uri}/facilities', headers=mbta_headers)
maps_response = requests.get(GOOGLE_MAPS_URI, params=google_headers)
# maps_request = maps_response.prepare()



# request_file = open('request.txt', 'w')
# request_file.write(maps_request.path_url)
# request_file.close()
maps_response_dict = dict(maps_response.json())
response_file = open("response.json", "w")
response_file.write(json.dumps(maps_response.json(), indent=2))
response_file.close()

json.dumps(maps_response.json(), indent=2)



# def get_route_segments():