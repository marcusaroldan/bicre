## Planning for project:
### Integrate biking with transit options
    - Alerts for bike parking
        - Filters: "BRINING_BIKE", "STORE_BIKE"

- combine biking with transit
- take whole route, separate into segments, determine best for cycling / transit (slow zones?)

1. PlacesAPI or GeocodingAPI --> placeID

Directions API Parameters:
    1. Origin: PlaceID
    2. Mode: 'trainsit', 'bicycling'
    3. Transit Routing Preference: 'less_walking' or 'fewer_transfers'

Desired Functionality:
    1. User specifies origin and destination locations (using standard names / addresses)
        1a. User could specify more parameters for route (train / tram only, etc.)
    2. Use GeocodingAPI to get origin / destination PlaceIDs
    3. Use DirectionAPI to generate route using transit
        3a. Convert route into steps (walking, transit)
        3b. Confirm transit allows bikes using MBTA Alerts API
        3c. If bikes not allowed, find alternative route (TBD)
        3d. Take walking steps, generate cycling directions
    4. Format readable route (using Maps Embed API)