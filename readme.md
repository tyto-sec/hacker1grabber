![Banner](./banner.png)

## HackerOne Scope Extractor

### Description

`hacker1grabber.py` is a specialized Python script that processes one or more CSV files exported from HackerOne's scope page to extract a clean, deduplicated list of in-scope domain identifiers. It's designed to filter out non-target rows and those explicitly marked as "Out of Scope" in the `instruction` field.

### Features

*   **CSV Batch Processing:** Handles all CSV files within a specified input directory.
*   **Scope Filtering:** Only extracts entries where:
    *   `eligible_for_submission` is not explicitly `false`.
*   **Deduplication:** Aggregates and returns a unique list of all identified in-scope identifiers.

### Requirements

This script uses the Python standard library, specifically `csv`, `os`, `sys`, and `glob`. No external libraries are required.

### Usage

The script takes exactly two command-line arguments: the path to the directory containing the CSV files and the path to the desired output file.

```bash
python3 hacker1grabber.py <input_directory> <output_file.txt>
```

#### Example

If you have a directory named `hackerone_reports` with multiple CSV files inside:

```bash
python3 hacker1grabber.py hackerone_reports/ in_scope_targets.txt
```

### Input CSV Format (Assumed)

The script assumes a CSV structure similar to an export from HackerOne, containing at least the following columns:

| Column Name | Description |
| :--- | :--- |
| **`identifier`** | The actual target string (domain, URL, IP). This is the value that is extracted. |
| `eligible_for_submission` | A boolean-like field (e.g., 'true', 'false') indicating if the asset is in scope. |

### Output File Format

The output file will be a plain text file with one unique, sorted identifier per line.

```
# in_scope_targets.txt
6sense.com
api.6sense.com/docs/#introduction
https://6sense.com/platform/sales/signup
```

---

## Domain and IP List Separator/Cleaner

### Description

`clean_domains.py` is a Python utility designed to process a list of mixed entries (URLs, domains, IPs), clean and normalize the domain entries, and then **separate valid domains from valid IP addresses** into two distinct output files. This is particularly useful for quickly categorizing targets from a raw list.

### Features

*   **Domain Normalization:** Removes protocols (`http://`, `https://`), common subdomains (`www.`, `api.`, `*.`), paths, ports, and query parameters from domain entries.
*   **IP Address Extraction:** Identifies and extracts valid IPv4 addresses into a dedicated file.
*   **Domain Filtering:** Ensures that only valid, cleaned domain strings are saved to the primary output file, excluding all extracted IP addresses.
*   **Deduplication:** Both the domain list and the IP address list ensure only unique entries are saved.

### Usage

The script takes exactly two command-line arguments: the path to the input file and the base name for the output files.

```bash
python3 clean_domains.py <input_file.txt> <output_domains.txt>
```

#### Example

```bash
python3 clean_domains.py raw_targets.txt domains.txt
```

If the name of the output domain file is `domains.txt`, the script will generate two files:
1.  **`domains.txt`**: Contains the cleaned and unique domain names.
2.  **`ips_domains.txt`**: Contains the unique IP addresses identified in the input.

### Input File Format

The input file should be a plain text file with one entry (domain, URL, or IP) per line.

```
# raw_targets.txt
https://www.example.com/some/path?q=1
*.subdomain.test.org
192.168.1.1
api.widget.net:8443
mail.another-domain.co.uk
10.0.0.5
```

### Output File Formats

The script generates two files. Both contain unique entries, sorted alphabetically.

**1. Primary Output (`<output_domains.txt>`)**

```
# domains.txt
another-domain.co.uk
example.com
subdomain.test.org
widget.net
```

**2. IP Address Output (`ips_<output_domains.txt>`)**

```
# ips_domains.txt
10.0.0.5
192.168.1.1
```


