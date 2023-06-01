#!/usr/bin/env python

__author__ = "Domhnall Carlin"
__copyright__ = "Copyright 2023 Queen's University Belfast"
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Domhnall carlin"
__status__ = "Development"


def determine_ris_platform_from_url(url: str) -> str:
    """Function to determine the RIS software platform from features in the URL

    Args:
        url (str): URL including search string parameters

    Returns:
        str: name of the 
    """
    pure_strings = ['/en/publications/', 'Fatira%2Fpure']
    dspace_strings = ['browse?type=type&value=Software', 'browse?type=type&value=software'
                      'openrepository.com', 'dspace']
    eprints_strings = ['/cgi/search/archive/advanced',
                       '/cgi/search/advanced', 'eprint']
    figshare_strings = ['figshare', 'search?itemTypes=9']
    haplo_strings = ['search?q=type%3A%22software%22',
                     'search?q=type%3Asoftware']
    worktribe_strings = ['worktribe']
    equella_strings = ['searching.do']
    fedora_strings = ['?utf8=%E2%9C%93&q=&']
    esploro_strings = ['esploro']
    hal_strings = ['/search/index/?q=*&docType_s=SOFTWARE']

    if not url.startswith('#'):
        if any([x in url for x in pure_strings]):
            return 'pure'
        elif any([x in url for x in eprints_strings]):
            return 'eprints'
        elif any([x in url for x in dspace_strings]):
            return 'dspace'
        elif any([x in url for x in figshare_strings]):
            return 'figshare'
        elif any([x in url for x in haplo_strings]):
            return 'haplo'
        elif any([x in url for x in worktribe_strings]):
            return 'worktribe'
        elif any([x in url for x in equella_strings]):
            return 'equella'
        elif any([x in url for x in fedora_strings]):
            return 'fedora'
        elif any([x in url for x in esploro_strings]):
            return 'esploro'
        elif any([x in url for x in hal_strings]):
            return 'hal'
        else:
            # print(url)
            return determine_ris_platform_from_page_source(url)


def determine_ris_platform_from_page_source(url):
    from bs4 import BeautifulSoup
    import requests
    from rsra.extract_strings_from_url import get_hostname_from_url

    hostname = get_hostname_from_url(url)
    headers = {
        'Host': hostname,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://'+hostname,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin'
    }

    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        check = soup.find("meta", {'name': "Generator"})
        if check == None:
            return 'unknown (error)'
        elif 'DSpace' in check.get('content'):
            return 'dspace'
        # VuFind
        elif 'VuFind' in check.get('content'):
            return 'vufind'
        else:
            return 'unknown'
    except requests.exceptions.ConnectionError:
        return 'unknown (connection error)'


if __name__ == '__main__':
    data = []
    with open('data/raw_manual_queries.txt', 'r') as urls:
        for url in urls:
            if not url.startswith('#'):
                data.append(url.strip() + ',' +
                            determine_ris_platform_from_url(url))

    # print(data)
    # with open('determine_ris.csv', 'w') as outfile:
    #    for item in data:
    #        outfile.writelines(item)
