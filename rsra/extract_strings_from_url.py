from urllib import parse


def get_params_from_url(url: str) -> dict:
    """ Takes a url featuring search parameters and breaks them into key/value pairs

    Args:
        url (str): URL to break down

    Returns:
        dict: a dict of key value pairs of search parameters from the url
    """
    if not url.startswith('#'):
        return dict(parse.parse_qsl(parse.urlsplit(url).query))



def get_hostname_from_url(url: str) -> str:
    """Returns hostname from a url e.g pure.qub.ac.uk

    Args:
        url (str): url to break down

    Returns:
        str: hostname
    """
    if not url.startswith('#'):
        return parse.urlsplit(url).hostname


def tests():
    #urls = ['https://cronfa.swan.ac.uk/Search/Results?join=AND&lookfor0%5B%5D=&type0%5B%5D=AllFields&lookfor0%5B%5D=&type0%5B%5D=AllFields&lookfor0%5B%5D=&type0%5B%5D=AllFields&bool0%5B%5D=AND&filter%5B%5D=%7Eformat%3A%22Computer+program%22&illustration=-1&daterange%5B%5D=publishDate&publishDatefrom=&publishDateto=',
            #'https://ore.exeter.ac.uk/repository/discover?filtertype_1=type&filter_relational_operator_1=contains&filter_1=software&filtertype_2=title&filter_relational_operator_2=contains&filter_2=&submit_apply_filter=']
    with open('./raw_manual_queries.txt','r') as urls:
        for url in urls:
            if not url.startswith('#'):
               #print(get_params_from_url(url))
               print(get_hostname_from_url(url))
            else:
                pass


#tests()
