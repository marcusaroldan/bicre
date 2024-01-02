import json
from backend.directions import generateDirections
from backend.address import address_to_Place_ID
from backend.route_evaluation import evaluateRoute
from backend.constants import TRAVEL_MODE


# Overall route list which consists of integrated_steps:
overall_route = []
    
def display_integrated_steps(integrated_steps):
    integrated_steps_file = open('integrated_steps.txt', 'w')
    for step in integrated_steps:
        print('{}: {}, {}'.format(step.get('travel_mode'), 
              step.get('distance').get('text'),
              step.get('duration').get('text')))
        print('Start: ({}, {}), End: ({}, {})'.format( 
              step.get('start_location').get('lat'), step.get('start_location').get('lng'),
              step.get('end_location').get('lat'), step.get('end_location').get('lng')))
        print(step.get('html_instructions'))


def main():
    origin = str(input('Enter an origin: '))
    dest = str(input('Enter a destination: '))
    origin_pid = address_to_Place_ID(origin)
    dest_pid = address_to_Place_ID(dest)
    directions = generateDirections(origin_pid, dest_pid, TRAVEL_MODE.transit)
    evaluateRoute(directions[0], overall_route)
    
    display_integrated_steps(overall_route)

if __name__ == '__main__':
    main()