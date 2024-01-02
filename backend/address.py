from backend.constants import GOOGLE_CLIENT

# address_to_Place_ID:
#   Given a human readable address, retrieve Place ID using Geocoding API
#   String (Address) --> String (Place ID)
def address_to_place_id(address:str) -> str:

    '''
    Given a human readable address, retrieve Place ID using Geocoding API
    :param address: string address of a location
    :rtype: string place_id from Geocoding API
    '''

    geocode_result = GOOGLE_CLIENT.geocode(address=address)
    place_id = 'place_id:' + geocode_result[0].get('place_id')
    return place_id