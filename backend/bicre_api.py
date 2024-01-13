from backend.address import address_to_place_id
from backend.directions import generate_directions
from backend.constants import TRAVEL_MODE
from backend.route_evaluation import evaluate_route

# Top level function:
def execute_bicre(start_addr:str, end_addr:str) -> list:
    '''
    Takes in two addresses to search for as a start and end point to the integrated route.
    Returns a list of steps needed to get from the start address to the end address through cycling and transit.

    :param start_addr: start address of the desired route
    :param end_addr: end address of the desired route
    :rtype list: list of dicts where each dict is a step containing information about that step in the route
    '''
    start_pid = address_to_place_id(start_addr)
    end_pid = address_to_place_id(end_addr)

    directions = generate_directions(start_pid, end_pid, TRAVEL_MODE.transit)

    generated_route = []
    evaluate_route(directions[0], generated_route)

    return generated_route

