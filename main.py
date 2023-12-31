import os
import requests
import googlemaps
import json
from requests.auth import HTTPBasicAuth
from enum import Enum

# API Keys from Environment Variables
MBTA_KEY = os.environ.get('MBTA_KEY')
GOOGLE_KEY = os.environ.get('GOOGLE_MAPS_KEY')

# Travel Mode Enum for parsing JSON Responses
TRAVEL_MODE = Enum('travel_mode', ['driving', 'bicycling', 'transit', 'walking'])

# Client for calls to Google Maps APIs
google_client = googlemaps.Client(key=GOOGLE_KEY)

# Overall route list which consists of integrated_steps:
#   integrated_steps are dicts with the following fields:
#       - start_location (LatLongLiteral)
#       - end_location (LatLongLiteral)
#       - travel_mode (TRAVEL_MODE: one of TRANSIT or BICYCLING)
#       - duration  (TextValueObject)
#       - distance (TextValueObject)
#       - instructions (String)
#       - [OPTIONAL] transit_details (DirectionsTransitDetails)
#       - [OPTIONAL] maneuver (String)
overall_route = []

# address_to_Place_ID:
#   Given a human readable address, retrieve Place ID using Geocoding API
#   String (Address) --> String (Place ID)
def address_to_Place_ID(address):
    geocode_result = google_client.geocode(address=address)
    place_id = 'place_id:' + geocode_result[0].get('place_id')
    return place_id

# generateDirections:
#   Query DirectionsAPI to generate a route between the given origin and destination (both Place_IDs).
#   Mode is one of: 'transit', 'bicycling'
#   Place_ID, Place_ID --> Dict (Route)
def generateDirections(origin, dest, mode=TRAVEL_MODE):
    directions_result = google_client.directions(origin=origin, 
                                                 destination=dest,
                                                 mode=mode.name)
    # directions_headers = {'origin': origin,
    #                       'destination': dest,
    #                       'mode': mode.name,
    #                       'key': GOOGLE_KEY}
    # directions_result = requests.get('https://maps.googleapis.com/maps/api/directions/json?', params=directions_headers).json()
    # print(json.dumps(directions_result))
    return directions_result[0]

# evaluateRoute:
#   Recursively evaluate a generated route, examining each leg and its steps.
#   If steps only consist of transit or biking, add these steps to the overall integrated route using
#       the parseTransit or parseBicycling functions respectively.
#   If a step consists of walking, use the parseWalking function to generate a new cycling route,
#       then recursively evaluate this route.
#   If a step consists of driving, something went wrong here. :)
def evaluateRoute(route):
    # Route has one or more legs
    #   Each leg has steps
    #       Each step has a transit mode:
    #           transit mode == TRANSIT --> add to overall list
    #           transit mode == WALKING --> create bike route for step
    #           transit mode == BIKING --> add to overall list

    for leg in route.get('legs'):
        for step in leg.get('steps'):
            mode = str.lower(step.get('travel_mode'))
            if mode == TRAVEL_MODE.transit.name:
                overall_route.append(parseIntegratedStep(step, TRAVEL_MODE.transit))
            elif mode == TRAVEL_MODE.walking.name:
                evaluateRoute(parseWalking(step))
            elif mode == TRAVEL_MODE.bicycling.name:
                overall_route.append(parseIntegratedStep(step, TRAVEL_MODE.bicycling))
            else: raise(ValueError(mode))

# parseIntegratedStep:
#   Parse the provided step with TRAVEL_MODE BICYCLING or TRANSIT into an integrated_step
#   Step --> integrated_step
def parseIntegratedStep(step=dict, travel_mode=TRAVEL_MODE):
    integrated_step = dict()
    integrated_step.update({'start_location': step.get('start_location')})
    integrated_step.update({'end_location': step.get('end_location')})
    integrated_step.update({'travel_mode': travel_mode.name})
    integrated_step.update({'duration': step.get('duration')})
    integrated_step.update({'distance': step.get('distance')})
    integrated_step['instructions'] = step['html_instructions']
    if travel_mode == TRAVEL_MODE.bicycling:
        maneuver = step.get('maneuver')
        if maneuver != None: integrated_step.update({'maneuver': maneuver})
    elif travel_mode == TRAVEL_MODE.transit:
        transit_details = step.get('transit_details')
        if transit_details != None: integrated_step.update({'transit_details': transit_details})
    
    return integrated_step

# parseWalking:
#   Extract start and end locations from walking step.
#   Use extracted locations as origin and destination for new route, respectively.
#   Returns: generated route for extracted start and end locations via bicycling. 
def parseWalking(step=dict):
    origin = step.get('start_location')
    dest = step.get('end_location')
    return generateDirections(origin, dest, TRAVEL_MODE.bicycling)
    
def display_integrated_steps(integrated_steps):
    integrated_steps_file = open('integrated_steps.txt', 'w')
    for step in integrated_steps:
        print('{}: {}, {}'.format(step.get('travel_mode'), 
              step.get('distance').get('text'),
              step.get('duration').get('text')))
        print('Start: ({}, {}), End: ({}, {})'.format( 
              step.get('start_location').get('lat'), step.get('start_location').get('lng'),
              step.get('end_location').get('lat'), step.get('end_location').get('lng')))
        print(step.get('instructions'))


def main():
    origin = '217 10th street Hoboken NJ'
    dest = 'Penn Station NY'
    origin_pid = address_to_Place_ID(origin)
    dest_pid = address_to_Place_ID(dest)
    directions = generateDirections(origin_pid, dest_pid, TRAVEL_MODE.transit)
    evaluateRoute(directions)
    # directions_result_file = open('directions_result_file.txt', 'w')
    # directions_result_file.write(json.dumps(directions))
    # directions_result_file.close
    
    display_integrated_steps(overall_route)

if __name__ == '__main__':
    main()