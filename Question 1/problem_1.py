import requests
import re
from thefuzz import process


def extract_pincode(address):
    """Extracts the 6-digit pincode from the address using regex."""
    match = re.search(r"\b\d{6}\b", address)
    return match.group() if match else None


def fetch_pincode_details(pincode):
    """Fetches area details for the given pincode from the API."""
    url = f"https://api.postalpincode.in/pincode/{pincode}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data and data[0]["Status"] == "Success":
            return [office["Name"] for office in data[0]["PostOffice"]]
    return None


def is_address_valid(address):
    """Validates if the pincode and area name in the address match using fuzzy matching."""
    pincode = extract_pincode(address)
    if not pincode:
        return False, "No PIN code found in the address."

    valid_areas = fetch_pincode_details(pincode)
    if not valid_areas:
        return False, "Invalid or non-existent PIN code."

    # Perform fuzzy matching on area names
    best_match, score = (
        process.extractOne(address, valid_areas) if valid_areas else (None, 0)
    )

    if best_match and score > 80:
        return True, f"Valid address. Closest area match: {best_match}"

    return (
        False,
        "Area name does not match the given pincode. Please check the address.",
    )


# 🔹 Example Test Cases
test_addresses = [
    "2nd Phase, 374/B, 80 Feet Rd, Mysore Bank Colony, Banashankari 3rd Stage, Bengaluru, Karnataka 560050",  # ✅ Should be valid
    "2nd Phase, 80 Feet Rd, Mysore Bank Colony, Bengaluru, Karnataka 560095",  # ❌ Wrong pincode
    "Colony, Bengaluru, Karnataka 560050",  # ❌ Too vague
]

for address in test_addresses:
    valid, message = is_address_valid(address)
    print(f"Address: {address}\nResult: {message}\n")
