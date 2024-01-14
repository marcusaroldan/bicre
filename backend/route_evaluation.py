from backend.constants import TRAVEL_MODE
from backend.directions import generate_directions
from backend.address import latlng_to_address
import requests
from backend.constants import MBTA_AUTH
import json
import datetime

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
                    if (is_transit_compatible_with_bikes(step)): overall_route.append(step)
                    else: evaluate_route(generate_new_cycling_route(step), overall_route)
                case TRAVEL_MODE.bicycling.name:
                    overall_route.append(step)
                case TRAVEL_MODE.walking.name:
                    evaluate_route(generate_new_cycling_route(step), overall_route)
                case _: raise(ValueError(mode))

# parseWalking:
#   Extract start and end locations from walking step.
#   Use extracted locations as origin and destination for new route, respectively.
#   Returns: generated route for extracted start and end locations via bicycling. 
def generate_new_cycling_route(step:dict) -> dict:

    '''
    Extract start and end locations from walking step.
    Use extracted locations as origin and destination for new route, respectively.

    :param step: step as a dictionary extracted from DirectionsAPI route response
    :rtype: generated route for extracted start and end locations via bicycling.
    '''

    origin = step.get('start_location')
    dest = step.get('end_location')
    return generate_directions(origin, dest, TRAVEL_MODE.bicycling)[0]

def is_transit_compatible_with_bikes(step:dict):

    '''
    :param step: transit step as a dict
    '''

    # origin_stop_latlng = step['transit_details']['departure_stop']['location']
    # dest_stop_latlng = step['transit_details']['arrival_stop']['location']
    # origin_stop_id = retrieve_stop_ID(origin_stop_latlng)
    # dest_stop_id = retrieve_stop_ID(dest_stop_latlng)

    #print(retrieve_stop_line_name(origin_stop_latlng))
    #print(retrieve_stop_line_name(dest_stop_latlng))

    return transit_step_allows_bike(step)


def retrieve_stop_ID(latlng:dict) -> str:
    
    '''
    Use the given lat and long values as a dict to determine the MBTA stop ID
    :param latlng: lattitude and longitude of stop as a dict
    :rtype: MBTA ID of the stop as a string
    '''

    # Request stop information filtered by lattitude and longitude
    url = 'https://api-v3.mbta.com/stops?filter[radius]=0.0025&filter[latitude]={}&filter[longitude]={}'
    latitude = latlng['lat']
    longitude = latlng['lng']
    stops_response = requests.get(url=url.format(latitude, longitude), auth=MBTA_AUTH).json()

    # Retrieve ID from response
    return stops_response['data'][0]['id']

def retrieve_stop_line_name(latlng:dict) -> str:
    # Request stop information filtered by lattitude and longitude
    url = 'https://api-v3.mbta.com/stops?filter[radius]=0.0025&filter[latitude]={}&filter[longitude]={}'
    latitude = latlng['lat']
    longitude = latlng['lng']
    stops_response = requests.get(url=url.format(latitude, longitude), auth=MBTA_AUTH).json()

    return stops_response['data'][0]['attributes']['vehicle_type']

def transit_step_allows_bike(step:dict) -> bool:

    '''
    Bikes are not allowed on Green Line, Mattapan Trolley, SL1, SL2, SL3
    Bikes are not allowed on any train during rush hour: (7-10AM), (4-7PM)
    Bikes are allowed on weekends
    Blueline Inbound: not allowed (7-9AM)
    Blueline Outbound: not allowed (4-6PM)
    '''
    

    # Route based on transit type:
    vehicle_type = step['transit_details']['line']['vehicle']['type']

    bikes_normally_allowed = None
    # Bikes not allowed on Green Line (Tram)
    match vehicle_type:
        case 'TRAM':
            bikes_normally_allowed = bikes_on_tram(step)
        case 'TROLLEYBUS': 
            bikes_normally_allowed = bikes_on_trolley(step)
        case 'SUBWAY' | 'HEAVY_RAIL':
            bikes_normally_allowed = bikes_on_subway(step)
        case 'FERRY':
            bikes_normally_allowed = bikes_on_ferry(step)
        case 'COMMUTER_TRAIN':
            bikes_normally_allowed = bikes_on_commuter_rail(step)
        case 'BUS':
            bikes_normally_allowed = bikes_on_bus(step)
        case _: 
            raise(ValueError(vehicle_type))

    url = 'https://api-v3.mbta.com/alerts?filter[stop]={}&filter[activity]=BRINGING_BIKE'
    allows_bike_response_api_response = requests.get(url=url.format(id), auth=MBTA_AUTH).json()
    no_alerts_from_mbta = len(allows_bike_response_api_response['data']) == 0

    return bikes_normally_allowed & no_alerts_from_mbta


def bikes_on_tram(step:dict):
    '''
    Bikes are not allowed on any Green Line Trams
    Will return false.
    '''
    return False

def bikes_on_trolley(step:dict):
    '''
    Bikes are not allowed on any trolleys such as the Mattapan Trolley.
    Will return false.
    '''
    return False

def bikes_on_ferry(step:dict):
    '''
    Bikes are always allowed on ferry service.
    Will return true.
    '''
    return True

def bikes_on_subway(step:dict):
    '''
    Orange and Red Lines allow bikes except during AM and PM Rush hour.
    Blue line allows bikes inbound except during AM Rush hour and outbound except during PM Rush hour.
    Determines the subway line and acts accordingly.
    '''

    line = step['transit_details']['line']['name']
    match line:
        case 'Red Line' | 'Orange Line':
            return bikes_on_orange_red_line(step)
        case 'Green Line':
            return bikes_on_tram(step)
        case 'Blue Line':
            return bikes_on_blue_line(step)

def bikes_on_commuter_rail(step:dict):
    # TODO: Bikes are allowed on certain lines at certain times according to timetable.
    return False

def bikes_on_bus(step:dict):
    # TODO: Bikes are allowed while there are bike racks available. Is this possible to determine?
    return True

def bikes_on_orange_red_line(step:dict):
    now = datetime.datetime.now()
    
    # Bikes allowed on weekends (Sat == 5, Sun == 6)
    if (now.weekday() >= 5):
        return True
    # Bikes are not allowed in AM or PM rush hours
    else: return not (is_between_hours(7,10) | is_between_hours(16,19))

def bikes_on_blue_line(step:dict):
    now = datetime.datetime.now()

    # Bikes allowed on weekends
    if (now.weekday() >= 5):
        return True
    # Bikes not allowed inbound between 7-9AM
    elif (step['transit_details']['headsign'] == 'Bowdoin'): 
        return not is_between_hours(7,9)
    # Bikes not allowed outbound between 4-6PM
    elif (step['transit_details']['headsign'] == 'Wonderland'):
        return not is_between_hours(16,18)

def is_between_hours(start:int, end:int) -> bool:
    '''
    Determines if the current time is between the given start and end hours, inclusively.
    :param start: beginning hour of period
    :param end: end hour of period
    :rtype: bool
    '''

    now = datetime.datetime.now()
    start_time = datetime.datetime.now().replace(hour=start, minute=0, second=0, microsecond=0)
    end_time = datetime.datetime.now().replace(hour=end, minute=0, second=0, microsecond=0)

    return now >= start_time & now <= end_time