import requests
from urllib import parse
import pandas as pd
import config
import numpy as np

'''- Queries the sherpa API 'https://v2.sherpa.ac.uk/cgi/retrieve' using authorisation in the config for repositories.
- Whole raw data is saved to /data/raw_opendoar_data.csv.  
- Data cleaning removes unneeded columns and filters for institutional repositories.
- Cleaned dataset is saved to data/cleaned_opendoar_data.csv'''


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
    hostname = parse.urlsplit(api_url).hostname
    headers['Host'] = hostname
    headers['Referer'] = 'https://'+hostname

    query = {'item-type': 'repository',
             'format': 'Json',
             'limit': '100',
             'offset': offset,
             'order': 'id',
             'api-key': config.SHERPA_API_KEY
             }

    r = requests.get(url=api_url, headers=headers, params=query)
    print(r.status_code)
    data = r.json()
    df_raw = pd.json_normalize(data, 'items')

    return df_raw


def data_clean(df: pd.DataFrame) -> pd.DataFrame:
    '''Drops unneccessary columns, removes empty rows, filters to only institutional repos'''

    print(df.keys())

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
    df_cleaned['system_metadata.id'].replace(
        '', np.nan, inplace=True)  # used to remove blanks
    df_cleaned.dropna(subset=['system_metadata.id'],
                      inplace=True)  # used to filter blank lines
    df_cleaned = df_cleaned.loc[df['repository_metadata.type']
                                == 'institutional']

    return df_cleaned


def runner():
    '''Paginates api responses (max=100) and appends all to a final df.
    Final df is saved as csv to data/cleaned_open_doar_data.csv'''

    appended_data = []
    for offset in range(0, 5600, 100):
        appended_data.append(get_data(offset))

    full_df = pd.concat(appended_data)
    # full_df.set_index('system_metadata.id', inplace=True)
    full_df.to_csv('data/raw_opendoar_data.csv')

    df_cleaned_data = data_clean(full_df)
    df_cleaned_data.set_index('system_metadata.id', inplace=True)
    df_cleaned_data.to_csv('data/cleaned_opendoar_data.csv')


if __name__ == '__main__':
    runner()
