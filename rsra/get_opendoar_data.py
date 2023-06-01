import json
from rsra.extract_strings_from_url import get_hostname_from_url
from rsra.base_header import headers
import requests
from pprint import pprint
import rsra.config as config


"""Module to retrieve all descriptive info from institutional repositories in the specified country (default UK) via JISC's sherpa API.
    Requires an account and API key (both free) - see https://v2.sherpa.ac.uk/api/.
    """


def get_opendoar_json(offset: int, country: str = 'gb') -> tuple:
    """Uses the sherpa API to query all data on UK-based institutional repositories.
    API has no pagination function, so a loop is necessary to retrieve up to 100 records at a time.

    Args:
        offset (int): index of records to start the 100-record limit from.
        country (str): country code to check (default gb)

    Returns:
        tuple : count(int): count of records.  Limit is 100, so count<100 means you're getting the last page of results.
                r.json(json): json representation of the data retrieved in the API response.
    """
    country = country.lower()
    api_url = 'https://v2.sherpa.ac.uk/cgi/retrieve'
    api_key = config.API_KEY
    hostname = get_hostname_from_url(api_url)
    headers['Host'] = hostname
    headers['Referer'] = 'https://'+hostname

    query = {'item-type': 'repository',
             'format': 'Json',
             'limit': '100',
             'offset': 'offset',
             'order': '-id',
             'filter': [["country", "equals", "gb"]],
             'api-key': ''
             }
    query['api-key'] = api_key
    query['offset'] = 0

    r = requests.get(
        f'https://v2.sherpa.ac.uk/cgi/retrieve?item-type=repository&format=Json&limit=&offset={offset}&order=-id&filter=%5B%5B%22country%22%2C%22equals%22%2C%22{country}%22%5D%5D&api-key={api_key}&page=2', headers=headers)

    print(type(r.json()))
    count = len(r.json()['items'])
    print("count:", count)

    return count, r.json()


def build_opendoar_data():
    """Loops the request for the max (100) items in the json response from get_opendoar_json(),
    incrementing the offset by 99 until the no of records returned is less than 100.
    Builds json and saves as /data/opendoar_data.json.
    """
    more_results = True

    data = []
    offset = 0
    while more_results:

        count, json_data = get_opendoar_json(offset, 'gb')
        data.extend(json_data)
        if count < 100:
            more_results = False
        offset += 99

        with open('data/opendoar_data'+str(offset)+'.json', "w") as outfile:
            outfile.write(json.dumps(json_data))


build_opendoar_data()

if __name__ == 'main':
    build_opendoar_data()
