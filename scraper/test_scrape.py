import requests

SERVERS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass-api.de/api/interpreter",
]
HEADERS = {"User-Agent": "business-dashboard-assignment/1.0"}

city = "Kochi"
lat, lon = 9.9312, 76.2673

query = f"""
[out:json][timeout:60];
(
  nwr["amenity"="restaurant"](around:5000,{lat},{lon});
  nwr["amenity"="pharmacy"](around:5000,{lat},{lon});
  nwr["amenity"="bank"](around:5000,{lat},{lon});
  nwr["amenity"="cafe"](around:5000,{lat},{lon});
);
out center tags;
"""

elements = None

for server in SERVERS:
    print("Trying:", server)
    try:
        response = requests.post(server, data={"data": query}, headers=HEADERS, timeout=90)
        print("Status code:", response.status_code)
        if response.status_code == 200:
            elements = response.json()["elements"]
            break
    except Exception as error:
        print("Failed:", error)

if elements is None:
    print("All servers failed. Wait a few minutes and try again.")
else:
    print("Total results:", len(elements))
    for item in elements[:5]:
        tags = item["tags"]
        print(tags.get("name"), "|", tags.get("amenity"), "|", tags.get("phone"))