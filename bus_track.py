import requests
import json
import time
from geopy.distance import geodesic

# maybe have more complicated functions to calculate velocity based off more points
# for a higher accuracy? for now just going to do last 2


def calc_velocity_2(bus_hist):
    """
    Calculates the approximate velocity of a bus using (d2-d1)/(t2-t1)
    :param bus_hist: A list of bus dictionaries containing info about the bus's position, bearing, etc
    :return: The velocity of the bus in mph, None if t2-t1 == 0
    """
    if len(bus_hist) >= 2:
        p1 = (bus_hist[-2]['lat'], bus_hist[-2]['lon'])
        p2 = (bus_hist[-1]['lat'], bus_hist[-1]['lon'])
        d = geodesic(p1, p2).miles

        t1 = bus_hist[-2]['lastUpdate']
        t2 = bus_hist[-1]['lastUpdate']
        t = t2 - t1

        if t != 0:
            return (d / t) * 60 * 60
        else:
            return None


HISTORY_LENGTH = 2

# Post Road (23) is Route 639 in TXST DoubleMap API request
ROUTE_POST_ROAD = 639


history = {}
while True:
    # Poll API and extract wanted information
    r = requests.get('http://txstate.doublemap.com/map/v2/buses')
    buses_info = json.loads(r.text)
    buses_info = [bus for bus in buses_info if bus['route'] == ROUTE_POST_ROAD]

    for bus_info in buses_info:
        bus_id = bus_info['id']

        # Append new history or start a list
        if bus_id in history.keys():
            history[bus_id].append(bus_info)
            # If full, clip the oldest entry
            if len(history[bus_id]) > HISTORY_LENGTH:
                history[bus_id] = history[bus_id][1:]
        else:
            history[bus_id] = [bus_info]

    # Print bus velocities
    for bus_history in history.values():
        print("{}\t {}".format(bus_history[0]['id'], calc_velocity_2(bus_history)))

    print()

    # Wait 3 seconds between polling API, doesn't update any faster
    time.sleep(3)



