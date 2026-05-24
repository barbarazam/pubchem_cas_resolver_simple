# PubChem CAS Resolver

Reads a CSV file with chemical names, looks each one up in the PubChem public API, and writes a new CSV with two added columns: `cas` and `status`.

---

## Setup

Python 3.10 or higher required.

```bash
pip install requests
```

---

## Usage

Put your CSV files in the `input/` folder. Each file needs a column called `Name`.

```bash
python pubchem_cas_resolver_simple.py
```

Custom folders:

```bash
python pubchem_cas_resolver_simple.py --input-dir my_data --output-dir my_results
```

---

## Output

| Name | Quantity | cas | status |
|------|----------|-----|--------|
| Acetone | 850 | 67-64-1 | found |
| Ethanol | 2200 | 64-17-5 | found |
| Unknownchemical | 50 | | not_found |

---

## Notes

- Respects PubChem's rate limit of 5 requests per second
- Retries up to 3 times on network errors
- Uses the [PubChem public REST API](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest) — no account needed
