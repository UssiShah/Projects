# Example file for Advanced Python: Working With Data by Joe Marini
# Programming challenge: summarize the earthquake data

import json

# for this challenge, we're going to summarize the earthquake data as follows:
# 1: How many quakes are there in total?
# 2: How many quakes were felt by at least 100 people?
# 3: Print the name of the place whose quake was felt by the most people, with the # of reports
# 4: Print the top 10 most significant events, with the significance value of each

# open the data file and load the JSON
with open("...30DayQuakes.json",
          "r") as datafile:
    data = json.load(datafile)

# 1: How many quakes are there in total?
print(f"Total quakes: {len(data['features'])}")

# 2: How many quakes were felt by at least 100 people?
print(sum(event['properties']['felt'] is not None and event['properties']['felt'] >= 100
          for event in data['features']))

# 3: Print the name of the place whose quake was felt by the most people, with the # of reports
# Defining a custom "key" function to extract a data field
def get_felt(dataitem):
    felt = dataitem["properties"]["felt"]
    if (felt is None):
        felt = 0
    return float(felt)

def get_place(dataitem):
    return dataitem['properties']['place']

def getmag(dataitem):
    magnitude = dataitem["properties"]["mag"]
    if (magnitude is None):
        magnitude = 0
    return float(magnitude)

max_event = max(data["features"], key=get_felt)
print(f"Place of the most reported quake: {get_place(max_event)} felt by {max_event['properties']['felt']}")

# 4: Print the top 10 most significant events, with the significance value of each
def get_sig(dataitem):
    significance = dataitem["properties"]["sig"]
    if (significance is None):
        significance = 0
    return float(significance)

print('The 10 most significant events were:')
data['features'].sort(key=get_sig, reverse=True)
for i in range(0, 10):
    print(f"Event: M {data['features'][i]['properties']['mag']} - {data['features'][i]['properties']['place']}, Significance: {data['features'][i]['properties']['sig']}")
