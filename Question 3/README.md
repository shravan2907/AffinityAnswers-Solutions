# **Extracting Scheme Name and NAV from URL**

## **Overview**
This document explains the approach taken to extract **Scheme Name** and **Net Asset Value (NAV)** from a structured text file available at `amfiindia.com/spages/NAVAll.txt`. The extracted data is saved in a **Tab-Separated Values (TSV) file** for further use.

## **Problem Statement**
The task requires:
- Fetching data from a given URL.
- Extracting only **Scheme Name (Column 4)** and **NAV (Column 5)**.
- Removing unnecessary headers.
- Ensuring the solution is **portable** across different Unix-like systems.

## **Approach**
To address the problem efficiently, the following considerations were made:

### **1️⃣ Fetching Data from URL**
- The command-line tool `curl` is used to retrieve the content of the file from the URL.
- The `-s` flag ensures silent execution without unnecessary logs.

### **2️⃣ Skipping the Header Row**
- The first row contains column headers, which are **not needed** in the extracted output.
- The `awk` utility is used to **skip the first row** dynamically.

### **3️⃣ Extracting Specific Fields**
- The data in the file is separated by semicolons (`;`), requiring **a field-based extraction approach**.
- `awk` is chosen over `cut` due to better portability between **Linux and macOS**.

### **4️⃣ Formatting the Output as TSV**
- The extracted fields are separated by a **tab (`\t`)**, making the output suitable for structured data analysis.
- The output is saved in a `.tsv` file.

## **Why This Approach?**
| Feature                | Chosen Solution (`awk`)   | Alternative (`cut`) |
|------------------------|-------------------------|---------------------|
| **Field Extraction**   | ✅ Yes (via `-F';'`)    | ✅ Yes (via `-d';'`) |
| **Skipping Header**    | ✅ Yes (`NR>1`)         | ❌ No (requires `tail`) |
| **Cross-Platform**     | ✅ Yes (Linux & macOS)  | ❌ No (BSD `cut` differs) |
| **Formatting (TSV)**   | ✅ Yes (`"\t"` separator) | ❌ No (`cut` lacks `--output-delimiter`) |

## **Challenges & Considerations**
- **BSD vs GNU Tool Differences**: Some Unix commands behave differently on **macOS (BSD)** and **Linux (GNU)**.
- **Alternative Methods**: Using `sed` could work but adds unnecessary complexity.
- **Error Handling**: The script can be extended to check **network availability** before executing.

## **Possible Enhancements**
1. **Improved Error Handling**: Adding validation to ensure that the URL is reachable before execution.
2. **Cross-Platform Compatibility for Windows**:
   - Using **Git Bash** with a `.bat` wrapper.
   - Converting `.sh` to `.exe` using `shc` or PowerShell scripts.

For implementation details, refer to the script file.
