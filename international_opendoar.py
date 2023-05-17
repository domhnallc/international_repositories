import requests
from urllib import parse
from pprint import pprint
import pandas as pd



def get_data(offset: int) -> pd.DataFrame:
    '''Retrieves repository data from sherpa API, tailored to institutional repositories from all countries'''
    
    
    headers = {
            'Host': '',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Referer': '',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin'
        }

    api_url = 'https://v2.sherpa.ac.uk/cgi/retrieve'
    api_key = config.SHERPA_API_KEY
    hostname = parse.urlsplit(api_url).hostname
    headers['Host'] = hostname
    headers['Referer'] = 'https://'+hostname

    query = {'item-type': 'repository',
            'format': 'Json',
            'limit': '100',
            'offset': offset,            
            'order': 'id',
            'api-key': 'DF245560-D3B0-11ED-91BD-4FB046A8B528'
            }


    r = requests.get(url=api_url, headers=headers, params=query)
    #print(r.json())

    print(r.status_code)

    data = r.json()
    df = pd.json_normalize(data, 'items')

    return df

appended_data = []
for offset in range(0, 6000, 100):
    appended_data.append(get_data(offset))

full_df = pd.concat(appended_data)
full_df.set_index('system_metadata.id', inplace=True)
print(full_df)

full_df.to_csv('data/raw_opendoar_data.csv')

def data_clean(df:pd.DataFrame) -> pd.DataFrame:
    '''Drops unneccessary columns'''

    columns_to_drop = ['repository_metadata.type_phrases',
'repository_metadata.content_types',		
'repository_metadata.content_subjects_phrases',
'repository_metadata.software.name_phrases',
'repository_metadata.content_subjects',
'repository_metadata.content_types_phrases',
'repository_metadata.name',
'system_metadata.date_created',
'system_metadata.date_modified',
'system_metadata.publicly_visible_phrases',
'system_metadata.publicly_visible',
'organisation.name',
'organisation.country_phrases',
'organisation.identifiers',
'repository_metadata.policy_urls',
'organisation.notes',
'repository_metadata.notes'
]

    df_cleaned = df.drop(columns=columns_to_drop)

    return df_cleaned





