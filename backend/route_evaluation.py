from backend.constants import TRAVEL_MODE
from backend.directions import generateDirections

# evaluateRoute:
#   Recursively evaluate a generated route, examining each leg and its steps.
#   If steps only consist of transit or biking, add these steps to the overall integrated route.
#   If a step consists of walking, use the parseWalking function to generate a new cycling route,
#       then recursively evaluate this route.
#   If a step consists of driving, something went wrong here. :)
def evaluateRoute(route:dict, overall_route:list) -> None:
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
                case TRAVEL_MODE.transit.name | TRAVEL_MODE.bicycling.name:
                    overall_route.append(step)
                case TRAVEL_MODE.walking.name:
                    evaluateRoute(parseWalking(step), overall_route)
                case _: raise(ValueError(mode))

# parseWalking:
#   Extract start and end locations from walking step.
#   Use extracted locations as origin and destination for new route, respectively.
#   Returns: generated route for extracted start and end locations via bicycling. 
def parseWalking(step:dict) -> dict:

    '''
    Extract start and end locations from walking step.
    Use extracted locations as origin and destination for new route, respectively.

    :param step: step as a dictionary extracted from DirectionsAPI route response
    :rtype: generated route for extracted start and end locations via bicycling.
    '''

    origin = step.get('start_location')
    dest = step.get('end_location')
    return generateDirections(origin, dest, TRAVEL_MODE.bicycling)[0]

# DEPRECATED:
# parseIntegratedStep:
#   Parse the provided step with TRAVEL_MODE BICYCLING or TRANSIT into an integrated_step
#   Step --> integrated_step
# def parseIntegratedStep(step=dict, travel_mode=TRAVEL_MODE):
#     integrated_step = dict()
#     integrated_step.update({'start_location': step.get('start_location')})
#     integrated_step.update({'end_location': step.get('end_location')})
#     integrated_step.update({'travel_mode': travel_mode.name})
#     integrated_step.update({'duration': step.get('duration')})
#     integrated_step.update({'distance': step.get('distance')})
#     integrated_step['instructions'] = step['html_instructions']
#     if travel_mode == TRAVEL_MODE.bicycling:
#         maneuver = step.get('maneuver')
#         if maneuver != None: integrated_step.update({'maneuver': maneuver})
#     elif travel_mode == TRAVEL_MODE.transit:
#         transit_details = step.get('transit_details')
#         if transit_details != None: integrated_step.update({'transit_details': transit_details})
#     return integrated_step