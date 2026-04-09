
"""
streamlit_pdf_conv.py

This module provides two ingestion paths for the Streamlit app:
1️⃣ Direct SDS PDF upload (WORKING PATH – unchanged)
2️⃣ CAS-based SDS lookup via AaronChem / Millipore-Sigma (FIXED PATH)

CRITICAL DESIGN RULE:
- Both paths MUST use the same downstream parser pipeline.
"""

# ✅ Import ONLY stable, cloud-safe modules
from parser import streamlit_pdf_upload, run_parser
from sds_vendor_fetcher import find_sds_pdf_by_cas


def sds_upload(pdf_file):
    """
    Handles direct user-uploaded SDS PDFs.

    This function is intentionally unchanged because it already works.
    """
    text = streamlit_pdf_upload(pdf_file)
    results = run_parser(input_val=text, source="PDF Upload")
    return results


def cas_reader(cas_list):
    """
    CAS-based SDS reader.

    For each CAS:
    - Search AaronChem and Millipore-Sigma
    - Download SDS PDF
    - Send PDF bytes through the SAME pipeline as manual upload
    """

    results = []

    for cas in cas_list:
        pdf_bytes, vendor = find_sds_pdf_by_cas(cas)

        # ❌ SDS not found for this CAS
        if pdf_bytes is None:
            results.append({
                "cas_number": cas,
                "error": "SDS not found from AaronChem or Millipore-Sigma",
                "source": None
            })
            continue

        try:
            # ✅ IDENTICAL processing path to manual PDF upload
            text = streamlit_pdf_upload(pdf_bytes)
            parsed = run_parser(input_val=text, source=f"CAS Lookup ({vendor})")

            parsed["source"] = vendor
            results.append(parsed)

        except Exception as e:
            results.append({
                "cas_number": cas,
                "error": f"Failed to process SDS: {e}",
                "source": vendor
            })

    return results


