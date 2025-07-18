import requests

def get_cid_from_cas(cas_number):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas_number}/cids/JSON"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        try:
            return data['IdentifierList']['CID'][0]
        except KeyError:
            return None
    else:
        return None

# Example usage:
cas_number = "7727-37-9"  # Ethanol
cid = get_cid_from_cas(cas_number)
print(f"CID for CAS {cas_number}: {cid}")