import requests
import json
import time
from geopy.distance import geodesic
from datetime import datetime

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

    # append new history
    if bus_id in history.keys():
      history[bus_id].append(bus_info)
      # if full, clip oldest
      if len(history[bus_id]) > HISTORY_LENGTH:
        history[bus_id] = history[bus_id][1:]

    else:
      history[bus_id] = [bus_info]

  # now calculate velocity = change distance / change time
  for bus in history.values():
    try:
      p1 = (bus[-2]['lat'], bus[-2]['lon'])
      p2 = (bus[-1]['lat'], bus[-1]['lon'])
      d = geodesic(p1, p2).miles
  
      t1 = bus[-2]['lastUpdate']
      t2 = bus[-1]['lastUpdate']
      t = t2 - t1

      # calculate velocity in mph
      if t != 0:
        v = (d / t) * 60 * 60
      else:
        v = None
      print("{}\t {} {} {}".format(bus[0]['id'], d, t, v))

    except IndexError:
      pass
  print()

  # print all dict info
  # print(json.dumps(history, indent=2))

  # print only time, lat and lon for one bus
  # try:
  #   for i in range(HISTORY_LENGTH):
  #     t = datetime.fromtimestamp(history[417][i]['lastUpdate']).strftime('%H:%M:%S')
  #     lat = history[417][i]['lat']
  #     lon = history[417][i]['lon']
  #     print(t, lat, lon)
  # except:
  #   pass
  # print()





  time.sleep(3)



