
# two options: SDS upload or CAS search
# collect all data that will be displayed onto streamlit UI

from sds_vendor_fetcher import find_sds_pdf_by_cas
from parser import streamlit_pdf_upload
from test_parser import run_parser


def sds_upload(pdf_file):
    """
    Handles direct PDF uploads.
    This function is UNCHANGED and already works.
    """
    text = streamlit_pdf_upload(pdf_file)
    return run_parser(input_val=text)


def looks_like_sds(text: str) -> bool:
    """
    Minimal SDS sanity check to avoid parsing non-SDS PDFs
    (catalogs, specs, CoA, marketing sheets, etc.)
    """
    if not text:
        return False

    required_phrases = [
        "safety data sheet",
        "hazards identification",
        "composition",
        "first aid",
    ]

    text_lower = text.lower()
    matches = sum(phrase in text_lower for phrase in required_phrases)
    return matches >= 2


def cas_reader(cas_list):
    """
    CAS workflow:
    - Try AaronChem first
    - Then Millipore-Sigma / Sigma-Aldrich
    - Download ONE PDF
    - Feed it through the SAME pipeline as PDF uploads
    """

    results = []

    for cas in cas_list:
        pdf_bytes, source = find_sds_pdf_by_cas(cas)

        if not pdf_bytes:
            results.append({
                "cas_number": cas,
                "chemical_name": None,
                "cid": None,
                "ghs_from_sds": [],
                "ghs_categories": None,
                "nfpa": None,
                "additional_cas": None,
                "notes": [
                    "SDS does not exist in AaronChem or Millipore-Sigma"
                ],
                "source": "CAS Search",
            })
            continue

        text = streamlit_pdf_upload(pdf_bytes)

        if not text:
            results.append({
                "cas_number": cas,
                "chemical_name": None,
                "cid": None,
                "ghs_from_sds": [],
                "ghs_categories": None,
                "nfpa": None,
                "additional_cas": None,
                "notes": [
                    "Downloaded PDF could not be read"
                ],
                "source": source,
            })
            continue

        result = run_parser(input_val=text)
        result["source"] = source

        # ✅ ensure Streamlit always renders something
        if not result.get("cas_number"):
            result["cas_number"] = cas

        results.append(result)

    return results


if __name__ == "__main__":
    cas_list = ["64-19-7", "7732-18-5", "000-00-0"]
    parsed = cas_reader(cas_list)
    for r in parsed:
        print(r.get("cas_number"), r.get("source"))
