
#!/bin/bash

# URL of the data source
URL="https://www.amfiindia.com/spages/NAVAll.txt"

# Output file
OUTPUT_FILE="output_data.tsv"

# Fetch data, extract Scheme Name and Asset Value, and save to a TSV file
curl -s "$URL" | awk -F ';' 'NR>1 {print $4 "\t" $5}'>"$OUTPUT_FILE"   
#using awk command line 
echo "Extracted data saved to $OUTPUT_FILE"
