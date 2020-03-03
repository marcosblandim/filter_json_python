import requests
import json
from flask import Flask

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
                if key =="time":
                    value = value.split(".")[0]
                    val = value.split(' ')
                    value = val[0] + " time " + val[1]
                    # value = "time " + value
                filtered_json[key] = value
        list_of_j.append(filtered_json)
        json_var = str(list_of_j).replace("}, ","}<br>")
        json_var = remove(json_var, ['[',']','\n','{','}'])
        json_var = json_var.replace('", "', " ; ")
        json_var = json_var.replace('":"', " = ")
        json_var = remove(json_var, ['"', ''])
        json_var = json_var.replace("time:", "date")
        json_var = json_var.replace("value", "person(s)")
    return json_var

def remove(string, bad_symbols):
    for symbol in bad_symbols:
        string = string.replace(symbol,'')
    return string

# returns final result (j_txt)
def main():
    # get json
    url = "https://uiot-dims.herokuapp.com/list/data?serviceNumber=777365"
    try:
        r = requests.get(url)
    except:
        raise Exception("request failed.")
    json_var = json.loads(r.text) # list of JSONs

    # filtering
    keys = ["time", "value"]
    json_var = filter_json(json_var, keys) # returns string

    return json_var

# output to file
filename = "filtered_dims.txt"
with open(filename, 'w') as outfile:
    json.dump(main(), outfile)

# set the server
from flask import Flask
app = Flask(__name__)
@app.route('/')
def serve_json():
    return main()

if __name__ == "__main__":
    app.run()
