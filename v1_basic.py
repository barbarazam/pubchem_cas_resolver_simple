import re
import requests



def get_cas_number(chemical_name):

    # ask PubChem for the compound ID of this name
    url      = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/cids/TXT"
    response = requests.get(url)

    if response.status_code == 404:
        print(chemical_name, "-> not found")
        return

    cid = response.text.strip()

    # get all synonyms for that compound ID
    url      = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/TXT"
    response = requests.get(url)

    synonyms = response.text.strip().split("\n")

    # CAS numbers look like 67-64-1 or 1319-77-3
    for synonym in synonyms:
        if re.match(r"^\d{2,7}-\d{2}-\d$", synonym):
            print(chemical_name, "-> found:", synonym)
            return

    print(chemical_name, "-> found in PubChem but no CAS registered")


get_cas_number("Acetone")
