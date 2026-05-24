# v2 adds retry logic and rate limiting
# problem: v1 crashes if the connection drops or PubChem is slow

import re
import requests
import time



def fetch(url):
    # try 3 times before giving up
    for attempt in range(1, 4):
        try:
            response = requests.get(url, timeout=10)
            time.sleep(0.25)  # PubChem allows max 5 requests per second
            return response
        except requests.RequestException:
            print(f"request failed (attempt {attempt}/3), retrying...")
            time.sleep(2)
    print("all attempts failed for:", url)
    return None


def get_cas_number(chemical_name):

    # ask PubChem for the compound ID of this name
    url      = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/cids/TXT"
    response = fetch(url)

    if response is None or response.status_code == 404:
        print(chemical_name, "-> not found")
        return

    cid = response.text.strip()

    # get all synonyms for that compound ID
    url      = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/TXT"
    response = fetch(url)

    if response is None:
        print(chemical_name, "-> could not get synonyms")
        return

    synonyms = response.text.strip().split("\n")

    # CAS numbers look like 67-64-1 or 1319-77-3
    for synonym in synonyms:
        if re.match(r"^\d{2,7}-\d{2}-\d$", synonym):
            print(chemical_name, "-> found:", synonym)
            return

    print(chemical_name, "-> found in PubChem but no CAS registered")


get_cas_number("Acetone")
