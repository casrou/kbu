import requests
import json
import csv
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

FILES = [
    "KBU Forløb - Sommeren 2022 - Runde 29.tsv",
    "KBU Forløb - Vinter 2022_2023 - Runde 30.tsv",
    "KBU Forløb - Sommeren 2023 - Runde 31.tsv",
    "KBU Forløb - Vinter 2023_2024 - Runde 32.tsv",
]

enheder = set()
for filename in FILES:
    with open(filename) as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)
        for line in reader:
            enheder.add(line[3])

print(enheder)

url = "https://places.googleapis.com/v1/places:searchText"

headers = {
  'Content-Type': 'application/json',
  'X-Goog-Api-Key': GOOGLE_API_KEY,
  'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.location'
}

locations = []
for e in enheder:
    payload = json.dumps({
    "textQuery": e,
    "includedType": "hospital"
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()

    locations.append({"enhed": e, "result": response_json})

with open("locations.json", "w") as file:
    json.dump(locations, file, ensure_ascii=False, )