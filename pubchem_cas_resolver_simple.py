import argparse
import csv
import logging
import os
import re
import requests
import time


logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt = "%H:%M:%S",
)
logger = logging.getLogger(__name__)


def fetch(url):
    # try 3 times before giving up
    for attempt in range(1, 4):
        try:
            response = requests.get(url, timeout=10)
            time.sleep(0.25)  # PubChem allows max 5 requests per second
            return response
        except requests.RequestException:
            logger.warning(f"request failed (attempt {attempt}/3), retrying...")
            time.sleep(2)
    logger.error("all attempts failed for: " + url)
    return None


def get_cas_number(chemical_name):
    # ask PubChem for the compound ID of this name
    url      = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/cids/TXT"
    response = fetch(url)

    if response is None or response.status_code == 404:
        logger.warning(f"{chemical_name} -> not found")
        return {"cas": "", "status": "not_found"}

    cid = response.text.strip()

    # get all synonyms for that compound ID
    url      = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/TXT"
    response = fetch(url)

    if response is None:
        logger.warning(f"{chemical_name} -> could not get synonyms")
        return {"cas": "", "status": "not_found"}

    synonyms = response.text.strip().split("\n")

    # CAS numbers look like 67-64-1 or 1319-77-3
    for synonym in synonyms:
        if re.match(r"^\d{2,7}-\d{2}-\d$", synonym):
            logger.info(f"{chemical_name} -> found: {synonym}")
            return {"cas": synonym, "status": "found"}

    logger.warning(f"{chemical_name} -> found in PubChem but no CAS registered")
    return {"cas": "", "status": "not_found"}


def process_file(input_path, output_dir):
    filename = os.path.basename(input_path)

    file    = open(input_path, newline="", encoding="utf-8")
    reader  = csv.DictReader(file)
    headers = list(reader.fieldnames)

    output_rows = []
    for row in reader:
        result        = get_cas_number(row["Name"])
        row["cas"]    = result["cas"]
        row["status"] = result["status"]
        output_rows.append(row)
    file.close()

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    output_file = open(output_path, "w", newline="", encoding="utf-8")
    writer      = csv.DictWriter(output_file, fieldnames=headers + ["cas", "status"])
    writer.writeheader()
    writer.writerows(output_rows)
    output_file.close()

    logger.info(f"done. results saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Resolve chemical names to CAS numbers using PubChem."
    )
    parser.add_argument("--input-dir",  "-i", default="input",  help="folder with input CSV files")
    parser.add_argument("--output-dir", "-o", default="output", help="folder for output CSV files")
    args = parser.parse_args()

    csv_files = [f for f in os.listdir(args.input_dir) if f.endswith(".csv")]
    for filename in sorted(csv_files):
        logger.info(f"processing: {filename}")
        process_file(os.path.join(args.input_dir, filename), args.output_dir)


if __name__ == "__main__":
    main()
