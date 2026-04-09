
def cas_reader(cas_list):
    """
    CAS-based SDS lookup with explicit vendor transparency.
    """
    results = []

    for cas in cas_list:
        vendor_result = find_sds_pdf_by_cas(cas)

        if vendor_result is None:
            results.append({
                "cas_number": cas,
                "status": "NOT FOUND",
                "vendor": None,
                "sds_url": None,
                "pdf_bytes": 0
            })
            continue

        # ✅ Explicit visibility
        vendor = vendor_result["vendor"]
        url = vendor_result["url"]
        pdf_bytes = vendor_result["pdf_bytes"]
        byte_size = vendor_result["byte_size"]

        # Surface raw fetch info FIRST
        diagnostic = {
            "cas_number": cas,
            "status": "FOUND",
            "vendor": vendor,
            "sds_url": url,
            "pdf_byte_size": byte_size
        }

        # Attempt parsing
        try:
            text = streamlit_pdf_upload(pdf_bytes)

            if not text or len(text.strip()) < 50:
                diagnostic["parse_status"] = "PDF DOWNLOADED BUT TEXT EXTRACTION FAILED"
                results.append(diagnostic)
                continue

            parsed = parse_sds_file(
                input_val=text,
                source=f"CAS Lookup ({vendor})"
            )

            # Merge diagnostic + parsed data
            parsed.update(diagnostic)
            results.append(parsed)

        except Exception as e:
            diagnostic["parse_status"] = f"PARSER ERROR: {e}"
            results.append(diagnostic)

    return results

