import random

import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000/listings/bulk"

random.seed(42)

cities = ["Kochi", "Bangalore", "Chennai", "Mumbai", "Delhi", "Hyderabad"]
categories = ["Restaurant", "Pharmacy", "Bank", "Cafe", "Hospital", "School"]

rows = []
for i in range(1, 101):
    city = random.choice(cities)
    category = random.choice(categories)
    rows.append({
        "business_name": f"Sample {category} {i}",
        "category": category,
        "city": city,
        "address": f"Sample address {i}, {city}",
        "phone": "9" + "".join(str(random.randint(0, 9)) for _ in range(9)),
        "source": "Sample Data",
    })

pd.DataFrame(rows).to_csv("scraper/sample_data.csv", index=False)

response = requests.post(API_URL, json=rows, timeout=60)
print(response.status_code, response.text)