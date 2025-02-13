
Extracting Scheme Name and NAV from URL
Problem Statement
You were given a URL (amfiindia.com/spages/NAVAll.txt) containing mutual fund data in a semicolon-separated format (;). The goal was to extract the Scheme Name (Column 4) and Net Asset Value (Column 5) and save the output in a Tab-Separated Values (TSV) file.

Approach
To solve this problem, I considered the following key points:

Handling URL Data
Used curl to fetch data from the URL (curl -s "$URL") to ensure minimal output clutter.
Skipping Headers
The first row contains headers, so it needed to be skipped.
Extracting Specific Columns
The data is semicolon-separated (;), so we need to extract Column 4 (Scheme Name) and Column 5 (NAV).
Ensuring Portability
Commands like cut behave differently in BSD/macOS vs. Linux, so I opted for awk, which is more portable and flexible.
Final Solution (Using awk)
sh
Copy
Edit
#!/bin/bash

URL="https://www.amfiindia.com/spages/NAVAll.txt"
OUTPUT_FILE="nav_data.tsv"

# Fetch data, skip header, extract Scheme Name & NAV, save as TSV
curl -s "$URL" | awk -F';' 'NR>1 {print $4 "\t" $5}' > "$OUTPUT_FILE"

echo "Extracted data saved to $OUTPUT_FILE"
Why I Chose This Approach?
1️⃣ curl for Fetching Data
curl -s "$URL"
Fetches data silently (-s suppresses unnecessary output).
Works cross-platform on Linux/macOS.
2️⃣ awk for Text Processing
awk -F';' 'NR>1 {print $4 "\t" $5}'
-F';' sets the delimiter to semicolon (;).
NR>1 skips the first row (header).
print $4 "\t" $5 extracts Scheme Name & NAV, separated by a tab (\t).
More portable than cut, which behaves differently on BSD/macOS.
3️⃣ TSV Format for Better Readability
Output is stored as a TSV file (.tsv), which is better for structured data than CSV.
