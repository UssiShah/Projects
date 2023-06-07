import json
import pandas as pd

def export_to_csv():
    file_input = '/Users/usa@gmail.com/Documents/REST API/json/calculations.json'
    file_csv = '/Users/usa@gmail.com/Documents/REST API/csv/calculations.csv'
    
    with open(file_input) as f:
        list1 = []
        data = json.loads(f.read())
        temp = data['data']['tableauUsers'][0]
        header_items = []
        get_header_items(header_items, temp)
        list1.append(header_items)

        for obj in data['data']['tableauUsers']:
            d = []
            add_items_to_data(d, obj)
            list1.append(d)

        with open(file_csv, 'w') as output_file:
            for a in list1:
                output_file.write(';'.join(map(str, a)) + "\r")

def get_header_items(items, obj):
    for x in obj:
        if isinstance(obj[x], list):
            for y in obj[x]:
                get_header_items(items, y)

        elif isinstance(obj[x], dict):
            items.append(x)
            get_header_items(items, obj[x])
            
        else:
            items.append(x)


def add_items_to_data(items, obj):
    for x in obj:
        if isinstance(obj[x], list):
            for y in obj[x]:
                add_items_to_data(items, y)
        
        elif isinstance(obj[x], dict):
            items.append("")
            add_items_to_data(items, obj[x])
        else:
            items.append(obj[x])

export_to_csv()