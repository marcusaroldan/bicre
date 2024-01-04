from backend.constants import TRAVEL_MODE
from backend.directions import generate_directions
from backend.address import latlng_to_address
import requests
from backend.constants import MBTA_AUTH
import json

# evaluateRoute:
#   Recursively evaluate a generated route, examining each leg and its steps.
#   If steps only consist of transit or biking, add these steps to the overall integrated route.
#   If a step consists of walking, use the parseWalking function to generate a new cycling route,
#       then recursively evaluate this route.
#   If a step consists of driving, something went wrong here. :)
def evaluate_route(route:dict, overall_route:list) -> None:
    # Route has one or more legs
    #   Each leg has steps
    #       Each step has a transit mode:
    #           transit mode == TRANSIT --> add to overall list
    #           transit mode == WALKING --> create bike route for step
    #           transit mode == BIKING --> add to overall list

    '''
    Recursively evaluate a generated route, examining each leg and its steps.
    If a step is transit or biking, add the step to the provided overall route list.
    If a step is walking, use the parseWalking function to generate a new route for that walking step,
    and recursively evaluate this route.

    :param route: route as a dictionary from DirectionsAPI
    :param overall_route: list of all steps for integrated route, will only consist of walking or biking
    '''

    for leg in route.get('legs'):
        for step in leg.get('steps'):
            mode = str.lower(step.get('travel_mode'))
            match mode:
                case TRAVEL_MODE.transit.name:
                    parse_transit(step)
                    overall_route.append(step)
                case TRAVEL_MODE.bicycling.name:
                    overall_route.append(step)
                case TRAVEL_MODE.walking.name:
                    evaluate_route(parse_walking(step), overall_route)
                case _: raise(ValueError(mode))

# parseWalking:
#   Extract start and end locations from walking step.
#   Use extracted locations as origin and destination for new route, respectively.
#   Returns: generated route for extracted start and end locations via bicycling. 
def parse_walking(step:dict) -> dict:

    '''
    Extract start and end locations from walking step.
    Use extracted locations as origin and destination for new route, respectively.

    :param step: step as a dictionary extracted from DirectionsAPI route response
    :rtype: generated route for extracted start and end locations via bicycling.
    '''

    origin = step.get('start_location')
    dest = step.get('end_location')
    return generate_directions(origin, dest, TRAVEL_MODE.bicycling)[0]

def parse_transit(step:dict):

    '''
    :param step: transit step as a dict
    '''

    origin_stop_latlng = step['start_location']
    dest_stop_latlng = step['end_location']
    origin_stop_id = retrieve_stop_ID(origin_stop_latlng)
    origin_stop_id = retrieve_stop_ID(dest_stop_latlng)

def retrieve_stop_ID(latlng:dict) -> str:
    
    '''
    Use the given lat and long values as a dict to determine the MBTA stop ID
    :param latlng: lattitude and longitude of stop as a dict
    :rtype: MBTA ID of the stop as a string
    '''

    # Request stop information filtered by lattitude and longitude
    url = 'https://api-v3.mbta.com/stops?filter[radius]=0.005&filter[latitude]={}&filter[longitude]={}'
    latitude = latlng['lat']
    longitude = latlng['lng']
    stops_response = requests.get(url=url.format(latitude, longitude), auth=MBTA_AUTH).json()

    # Retrieve ID from response
    return stops_response['data'][0]['id']