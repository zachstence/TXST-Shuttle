import requests
import json
import time
from geopy.distance import geodesic
import routes


def get_velocity(bus_hist):
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

        # Only update velocity if it exists, otherwise use previous
        if t != 0:
            bus_hist[-1]['lastVel'] = (d / t) * 60 * 60
        else:
            # If lastVel field doesn't exist yet, just skip
            try:
                bus_hist[-1]['lastVel'] = bus_hist[-2]['lastVel']
            except KeyError:
                pass


HISTORY_LENGTH = 2
history = {}
# history = {
#     bus_id : bus_history,
#     bus_id : bus_history,
#     ...
# }
#
# bus_history = {
#     'id'         : 3 digit ID,
#     'name'       : id as a string (generally),
#     'lat'        : latitude of bus,
#     'lon'        : longitude of bus,
#     'heading'    : 0-360 value: 0=stopped, 360=north,
#     'route'      : route id the bus is currently driving,
#     'lastStop'   : ID of the last stop the bus was at,
#     'fields'     : extra information,
#     'lastUpdate' : unix timestamp when information was last updated,
#     'capacity'   : # of passengers the bus can hold,
#     'load'       : # of passengers on the bus (rarely used)
# }
while True:
    # Poll API and extract wanted information
    r = requests.get('http://txstate.doublemap.com/map/v2/buses')
    buses_info = json.loads(r.text)
    buses_info = [bus for bus in buses_info if bus['route'] == routes.R21_OFFCAMPUS_BLANCO_RIVER]

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
        get_velocity(bus_history)
        print('id: %s   head: %3d   speed: ' % (bus_history[-1]['id'],  bus_history[-1]['heading']), end='')
        try:
            print('%5.2f' % bus_history[-1]['lastVel'])
        except KeyError:
            print('')

    print()

    # Wait 3 seconds between polling API, doesn't update any faster
    time.sleep(3)



