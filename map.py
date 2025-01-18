import urllib.parse

# Assuming `address` is fetched from the database
address = "313 4th St SW, Willmar, MN 56201, USA"

# URL-encode the address
encoded_address = urllib.parse.quote(address)

# Create the Google Maps URL
google_maps_url = f"https://www.google.com/maps?q={encoded_address}"

# Use this URL in the iframe
iframe_html = f"""
<iframe
    src="https://www.google.com/maps?q={encoded_address}&output=embed"
    width="100%" height="300" style="border:0;" allowfullscreen=""
    loading="lazy"></iframe>
"""
print(iframe_html)
