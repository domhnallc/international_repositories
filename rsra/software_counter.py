from rsra.scrapers import *
from rsra.url_checker import determine_ris_platform_from_url

def get_software_counts(url: str) -> int:

    manual_software_count = 0

    match determine_ris_platform_from_url(url):
        case 'pure':
            manual_software_count = scrape_pure_site_full_query(url)
        case 'eprints':
            manual_software_count = scrape_eprints_full_query(url)
        case 'dspace':
            manual_software_count = scrape_dspace_full_query(url)
        case 'figshare':
            manual_software_count = scrape_figshare_full_query(url)
        case 'haplo':
            manual_software_count = scrape_haplo_full_query(url)
        case 'worktribe':
            manual_software_count = 0
        case 'equella':
            manual_software_count = 0
        case 'fedora':
            manual_software_count = 0
        case 'esploro':
            manual_software_count = 0
        case 'unknown':
            manual_software_count = 0
    
    if manual_software_count == None:
                    manual_software_count = 0
    
    
    return manual_software_count

if __name__ == '__main__':
     
     get_software_counts('https://kclpure.kcl.ac.uk/portal/en/publications/search.html?type=%2Fdk%2Fatira%2Fpure%2Fresearchoutput%2Fresearchoutputtypes%2Fnontextual%2Fsoftware')