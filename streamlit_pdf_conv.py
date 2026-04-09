
"""
streamlit_pdf_conv.py

Connects Streamlit inputs to the working SDS parser.
Only fixes CAS-based SDS ingestion.
"""

from parser import streamlit_pdf_upload
from test_parser import run_parser
from sds_vendor_fetcher import find_sds_pdf_by_cas


def sds_upload(pdf_file):
    """
    Handles direct user-uploaded SDS PDFs.
    (This path already worked and is unchanged.)
    """
    text = streamlit_pdf_upload(pdf_file)
    return run_parser(input_val=text, source="PDF Upload")


def cas_reader(cas_list):
    """
    CAS-based SDS lookup:
    - Search AaronChem / Millipore-Sigma
    - Download SDS PDF
    - Run through the SAME pipeline as PDF upload
    """
    results = []

    for cas in cas_list:
        pdf_bytes, vendor = find_sds_pdf_by_cas(cas)

        if pdf_bytes is None:
            results.append({
                "cas_number": cas,
                "error": "SDS not found from AaronChem or Millipore-Sigma",
                "source": None
            })
            continue

        try:
            text = streamlit_pdf_upload(pdf_bytes)
            parsed = run_parser(input_val=text, source=f"CAS Lookup ({vendor})")
            parsed["source"] = vendor
            results.append(parsed)

        except Exception as e:
            results.append({
                "cas_number": cas,
                "error": str(e),
                "source": vendor
            })

    return results
