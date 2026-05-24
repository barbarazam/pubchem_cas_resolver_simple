# v3 reads chemical names from a CSV file instead of one hardcoded name
# problem: v2 only works for one chemical at a time

import csv
import re
import requests
import time



def fetch(url):
    for attempt in range(1, 4):
        try:
            response = requests.get(url, timeout=10)
            time.sleep(0.25)
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


# open the CSV and call get_cas_number for each row
file   = open("input/batch_1.csv", newline="", encoding="utf-8")
reader = csv.DictReader(file)
for row in reader:
    get_cas_number(row["Name"])
file.close()
