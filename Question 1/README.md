
# Address Validation Using PIN Code and Fuzzy Matching

## **Problem Statement**
BestDelivery Courier Company is facing an issue where parcels are often assigned incorrect PIN codes, leading to misrouted deliveries. The correct PIN code needs to be verified against the address provided. Instead of just checking the district and state, a better approach is to validate the nearest area name associated with the PIN code. The goal is to implement a system that ensures accurate address validation.

---

## **Solution Approach**
To effectively validate the PIN code, I followed a **systematic approach** that includes:
1. **Extracting the PIN Code** from the given address using regular expressions.
2. **Fetching the list of valid area names** corresponding to the PIN code from the Postal API.
3. **Using fuzzy matching** to compare the extracted address with the list of areas retrieved from the API.
4. **Determining the validity** of the address based on similarity scores.

This method ensures that minor variations in address formatting do not cause incorrect rejections while maintaining high accuracy.

---

## **Technology & Libraries Used**
- **Python**: Chosen for its ease of string manipulation and API handling.
- **Regular Expressions (`re`)**: For extracting the PIN code from the address string.
- **Requests (`requests`)**: To fetch area details from the Postal API.
- **Fuzzy Matching (`thefuzz`)**: To handle slight address variations and improve validation accuracy.

---

## **Step-by-Step Implementation**

### **Step 1: Extracting the PIN Code from the Address**
We use a **regular expression** to extract the 6-digit PIN code:
```python
import re

def extract_pincode(address):
    match = re.search(r"\b\d{6}\b", address)  # Look for a 6-digit number
    return match.group() if match else None
```
- `\b\d{6}\b` ensures that only a **standalone** 6-digit number is extracted (prevents matching substrings within larger numbers).
- If a match is found, it is returned; otherwise, `None` is returned.

### **Step 2: Fetching Area Names for the PIN Code**
We use the **postal API** to fetch the list of areas corresponding to the given PIN code:
```python
import requests

def fetch_pincode_details(pincode):
    url = f"https://api.postalpincode.in/pincode/{pincode}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data and data[0]['Status'] == 'Success':
            return [office["Name"] for office in data[0]['PostOffice']]
    return None
```
- We make an API request using `requests.get()`.
- If the request is successful and returns valid data, we extract **all area names** associated with the PIN code.
- If the response is invalid, we return `None`.

### **Step 3: Using Fuzzy Matching to Validate Address**
We use **fuzzy string matching** to compare the extracted address with the list of valid areas:
```python
from thefuzz import process

def is_address_valid(address):
    pincode = extract_pincode(address)
    if not pincode:
        return False, "No PIN code found in the address."

    valid_areas = fetch_pincode_details(pincode)
    if not valid_areas:
        return False, "Invalid or non-existent PIN code."

    # Perform fuzzy matching to find the best match
    best_match, score = process.extractOne(address, valid_areas) if valid_areas else (None, 0)

    if best_match and score > 80:
        return True, f"Valid address. Closest area match: {best_match}"
    
    return False, "Area name does not match the given pincode. Please check the address."
```
- `process.extractOne()` compares the address against all valid areas and finds the **best match**.
- The **threshold score of 80%** ensures that minor spelling errors do not lead to false rejections.
- If a strong match is found, the address is considered valid; otherwise, we prompt for correction.

---

## **Example Test Cases**

```python
test_addresses = [
    "2nd Phase, 374/B, 80 Feet Rd, Mysore Bank Colony, Banashankari 3rd Stage, Bengaluru, Karnataka 560050",  # ✅ Valid
    "374/B, 80 Feet Rd, Bengaluru, Karnataka 560050",  # ✅ Might be valid (if fuzzy match is strong)
    "2nd Phase, 80 Feet Rd, Mysore Bank Colony, Bengaluru, Karnataka 560095",  # ❌ Wrong pincode
    "Colony, Bengaluru, Karnataka 560050"  # ❌ Too vague
]

for address in test_addresses:
    valid, message = is_address_valid(address)
    print(f"Address: {address}\nResult: {message}\n")
```
- Ensures that the method correctly identifies **valid and invalid addresses**.
- Handles **missing area names**, **misspellings**, and **incorrect PIN codes** effectively.

---

## **Edge Cases Considered**
1. **Completely missing area name** → Should return invalid.
2. **Minor spelling errors** → Should still be valid if the best match is above the threshold.
3. **Multiple valid area names for a PIN** → Uses fuzzy matching to find the best match.
4. **Completely wrong PIN code** → Should return invalid.

---

