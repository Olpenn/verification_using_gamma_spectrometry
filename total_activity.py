import json

with open('background_activities.json') as json_data:
    d = json.load(json_data)
    json_data.close()
    total = 0
    for key, value in d.items():
        total += value
    print("Total background activity: " + str(total))

with open('core_activities.json') as json_data:
    d = json.load(json_data)
    json_data.close()
    total = 0
    for key, value in d.items():
        total += value
    print("Total core activity: " + str(total))