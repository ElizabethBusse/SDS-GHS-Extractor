
# two options: SDS upload or CAS search
# collect all data that will be displayed onto streamlit UI

from sds_vendor_fetcher import find_sds_pdf_by_cas
from parser import streamlit_pdf_upload
from test_parser import run_parser


def sds_upload(pdf_file):
    """
    Handles direct PDF uploads (THIS PATH IS UNCHANGED).
    """
    text = streamlit_pdf_upload(pdf_file)
    results = run_parser(input_val=text)
    return results


def cas_reader(cas_list):
    """
    Handles CAS input:
    - Searches AaronChem first
    - Then Millipore-Sigma / Sigma-Aldrich
    - Downloads ONE SDS PDF
    - Feeds it into the SAME PDF pipeline as uploads
    """

    results = []

    for cas in cas_list:
        pdf_bytes, source = find_sds_pdf_by_cas(cas)

        if pdf_bytes:
            # ✅ Reuse the EXACT same working PDF logic
            result = sds_upload(pdf_bytes)
            result["source"] = source
            results.append(result)
        else:
            # ❌ Explicit, user-visible error
            results.append({
                "cas_number": cas,
                "source": "CAS Search",
                "notes": [
                    "SDS does not exist in AaronChem or Millipore-Sigma"
                ],
                "ghs_from_sds": [],
                "ghs_categories": None,
                "nfpa": None,
            })

    return results


if __name__ == "__main__":
    # Simple manual test
    cas_list = ['64-19-7', '1015484-22-6', '000-00-0']
    results = cas_reader(cas_list)
    print(results)
