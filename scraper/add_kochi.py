import time
import requests
import pandas as pd

SERVERS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass-api.de/api/interpreter",
]
HEADERS = {"User-Agent": "business-dashboard-assignment/1.0"}

CATEGORY_NAMES = {
    "restaurant": "Restaurant",
    "pharmacy": "Pharmacy",
    "bank": "Bank",
    "cafe": "Cafe",
    "hospital": "Hospital",
    "school": "School",
}

city = "Kochi"
lat, lon = 9.9312, 76.2673

query = f"""
[out:json][timeout:60];
nwr["amenity"~"^(restaurant|pharmacy|bank|cafe|hospital|school)$"]["name"](around:6000,{lat},{lon});
out center tags;
"""

elements = []
for attempt in range(3):
    for server in SERVERS:
        try:
            print("Trying", server)
            response = requests.post(server, data={"data": query}, headers=HEADERS, timeout=90)
            if response.status_code == 200:
                elements = response.json()["elements"]
                break
            print("  Status", response.status_code)
        except Exception as error:
            print("  Failed:", error)
        time.sleep(5)
    if elements:
        break
    print("Retrying in 20 seconds...")
    time.sleep(20)

print("Raw results:", len(elements))

rows = []
for item in elements:
    tags = item.get("tags", {})
    name = tags.get("name")
    if not name:
        continue
    parts = [
        tags.get("addr:housenumber"),
        tags.get("addr:street"),
        tags.get("addr:suburb"),
        tags.get("addr:postcode"),
    ]
    parts = [p for p in parts if p]
    if parts:
        address = ", ".join(parts) + ", " + city
    else:
        address = "Address not available, " + city
    rows.append({
        "business_name": name.strip(),
        "category": CATEGORY_NAMES.get(tags.get("amenity"), "Other"),
        "city": city,
        "address": address,
        "phone": tags.get("phone") or tags.get("contact:phone"),
        "source": "OpenStreetMap",
    })

kochi = pd.DataFrame(rows)

if kochi.empty:
    print("No Kochi data. Wait a few minutes and run again.")
else:
    kochi = kochi.drop_duplicates(subset=["business_name", "address"]).head(150)
    old = pd.read_csv("scraper/data.csv")
    old = old[old["city"] != "Kochi"]
    final = pd.concat([old, kochi], ignore_index=True)
    final.to_csv("scraper/data.csv", index=False)
    print("Kochi rows added:", len(kochi))
    print("Total rows now:", len(final))
    print(final["city"].value_counts())