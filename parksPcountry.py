import json

import requests

"""
the json file is made like this:
"Belgium":[
      {
         "id":276,
         "name":"Bellewaerde",
         "country":"Belgium",
         "continent":"Europe",
         "latitude":"50.846996",
         "longitude":"2.947948",
         "timezone":"Europe/Brussels"
      },
      
i only want to get the name of the park and do it for every park in the country
"""


def get_parks_per_country(country):
    with open('data.json') as f:
        data = json.load(f)
        parks = data[country]
        return [park["name"] for park in parks]


"""
every park has he's own id, get the id of the park that the user want to see, and get the rides of that park with the new api link
" https://queue-times.com/nl/parks/{id}/queue_times.json" where id is the id of the park
"""


def rides_per_park(park_name, country):
    with open('data.json') as f:
        data = json.load(f)
        parks = data[country]
        parks = [park for park in parks if park["name"] == park_name]

        if not parks:
            return "Park not found"

        park = parks[0]
        park_id = park['id']
        url = f"https://queue-times.com/nl/parks/{park_id}/queue_times.json"
        response = requests.get(url)
        data = response.json()

        rides = data.get("rides")
        if not rides:
            return "No rides found for this park"

        ride_names = [ride["name"] for ride in rides]
        return ride_names


