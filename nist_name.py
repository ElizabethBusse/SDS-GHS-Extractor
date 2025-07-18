import requests
from bs4 import BeautifulSoup

def get_nist_names(cas):
    """
    Scrapes the NIST Chemistry WebBook page and returns a list of 'Other names'.
    """
    url = f"https://webbook.nist.gov/cgi/cbook.cgi?ID={cas}&Units=SI"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Search through all <li> tags to find the one containing 'Other names:'
        li_tags = soup.find_all('li')
        for li in li_tags:
            strong_tag = li.find('strong')
            if strong_tag and "Other names" in strong_tag.text:
                other_names_raw = li.get_text(separator=' ')
                other_names = other_names_raw.replace("Other names:", "").strip().split(';')
                return [name.strip() for name in other_names if name.strip()]
            
    except Exception as e:
        print(f"NIST Error: {e}")
        return []
    
    # Fallback if not found
    return []

# url = 'https://webbook.nist.gov/cgi/cbook.cgi?ID=64-19-7&Units=SI'
# names = get_other_names(url)
# print(names)