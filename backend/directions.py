from backend.constants import GOOGLE_CLIENT, TRAVEL_MODE

def test():
    print("Hello world")

# generateDirections:
#   Query DirectionsAPI to generate a route between the given origin and destination (both Place_IDs).
#   Mode is one of: 'transit', 'bicycling'
#   String (Place_ID, LatLng), String (Place_ID, LatLng) --> Dict (Route)
def generateDirections(origin:str, dest:str, mode:TRAVEL_MODE) -> list:
    '''
    Use DirectionsAPI to generate a set of routes from the given origin to destination using the specified travel mode.
    :param origin: origin location as a string place_id or latlng
    :param dest: destination location as a string place_id or latlng
    :param mode: travel mode for the route, Enum TRAVEL_MODE
    :rtype: list of routes
    '''

    directions_result = GOOGLE_CLIENT.directions(origin=origin, 
                                                 destination=dest,
                                                 mode=mode.name)
    # directions_headers = {'origin': origin,
    #                       'destination': dest,
    #                       'mode': mode.name,
    #                       'key': GOOGLE_KEY}
    # directions_result = requests.get('https://maps.googleapis.com/maps/api/directions/json?', params=directions_headers).json()
    # print(json.dumps(directions_result))
    return directions_result