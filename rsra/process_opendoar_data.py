import json
from pprint import pprint
import pandas as pd

def load_json(json_file_path:str = 'data/opendoar_data.json') -> dict:

    with open(json_file_path,'r') as json_file:
        data = json.loads(json_file.read())

    return data

x = load_json()

pprint(x)



for repo in x['items']:
    try:
        print(repo['repository_metadata']['url'],repo['repository_metadata']['oai_url'])
    except KeyError:
        print('error')






