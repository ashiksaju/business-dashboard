import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000/listings/bulk"


def clean_phone(value):
    if value is None:
        return None
    first = str(value).split(";")[0].split(",")[0].strip()
    return first[:50] or None


df = pd.read_csv("scraper/data.csv")
df = df.astype(object).where(df.notna(), None)

records = df.to_dict(orient="records")
for record in records:
    record["phone"] = clean_phone(record["phone"])

print("Rows to upload:", len(records))

batch_size = 200
for start in range(0, len(records), batch_size):
    batch = records[start:start + batch_size]
    response = requests.post(API_URL, json=batch, timeout=60)
    print("Batch", start // batch_size + 1, "->", response.status_code, response.text)

print("Done")