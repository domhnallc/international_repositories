from bs4 import BeautifulSoup
import requests
import pprint
from rsra.query_data import *
from rsra.extract_strings_from_url import get_hostname_from_url
from rsra.base_header import headers


"""Module contains the scrapers implemented on a RIS platform basis.  
Each is implemented to search for software within the institutional repositories 
based on the url provided and return an int of the count of software, if present.
"""


def set_headers(url: str) -> dict:
    """Generates the hostname from the URL and adds to the base_header

    Args:
        url (str): url to be retrieved

    Returns:
        dict: dict of headers for the request
    """
    hostname = get_hostname_from_url(url)
    headers["Host"] = hostname
    headers["Referer"] = "https://" + hostname

    return headers


def scrape_hal_full_query(url: str) -> int:
    # /search/index/?q=*&docType_s=SOFTWARE
    # class="results-header"
    try:
        r = requests.get(url, headers=set_headers(url))
        soup = BeautifulSoup(r.content, "html5lib")
        x = soup.find_all("span", attrs={"class": "results-header"})
        if len(x) > 0:
            return x
    except AttributeError:
        pass
    except requests.exceptions.ConnectionError:
        print("CONNECTION ERROR", url)
    except requests.exceptions.TooManyRedirects:
        print("REDIRECT ERROR", url)
        
def scrape_weko_url(url: str) -> int:
    #url1 = 'https://niigata-u.repo.nii.ac.jp'
    #url2 = 'https://hirosaki.repo.nii.ac.jp'

    search1 = '/search?page=1&size=20&sort=-createdate&search_type=0&q=&title=&creator=&filedate_from=&filedate_to=&fd_attr=&srctitle=&type=43&dategranted_from=&dategranted_to=&dissno=&wid='
    #search2 = '/?action=pages_view_main&active_action=repository_view_main_item_snippet&all=&title=&creator=&typeList=12&pubYearFrom=&pubYearUntil=&idx=&wekoAuthorId=&count=20&order=7&pn=1&page_id=13&block_id=21' # seems to not allow this to be directly visited
    host = 'niigata-u.repo.nii.ac.jp'

    headers = headers=set_headers(url)

    url_string1 = url + search1 
    #url_string2 = url2 + search2


    try:
    # TODO move out to config file
        driver = webdriver.Chrome("/snap/bin/chromium.chromedriver")
        driver.get(url_string1)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, "html5lib")
        if '404 Not Found' in soup.text:
            return '404 error'
        else:
            x = soup.find("div", attrs={"class": "invenio-search-results"}).text
        if 'No results' in x:
            return 0
        else:
            return x
    except AttributeError:
        print("attribute error")
        return 0

    except ConnectionResetError:
        print("Connection reset", url)
    finally:
        driver.quit()  


def scrape_eprints_full_query(url: str) -> int:
    """Scrapes a url from a known eprints host for a specific tag/class with the value of the software in the repository

    Args:
        url (str): url with full search parameters from raw_manual_queries to scrape

    Returns:
        int: count of software in the repository, based on scraping the html (see x)
    """
    try:
        r = requests.get(url, headers=set_headers(url))
        soup = BeautifulSoup(r.content, "html5lib")
        x = soup.findAll("span", attrs={"class": "ep_search_number"})
        if len(x) > 0:
            return int(x[-1].text)
        elif (
            "Search has no matches"
            in soup.find("div", attrs={"class": "ep_search_controls"}).text
        ):
            # return soup.find('div', attrs={'class': 'ep_search_controls'}).text[0:3]
            return 0
    except AttributeError:
        pass
    except requests.exceptions.ConnectionError:
        print("CONNECTION ERROR", url)
    except requests.exceptions.TooManyRedirects:
        print("REDIRECT ERROR", url)


# TODO needs implemented properly


def scrape_eprints_without_query(url):
    """Scrapes a url from a known eprints host for a specific tag/class with the value of the software in the repository.
    default search parameters are added to the base url.

    Args:
        url (str): url to scrape

    Returns:
        int: count of software in the repository, based on scraping the html (see x)
    """
    try:
        r = requests.get(url, headers=set_headers(url))
        soup = BeautifulSoup(r.content, "html5lib")
        x = soup.find("div", attrs={"id": "column-2-content"})
        if x:
            return x[-1].text
        elif (
            "Search has no matches"
            in soup.find("div", attrs={"class": "ep_search_controls"}).text
        ):
            # soup.find('div', attrs={'class': 'ep_search_controls'}).text[0:3]
            return 0
        else:
            return "Error"
    except AttributeError:
        pass
    except requests.exceptions.ConnectionError:
        print("CONNECTION ERROR", url)
    except requests.exceptions.TooManyRedirects:
        print("REDIRECT ERROR", url)


def scrape_dspace_full_query(url: str) -> int:
    """Scrapes a url from a known dspace host for a specific tag/class with the value of the software in the repository.
    Several hosts have a different implementation from rest- see special cases []  and imperial.ac.uk

    Args:
        url (str): url with full search parameters from raw_manual_queries to scrape

    Returns:
        int: count of software in the repository, based on scraping the html (see x)
    """

    hostname = get_hostname_from_url(url)
    print("host", hostname)
    dspace_special_cases = ["ore.exeter.ac.uk", "repository.cam.ac.uk"]
    try:
        r = requests.get(url, headers=set_headers(url))
        soup = BeautifulSoup(r.content, "html5lib")

        if "imperial.ac.uk" in url:
            print("imperial mode")
            x = soup.find(
                "div", attrs={"class": "discovery-result-pagination row container"}
            ).text
            # initial \n causing strip to return NoneType
            return int(x.split()[3])
        elif (
            "bodleian.ox.ac.uk" in url
            and "No items found" in soup.find("h4", attrs={"class": None}).text
        ):
            return 0
        elif "openrepository.com" in url:
            x = soup.find("p", attrs={"class": "ds-paragraph"}).text
            if x == "Search produced no results":
                return 0
        elif any([x in url for x in dspace_special_cases]):
            x = soup.find("p", attrs={"class": "pagination-info"}).text
            return int(x.strip().split()[5])
        else:
            x = soup.find(
                "div", attrs={"class": "discovery-result-pagination row container"}
            ).text
            return int(x.strip().split()[5])

    except AttributeError:
        print("ATTRIBUTE ERROR", url)
        pass
    except requests.exceptions.ConnectionError:
        print("CONNECTION ERROR", url)


# TODO needs implemented properly


def scrape_pure_site_host(host):
    url_string = "https://" + host + "/en/publications"
    r = requests.get(url_string, headers=set_headers(host))
    soup = BeautifulSoup(r.content, "html5lib")
    x = soup.find("li", attrs={"class": "search-pager-information"}).text

    return x.strip().split()[0]

def scrape_pure_site_url(url):
    url_string = url + "/en/publications"
    r = requests.get(url_string, headers=set_headers(host))
    soup = BeautifulSoup(r.content, "html5lib")
    x = soup.find("li", attrs={"class": "search-pager-information"}).text

    return x.strip().split()[0]


def scrape_pure_site_full_query(url):
    """Scrapes a url from a known PURE host for a specific tag/class with the value of the software in the repository.
    Several hosts have a different implementation from rest- see special cases [].

    Args:
        url (str): url with full search parameters from raw_manual_queries to scrape

    Returns:
        int: count of software in the repository, based on scraping the html (see x)
    """
    r = requests.get(url, headers=set_headers(url))
    soup = BeautifulSoup(r.content, "html5lib")

    pure_special_cases = [
        "research.bangor.ac.uk",
        "risweb.st-andrews",
        "kclpure.kcl.ac.uk/",
        "https://pure.aber.ac.uk/",
    ]
    try:
        if any([spec_case in url for spec_case in pure_special_cases]):
            # <span class="portal_navigator_window_info">1 - 10 out of 283</span>
            x = soup.find("span", attrs={"class": "portal_navigator_window_info"}).text

            return int(x.strip().split()[5])
        else:
            x = soup.find("li", attrs={"class": "search-pager-information"}).text
            if len(x) >= 2:
                return int(x.strip().split()[-2])

    except AttributeError:
        pass


def scrape_figshare_full_query(url):
    """Scrapes a url from a known Figshare host for a specific tag/class with the value of the software in the repository.
    Function operates differently to others in this module as the html identifying the result is generated by a browser.
    Selenium is used to control Chrome/Chromium.  A working installation of Chrome/chromium and chromedriver is required.
    See README.
    Args:
        url (str): url with full search parameters from raw_manual_queries to scrape

    Returns:
        int: count of software in the repository, based on scraping the html (see x)
    """
    import time
    from selenium import webdriver

    try:
        # TODO move out to config file
        driver = webdriver.Chrome("/snap/bin/chromium.chromedriver")
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, "html5lib")
        x = soup.find("span", attrs={"class": "ctMjQ"}).text
        return int(x.split()[0])
    except AttributeError:
        print("attribute error")
        return 0

    except ConnectionResetError:
        print("Connection reset", url)
    finally:
        driver.quit()


def scrape_haplo_full_query(url):
    """Scrapes a url from a known haplo host for a specific tag/class with the value of the software in the repository.

    Args:
        url (str): url with full search parameters from raw_manual_queries to scrape

    Returns:
        int: count of software in the repository, based on scraping the html (see x)
    """
    headers = set_headers(url)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")
    try:
        x = soup.find("div", attrs={"class": "haplo-results-info"}).text
        return int(x.split()[0])
    except AttributeError:
        print("no software search")
        return 0


def scrape_vufind_full_query(url):
    """Scrapes a url from a known VuFind host for a specific tag/class with the value of the software in the repository.

    Args:
        url (str): url with full search parameters from raw_manual_queries to scrape

    Returns:
        int: count of software in the repository, based on scraping the html (see x)
    """
    headers = set_headers(url)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")
    try:
        x = soup.find("div", attrs={"class": "col-sm-12"}).text
        if "NoResults!" in x.split()[0] + x.split()[1]:
            return 0
        else:
            return int(x.split()[0])
    except AttributeError:
        print(url, "no software search")
        return 0


def write_repo_to_csv(repo_data):
    import csv

    with open("mycsvfile.csv", "w+") as f:
        w = csv.DictWriter(f, repo_data.keys())
        w.writeheader()
        w.writerow(repo_data)


if __name__ == "__main__":
    x = scrape_pure_site_full_query(
        "https://kclpure.kcl.ac.uk/portal/en/publications/search.html?type=%2Fdk%2Fatira%2Fpure%2Fresearchoutput%2Fresearchoutputtypes%2Fnontextual%2Fsoftware"
    )
    print(type(x))
    print(x)
