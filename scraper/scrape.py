import time
import requests
import pandas as pd

SERVERS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass-api.de/api/interpreter",
]
HEADERS = {"User-Agent": "business-dashboard-assignment/1.0"}

CITIES = {
    "Kochi": (9.9312, 76.2673),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Hyderabad": (17.3850, 78.4867),
}

CATEGORY_NAMES = {
    "restaurant": "Restaurant",
    "pharmacy": "Pharmacy",
    "bank": "Bank",
    "cafe": "Cafe",
    "hospital": "Hospital",
    "school": "School",
}

MAX_PER_CITY = 150


def fetch_city(lat, lon):
    query = f"""
    [out:json][timeout:60];
    nwr["amenity"~"^(restaurant|pharmacy|bank|cafe|hospital|school)$"]["name"](around:4000,{lat},{lon});
    out center tags;
    """
    for server in SERVERS:
        try:
            response = requests.post(server, data={"data": query}, headers=HEADERS, timeout=90)
            if response.status_code == 200:
                return response.json()["elements"]
            print("  Server busy, status", response.status_code)
        except Exception as error:
            print("  Failed:", error)
        time.sleep(5)
    return []


def build_address(tags, city):
    parts = [
        tags.get("addr:housenumber"),
        tags.get("addr:street"),
        tags.get("addr:suburb"),
        tags.get("addr:postcode"),
    ]
    parts = [p for p in parts if p]
    if parts:
        return ", ".join(parts) + ", " + city
    return "Address not available, " + city


rows = []

for city, (lat, lon) in CITIES.items():
    print("Fetching", city, "...")
    elements = fetch_city(lat, lon)
    print("  Raw results:", len(elements))

    city_rows = []
    for item in elements:
        tags = item.get("tags", {})
        name = tags.get("name")
        if not name:
            continue
        city_rows.append({
            "business_name": name.strip(),
            "category": CATEGORY_NAMES.get(tags.get("amenity"), "Other"),
            "city": city,
            "address": build_address(tags, city),
            "phone": tags.get("phone") or tags.get("contact:phone"),
            "source": "OpenStreetMap",
        })

    city_df = pd.DataFrame(city_rows)
    if not city_df.empty:
        city_df = city_df.drop_duplicates(subset=["business_name", "address"])
        city_df = city_df.head(MAX_PER_CITY)
        rows.append(city_df)
    print("  Kept:", len(city_df))
    time.sleep(10)

if rows:
    final = pd.concat(rows, ignore_index=True)
    final.to_csv("scraper/data.csv", index=False)
    print("Saved scraper/data.csv")
    print("Total rows:", len(final))
    print(final["city"].value_counts())
    print(final["category"].value_counts())
else:
    print("No data collected. Wait a few minutes and run again.")