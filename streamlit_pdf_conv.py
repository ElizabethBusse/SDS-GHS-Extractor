
"""
streamlit_pdf_conv.py

Connects Streamlit inputs to the SDS parser.
NO parser logic is modified.
"""

from parser import streamlit_pdf_upload, parse_sds_file
from sds_vendor_fetcher import find_sds_pdf_by_cas


def sds_upload(pdf_file):
    """
    Handles direct user-uploaded SDS PDFs.
    This path already works and is unchanged.
    """
    text = streamlit_pdf_upload(pdf_file)
    return parse_sds_file(input_val=text, source="PDF Upload")


def cas_reader(cas_list):
    """
    CAS-based SDS lookup:
    - Search AaronChem / Millipore-Sigma
    - Download SDS PDF
    - Run through the SAME parser as PDF upload
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
            parsed = parse_sds_file(
                input_val=text,
                source=f"CAS Lookup ({vendor})"
            )
            parsed["source"] = vendor
            results.append(parsed)

        except Exception as e:
            results.append({
                "cas_number": cas,
                "error": str(e),
                "source": vendor
            })

    return results
