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
this is a function that will check if the user selected a park or a land
"""


def get_park_or_land(user_input, country):
    with open('data.json') as f:
        data = json.load(f)
        parks = data[country]
        parks = [park for park in parks if park["name"] == user_input]

        if not parks:
            return "Park not found"

        park = parks[0]
        park_id = park['id']
        url = f"https://queue-times.com/nl/parks/{park_id}/queue_times.json"
        response = requests.get(url)
        data = response.json()

        lands = data.get("lands")
        if not lands:
            return "park"

        return "land"


"""
this function will get all the lands in the park
"""


def get_lands_per_park(user_input, country):
    with open('data.json') as f:
        data = json.load(f)
        parks = data[country]
        parks = [park for park in parks if park["name"] == user_input]

        if not parks:
            return "Park not found"

        park = parks[0]
        park_id = park['id']
        url = f"https://queue-times.com/nl/parks/{park_id}/queue_times.json"
        response = requests.get(url)
        data = response.json()

        lands = data.get("lands")
        if not lands:
            return "lands not found"

        return [land["name"] for land in lands]


def get_rides_per_land(user_input, land, country):
    with open('data.json') as f:
        data = json.load(f)
        parks = data[country]
        parks = [park for park in parks if park["name"] == user_input]

        if not parks:
            return "Park not found"

        park = parks[0]
        park_id = park['id']
        url = f"https://queue-times.com/nl/parks/{park_id}/queue_times.json"
        response = requests.get(url)
        data = response.json()

        land_chosen = land

        lands = data.get("lands")
        if not lands:
            return "lands not found"

        wait_time = []
        is_open = []
        rides = []

        # get the wait_time and is_open of the rides in the land and append them to the list
        for land in lands:
            if land["name"] == land_chosen:
                rides = land["rides"]
                for ride in rides:
                    wait_time.append(ride["wait_time"])
                    is_open.append(ride["is_open"])

        # if is_open is false then make it Gesloten instead of false
        for i in range(len(is_open)):
            if is_open[i] == False:
                is_open[i] = "Gesloten"
            else:
                is_open[i] = "Open"

        # make wait_time a str and add " min" to the end of it
        for i in range(len(wait_time)):
            wait_time[i] = str(wait_time[i]) + " min"

        # add the wait_time and is_open to the list
        return [ride["name"] for ride in rides], wait_time, is_open


"""
every park has he's own id, get the id of the park that the user want to see, and get the rides of that park with the new api link
" https://queue-times.com/nl/parks/{id}/queue_times.json" where id is the id of the park
"""


def rides_per_park(user_input, country):
    with open('data.json') as f:
        data = json.load(f)
        parks = data[country]
        parks = [park for park in parks if park["name"] == user_input]

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

        # get the wait_time and is_open of the rides and append them to the list
        wait_time = []
        is_open = []
        for ride in rides:
            wait_time.append(ride["wait_time"])
            is_open.append(ride["is_open"])

        # if is_open is false then make it Gesloten instead of false
        for i in range(len(is_open)):
            if is_open[i] == False:
                is_open[i] = "Gesloten"
            else:
                is_open[i] = "Open"

        # make wait_time a str and add " min" to the end of it
        for i in range(len(wait_time)):
            wait_time[i] = str(wait_time[i]) + " min"

        # add the wait_time and is_open to the list
        return [ride["name"] for ride in rides], wait_time, is_open


# get_rides_per_land("Efteling", "Ruigrijk", "Netherlands")
# rides_per_park("Bellewaerde", "Belgium")
