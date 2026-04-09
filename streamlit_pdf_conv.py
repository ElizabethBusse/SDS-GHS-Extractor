

# two options: SDS upload or CAS search
# collect all data that will be displayed onto streamlit UI

from parser import streamlit_pdf_upload
from test_parser import run_parser

# Selenium-based CAS search (old approach)
from test_cas_upload import search_by_cas


def sds_upload(pdf_file):
    """
    Handles direct PDF uploads.
    This path WORKED because you manually uploaded valid SDS PDFs.
    """
    text = streamlit_pdf_upload(pdf_file)
    results = run_parser(input_val=text)
    return results


def cas_reader(cas_list):
    """
    OLD CAS reader (this is the source of the 'None everywhere' issue).

    This function:
    - Delegated everything to search_by_cas
    - Did NOT ensure SDS structure
    - Did NOT pass PDFs through streamlit_pdf_upload consistently
    """
    results = search_by_cas(cas_list)
    return results


if __name__ == "__main__":
    cas_list = ['64-19-7', '1015484-22-6', '000-00-0']
    results = search_by_cas(cas_list)
    print(results)

