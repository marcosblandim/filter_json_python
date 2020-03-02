import requests
import json
from flask import Flask
import argparse

# custom filter json
def filter_json(j_txt, keys):
    '''
    receives list of dicts
    (python representation of
    a JSON) and returns a
    filtered list of dicts.
    '''
    list_of_j = []
    for dictionary in j_txt:
        filtered_json = dict()
        for (key, value) in dictionary.items():
            if key in keys:
                filtered_json[key] = value
        list_of_j.append(filtered_json)
    return list_of_j

# get json
url = "https://uiot-dims.herokuapp.com/list/data?serviceNumber=777365"
try:
    r = requests.get(url)
except:
    raise Exception("request failed.")
j_txt = r.text
j_py = json.loads(j_txt) # list of JSONs

# filtering
keys = ["time", "value"]
j_py = filter_json(j_py, keys)

# back to json
j_txt = json.dumps(j_py)

# output to file
filename = "filtered_dims.txt"
with open(filename, 'w') as outfile:
    json.dump(j_py, outfile)

# set the server
from flask import Flask
app = Flask(__name__)
@app.route('/')
def serve_json():
    return j_txt

'''
note that to set the server 
you must run with:
$ export FLASK_APP=main.py
$ flask run
'''