from backend.address import address_to_place_id
from backend.directions import generate_directions
from backend.constants import TRAVEL_MODE
from backend.route_evaluation import evaluate_route

# Top level function:
def execute_bicre(start_addr:str, end_addr:str) -> list:
    start_pid = address_to_place_id(start_addr)
    end_pid = address_to_place_id(end_addr)

    directions = generate_directions(start_pid, end_pid, TRAVEL_MODE.transit)

    generated_route = []
    evaluate_route(directions[0], generated_route)

    return generated_route

