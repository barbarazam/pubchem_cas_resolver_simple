# v4 writes results to an output CSV instead of printing them
# problem: printing is not useful, you need a file you can open and share

import csv
import os
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
    # now returns a dict instead of printing, so we can collect results

    # ask PubChem for the compound ID of this name
    url      = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/cids/TXT"
    response = fetch(url)

    if response is None or response.status_code == 404:
        return {"cas": "", "status": "not_found"}

    cid = response.text.strip()

    # get all synonyms for that compound ID
    url      = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/TXT"
    response = fetch(url)

    if response is None:
        return {"cas": "", "status": "not_found"}

    synonyms = response.text.strip().split("\n")

    # CAS numbers look like 67-64-1 or 1319-77-3
    for synonym in synonyms:
        if re.match(r"^\d{2,7}-\d{2}-\d$", synonym):
            return {"cas": synonym, "status": "found"}

    return {"cas": "", "status": "not_found"}


# read input
file    = open("input/batch_1.csv", newline="", encoding="utf-8")
reader  = csv.DictReader(file)
headers = list(reader.fieldnames)  # save original column names

output_rows = []
for row in reader:
    result        = get_cas_number(row["Name"])
    row["cas"]    = result["cas"]
    row["status"] = result["status"]
    print(row["Name"], "->", result["status"], result["cas"])
    output_rows.append(row)
file.close()

# write output — same columns as input plus cas and status
os.makedirs("output", exist_ok=True)

output_file = open("output/batch_1.csv", "w", newline="", encoding="utf-8")
writer      = csv.DictWriter(output_file, fieldnames=headers + ["cas", "status"])
writer.writeheader()
writer.writerows(output_rows)
output_file.close()

print("done. results saved to output/batch_1.csv")
