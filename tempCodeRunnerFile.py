    # if not nfpa_section:
    #     return None

    # result = {
    #     "Health": None,
    #     "Flammability": None,
    #     "Instability": None,
    #     "Special": None
    # }

    # for info in nfpa_section["Information"]:
    #     name = info.get("Name", "")
    #     value = info["Value"]["StringWithMarkup"][0]["String"].strip()

    #     if "Health" in name:
    #         result["Health"] = {
    #             "value_html": value[0],
    #             "description": value[2:].strip()
    #         }
    #     elif "Fire" in name:
    #         result["Flammability"] = {
    #             "value_html": value[0],
    #             "description": value[2:].strip()
    #         }
    #     elif "Instability" in name:
    #         result["Instability"] = {
    #             "value_html": value[0],
    #             "description": value[2:].strip()
    #         }