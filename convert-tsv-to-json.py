import csv
import json

# Exported from Google Sheets as .tsv
FILES = [
    "KBU Forløb - Sommeren 2022 - Runde 29.tsv",
    "KBU Forløb - Vinter 2022_2023 - Runde 30.tsv",
    "KBU Forløb - Sommeren 2023 - Runde 31.tsv",
    "KBU Forløb - Vinter 2023_2024 - Runde 32.tsv",
    "KBU Forløb - Sommeren 2024 - Runde 33.tsv",
    "KBU Forløb - Vinter 2024_2025 - Runde 34.tsv",
]

for filename in FILES:
    results = []
    with open(filename) as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)
        for line in reader:
            results.append({"nummer": int(line[0]), "speciale": line[2], "enhed": line[3], "afdeling": line[4]})

    sortedResults = sorted(results, key=lambda x:int(x["nummer"]))
    with open(filename.replace("tsv", "json"), "w") as file:
        json.dump(sortedResults, file, ensure_ascii=False)