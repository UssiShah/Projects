# Example file for Advanced Python: Working With Data by Joe Marini
# Programming challenge: use advanced data collections on the earthquake data

import json
from collections import defaultdict



# open the data file and load the JSON
with open("/Users/usama.shahid.siddiqui@schibsted.com/Documents/Learning/advanced-python-working-with-data-4312001/30DayQuakes.json",
          "r") as datafile:
          data=json.load(datafile)

# Steps: create a list of all 'types' including duplicates
all_quake_types = list(event['properties']['type'] for event in data['features'])

type_counter = defaultdict(int)

for quake_type in all_quake_types:
    type_counter[quake_type] += 1

print(type_counter)

for i in type_counter:
    print(i, ': ', type_counter[i])





