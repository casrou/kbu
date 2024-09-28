import csv
import json

FILES = [
    "KBU Forløb - Sommeren 2022 - Runde 29.tsv",
    "KBU Forløb - Vinter 2022_2023 - Runde 30.tsv",
    "KBU Forløb - Sommeren 2023 - Runde 31.tsv",
    "KBU Forløb - Vinter 2023_2024 - Runde 32.tsv",
]

FORMAT = "JSON"
# FORMAT = "CSV"

if (FORMAT == "CSV"):
    results = []
    for filename in FILES:
        with open(filename) as file:
            reader = csv.reader(file, delimiter='\t')
            next(reader)
            for line in reader:
                results.append([line[0], line[2], line[3], line[4]])

    with open("result.csv", "w") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Nummer", "Speciale", "Enhed", "Afdeling"])
        for r in results:
            writer.writerow(r)
else: #JSON
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