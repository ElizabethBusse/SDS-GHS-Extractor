import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_aaronchem_sds(cas):
    search_url = f"https://www.aaronchem.com/search?type=product&q={cas}"

    r = requests.get(search_url, headers=HEADERS, timeout=10)
    if not r.ok:
        return None

    # Find PDF links
    pdf_links = re.findall(r"https?://[^\"']+\.pdf", r.text, re.IGNORECASE)

    for link in pdf_links:
        if "sds" in link.lower():
            pdf = requests.get(link, headers=HEADERS, timeout=15)
            if pdf.ok and pdf.headers.get("content-type", "").lower().startswith("application/pdf"):
                return pdf.content

    return None

def fetch_sigma_sds(cas):
    search_url = f"https://www.sigmaaldrich.com/US/en/search/{cas}?focus=products"

    r = requests.get(search_url, headers=HEADERS, timeout=10)
    if not r.ok:
        return None

    pdf_links = re.findall(r"https?://[^\"']+\.pdf", r.text, re.IGNORECASE)

    for link in pdf_links:
        if "sds" in link.lower():
            pdf = requests.get(link, headers=HEADERS, timeout=15)
            if pdf.ok and pdf.headers.get("content-type", "").lower().startswith("application/pdf"):
                return pdf.content

    return None

def find_sds_pdf_by_cas(cas):
    # 1️⃣ AaronChem
    pdf = fetch_aaronchem_sds(cas)
    if pdf:
        return pdf, "AaronChem"

    # 2️⃣ Millipore / Sigma
    pdf = fetch_sigma_sds(cas)
    if pdf:
        return pdf, "Millipore-Sigma"

    # ❌ Explicit failure
    return None, None
