import requests

def extract_nfpa_hazard(cid):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"
    response = requests.get(url)
    data = response.json()

    nfpa_section = None
    for section in data["Record"]["Section"]:
        if section["TOCHeading"] == "Safety and Hazards":
            for subsection in section.get("Section", []):
                if subsection["TOCHeading"] == "Hazards Identification":
                    for subsubsection in subsection.get("Section", []):
                        if subsubsection["TOCHeading"] == "NFPA Hazard Classification":
                            nfpa_section = subsubsection
                            break
            break

    if not nfpa_section:
        return None

    result = {
        "Health": None,
        "Flammability": None,
        "Instability": None,
        "Special": None,
        "name": None
    }

    for info in nfpa_section["Information"]:
        name = info.get("Name", "")
        value = info["Value"]["StringWithMarkup"][0]["String"].strip()

        if "Health" in name:
            result["Health"] = {
                "value_html": value[0],
                "description": value[2:].strip()
            }
        elif "Fire" in name:
            result["Flammability"] = {
                "value_html": value[0],
                "description": value[2:].strip()
            }
        elif "Instability" in name:
            result["Instability"] = {
                "value_html": value[0],
                "description": value[2:].strip()
            }
        elif "Special" in name:
            result["Special"] = {
            "value_html": value[0] if value else None,
            "description": value[2:].strip() if len(value) > 2 else ""
            }

        # Remove leading dash from descriptions
        for key in ["Health", "Flammability", "Instability"]:
            if result[key] and result[key]["description"].startswith("-"):
                result[key]["description"] = result[key]["description"][1:].strip()

        # Handle Special if None
        if result["Special"] is None:
            result["Special"] = {
                "value_html": None,
                "description": ""
            }

    print(result)

    return result if any(v for v in result.values()) else None


if __name__ == "__main__":
    extract_nfpa_hazard(22985)