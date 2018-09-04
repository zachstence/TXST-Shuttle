import requests
import json
import time
from geopy.distance import geodesic
from datetime import datetime

# maybe have more complicated functions to calculate velocity based off more points
# for a higher accuracy? for now just going to do last 2



# returns the velocity of one bus based on its history of position and time
# only considers 2 most recent history points
def calcVelocity2(bus_history):
  if len(bus_history) >= 2:
    p1 = (bus_history[-2]['lat'], bus_history[-2]['lon'])
    p2 = (bus_history[-1]['lat'], bus_history[-1]['lon'])
    d = geodesic(p1, p2).miles

    t1 = bus_history[-2]['lastUpdate']
    t2 = bus_history[-1]['lastUpdate']
    t = t2 - t1

    if t != 0:
      return (d / t) * 60 * 60
    else:
      return None










HISTORY_LENGTH = 2

# Post Road (23) is Route 639 in TXST DoubleMap API request
ROUTE_POST_ROAD = 639

# for calculating velocity of buses
history = {}
while True:
  r = requests.get('http://txstate.doublemap.com/map/v2/buses')
  buses_info = json.loads(r.text)
  buses_info = [bus for bus in buses_info if bus['route'] == ROUTE_POST_ROAD]

  for bus_info in buses_info:
    bus_id = bus_info['id']

    # append new history or start a list with it
    if bus_id in history.keys():
      history[bus_id].append(bus_info)
      # if full, clip oldest
      if len(history[bus_id]) > HISTORY_LENGTH:
        history[bus_id] = history[bus_id][1:]
    else:
      history[bus_id] = [bus_info]

  # print velocities
  for bus_history in history.values():
    print("{}\t {}".format(bus_history[0]['id'], calcVelocity2(bus_history)))

  print()




  time.sleep(3)



