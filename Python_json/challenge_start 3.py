# Example file for Advanced Python: Working With Data by Joe Marini
# Programming challenge: use advanced data collections on the earthquake data

import json
import csv
import datetime


# open the data file and load the JSON
with open("/Users/usama.shahid.siddiqui@schibsted.com/Documents/Learning/advanced-python-working-with-data-4312001/30DayQuakes.json", "r") as datafile:
    data = json.load(datafile)

# Create a CSV file with the following information:
# 40 most significant seismic events, ordered by most recent
# Header row: Magnitude, Place, Felt Reports, Date, and Google Map link
# Date should be in the format of YYYY-MM-DD

### Exploration:
"""
# Exploring how the Google Maps URL is made up:
for event in data['features']:
    if (event['properties']['mag'] == 5.21 
            and event['properties']['place'] == "15km W of Petrolia, CA"):
        print(event)
"""

### Transform data - getting to the required data:
## Functions:
# Define a function to get significance:
def get_id(dataitem):
    return dataitem['id']

# Define a function to get time:
def get_time(dataitem):
    return dataitem['properties']['time']

# Define a function to get significance:
def get_sig(dataitem):
    significance = dataitem['properties']['sig']
    if (significance is None):
        significance = 0
    return float(significance)

# Define a function to get the datetime:
def simplify(q):
    return {
        "Magnitude": q['properties']['mag'],
        "Place": q['properties']['place'],
        "Felt Reports": q['properties']['felt'],
        "Date": str(datetime.date.fromtimestamp(q['properties']["time"]/1000)),
        "Link": str('https://maps.google.com/maps/search/?api=1&query=' + 
                    str(q['geometry']['coordinates'][1]) + '%2C' +
                    str(q['geometry']['coordinates'][0]))

    }

## Transformations:
# Sort all events based on significance:
data['features'].sort(key=get_sig, reverse=True)

# Create an empty list
sig_fltrd_events = []
# Add the 40 most significant events to the list:
for i in range(0, 40): 
    sig_fltrd_events.append(data['features'][i])

# Sort by most recent
sig_fltrd_events.sort(key=get_time, reverse=True)

# Using the id_list as a criterion, fiter out the events that are not significant:
sig_fltrd_smplfd_events = list(map(simplify, sig_fltrd_events))
print(sig_fltrd_smplfd_events)

### Importing data into a CSV:

# Create the header and row structures for the data
header = ["Magnitude", "Place", "Felt Reports", "Date", "Link"]
rows = []

# populate the rows with the resulting quake data
for event in sig_fltrd_smplfd_events:
    rows.append([event["Magnitude"], 
                 event["Place"],
                 event["Felt Reports"],
                 event["Date"],
                 event["Link"]])

# write the results to the CSV file
with open("results.csv", "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(header)
    writer.writerows(rows)
