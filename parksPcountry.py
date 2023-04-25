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
        print(f"park ID: {park_id}")
        url = f"https://queue-times.com/nl/parks/{park_id}/queue_times.json"
        response = requests.get(url)
        data = response.json()

        rides = data.get("rides")
        if not rides:
            return "No rides found for this park"

        ride_names = [ride["name"] for ride in rides]
        return ride_names


"""
this is a example of the json file that i get from the api per park

{
    "id":5585,
    "name":"#LikeMe Coaster",
    "is_open":true,
    "wait_time":0,
    "last_updated":"2023-04-24T13:01:13.000Z"
},

get waitime and status of the ride
"""


def wait_time(park_name, country):
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

        # check if the park has rides in the rides or land key
        if data.get("lands"):
            lands = data.get("lands")
            # get all the names of the lands
            land_names = [land["name"] for land in lands]
            # print the names of rides in the lands
            for land in lands:
                rides = land.get("rides")

            # all rides = land + rides
            all_rides = []
            all_wait_time = []
            all_is_open = []
            for land in lands:
                rides = land.get("rides")
                all_rides += rides
                for ride in rides:
                    all_wait_time.append(ride["wait_time"])
                    all_is_open.append(ride["is_open"])



            # change the status from true/false to open/closed
            for i in range(len(all_is_open)):
                if all_is_open[i] == True:
                    all_is_open[i] = "Open"
                else:
                    all_is_open[i] = "Closed"

            all_rides = [str(i) for i in all_rides]
            # change the wait time from int to string
            all_wait_time = [str(i) for i in all_wait_time]

            # add min to the wait time
            for i in range(len(all_wait_time)):
                all_wait_time[i] += " min"

            # make a list with all the info
            total_info = []
            # print(len(all_rides))
            for i in range(0, len(all_rides)):
                print(i)
                total_info.append([all_rides[i], all_wait_time[i], all_is_open[i]])

            return total_info



        elif data.get("rides"):
            rides = data.get("rides")
            ride_names = [ride["name"] for ride in rides]
            is_open = [ride["is_open"] for ride in rides]
            wait_time = [ride["wait_time"] for ride in rides]



            wait_time = [str(i) for i in wait_time]

            for i in range(len(wait_time)):
                wait_time[i] += " min"

            # change the status from true/false to open/closed
            for i in range(len(is_open)):
                if is_open[i] == True:
                    is_open[i] = "Open"
                else:
                    is_open[i] = "Closed"

            total_info = []
            for i in range(len(rides)):
                total_info.append([ride_names[i], wait_time[i], is_open[i]])

        else:
            return "No rides or lands found for this park"

        return total_info


def a(park_name, country):
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

        # get the wait time and status of all the rides
        ride_names = [ride["name"] for ride in rides]
        ride_wait_time = [ride["wait_time"] for ride in rides]
        ride_status = [ride["is_open"] for ride in rides]


        ride_wait_time = [str(i) for i in ride_wait_time]

        # change the status from true/false to open/closed
        for i in range(len(ride_status)):
            if ride_status[i] == True:
                ride_status[i] = "Open"
            else:
                ride_status[i] = "Closed"

        total_info = []



        for i in range(len(rides)):
            total_info.append([ride_names[i], ride_wait_time[i], ride_status[i]])

        return total_info


