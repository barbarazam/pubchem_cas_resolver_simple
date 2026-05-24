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

All original columns are preserved. Two columns are added at the end.

```
Name,"Quantity, kg",cas,status
Example:
Acetone,850,67-64-1,found
Soy flour (defatted),1500,,not_found
```

---

## Versions

The repository includes `v1` through `v6` showing the development steps. The final version is `pubchem_cas_resolver_simple.py`.

---
## Notes

- Respects PubChem's rate limit of 5 requests per second
- Retries up to 3 times on network errors
- Uses the [PubChem public REST API](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)
