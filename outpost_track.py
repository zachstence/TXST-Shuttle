import requests
import json
import time
from geopy.distance import geodesic

HISTORY_LENGTH = 2

# Post Road (23) is Route 639 in TXST DoubleMap API request
ROUTE_POST_ROAD = 639


history = []
while True:
  r = requests.get('http://txstate.doublemap.com/map/v2/buses')
  buses = json.loads(r.text)
  post_road_buses = [bus for bus in buses if bus['route'] == ROUTE_POST_ROAD]

  if len(history) == HISTORY_LENGTH:
    history = history[1:]
  history.append(post_road_buses)

  time.sleep(3)