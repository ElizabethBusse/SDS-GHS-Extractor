
from parser import streamlit_pdf_upload, parse_sds_file


def sds_upload(pdf_file):
    text = streamlit_pdf_upload(pdf_file)
    return parse_sds_file(input_val=text, source="PDF Upload")


def cas_reader(cas_list):
    try:
        from sds_vendor_fetcher import find_sds_pdf_by_cas
    except Exception as e:
        return {
            "error": "Failed to import sds_vendor_fetcher",
            "details": str(e)
        }

    if not cas_list:
        return {
            "error": "No CAS number provided"
        }

    cas = cas_list[0]

    try:
        vendor_result = find_sds_pdf_by_cas(cas)
    except Exception as e:
        return {
            "cas_number": cas,
            "status": "VENDOR LOOKUP ERROR",
            "error": str(e)
        }

    if vendor_result is None:
        return {
            "cas_number": cas,
            "status": "NOT FOUND",
            "vendor": None,
            "sds_url": None,
            "pdf_byte_size": 0
        }

    try:
        vendor = vendor_result.get("vendor")
        url = vendor_result.get("url")
        pdf_bytes = vendor_result.get("pdf_bytes")
        byte_size = vendor_result.get("byte_size")

        text = streamlit_pdf_upload(pdf_bytes)

        if not text or len(text.strip()) < 50:
            return {
                "cas_number": cas,
                "status": "FOUND",
                "vendor": vendor,
                "sds_url": url,
                "pdf_byte_size": byte_size,
                "parse_status": "PDF DOWNLOADED BUT TEXT EXTRACTION FAILED"
            }

        parsed = parse_sds_file(
            input_val=text,
            source=f"CAS Lookup ({vendor})"
        )

        parsed.update({
            "cas_number": cas,
            "status": "FOUND",
            "vendor": vendor,
            "sds_url": url,
            "pdf_byte_size": byte_size
        })

        return parsed

    except Exception as e:
        return {
            "cas_number": cas,
            "status": "PARSER ERROR",
            "error": str(e)
        }
