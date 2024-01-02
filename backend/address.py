from backend.constants import GOOGLE_CLIENT, LOOKUP_BOUNDS

# address_to_Place_ID:
#   Given a human readable address, retrieve Place ID using Geocoding API
#   String (Address) --> String (Place ID)
def address_to_place_id(address:str) -> str:

    '''
    Given a human readable address, retrieve Place ID using Geocoding API
    :param address: string address of a location
    :rtype: string place_id from Geocoding API
    '''

    geocode_result = GOOGLE_CLIENT.geocode(address=address, bounds=LOOKUP_BOUNDS)
    place_id = 'place_id:' + geocode_result[0].get('place_id')
    return place_id

def latlng_to_address(latlng:dict) -> str:

    '''
    Convert lattitude and longitude (latlng) coordinates to human readable address
    using Geocoding API.
    :param latlng: dict encoding of lat, long coordinates
    :rtype: address as a string
    '''
    address_result = GOOGLE_CLIENT.reverse_geocode(latlng=latlng)
    return address_result[0]['formatted_address']