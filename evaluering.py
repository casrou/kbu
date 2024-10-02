import json
import requests
from thefuzz import process
from rapidfuzz import fuzz
import os.path

FETCH = False

START_DATE = "30/09/2023"
END_DATE = "29/09/2024"

FILES = [
    "KBU Forløb - Sommeren 2022 - Runde 29.json",
    "KBU Forløb - Vinter 2022_2023 - Runde 30.json",
    "KBU Forløb - Sommeren 2023 - Runde 31.json",
    "KBU Forløb - Vinter 2023_2024 - Runde 32.json",
]

EVALUERING_FILE = "evaluering.json"


class EnhedAfdeling:
    def __init__(self, enhed, afdeling):
        self.enhed = enhed
        self.afdeling = afdeling

    def __eq__(self, other):
        if not isinstance(other, EnhedAfdeling):
            return False
        return self.enhed == other.enhed and self.afdeling == other.afdeling

    def __hash__(self):
        return hash((self.enhed, self.afdeling))

    def __str__(self):
        return json.dumps(
            {"enhed": self.enhed, "afdeling": self.afdeling}, ensure_ascii=False
        )

    def __repr__(self):
        return self.__str__()


def unikke_enhed_afdelinger():
    enhed_afdelinger = set()
    for f in FILES:
        with open(f) as file:
            elements = json.load(file)
            for e in elements:
                enhed = e["enhed"]
                afdeling = e["afdeling"]
                enhed_afdelinger.add(EnhedAfdeling(enhed, afdeling))
    return list(enhed_afdelinger)


def alle_evaluering_sygehuse():
    url = "https://stamdatakatalog-api-prod.azurewebsites.net/api/Evalueringsstatistik/sygehusForSelect/"

    payload = json.dumps(
        {
            "regionIds": [
                "09f81f66-5166-44fb-a6c7-2bc6d551f1ca",
                "7b004954-ff3e-4469-ab3f-bad145a2ee88",
                "8bcf060f-f28f-405f-ab23-fb51391ca69c",
                "00fc2b0f-9a66-44d9-b45f-c6b638c39cea",
                "7e28dde8-05a1-4ed8-ac8c-90f5d26719f0",
                "4433acdd-e5d9-4588-ba2c-9cda1cea811f",
                "5c799b4a-8a0a-4bea-926e-7dd62393d396",
            ],
            "includeInactive": False,
        }
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://uddannelseslaege.dk/",
        "content-type": "application/json",
        "Origin": "https://uddannelseslaege.dk",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Priority": "u=4",
        "Cookie": "ARRAffinity=6baab673920cdd72d5292ed70f53157373a58e78fa4d23722efa3ae6748c9e7b; ARRAffinitySameSite=6baab673920cdd72d5292ed70f53157373a58e78fa4d23722efa3ae6748c9e7b",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # {
    # "failed": false,
    # "data": [
    #     {
    #         "id": "1c1d0000-0000-0000-0000-000000000000",
    #         "text": "Almen praksis område Vest - almen praksis uspecificeret",
    #         "groupText": null,
    #         "subText": null
    #     },
    # ...
    return json.loads(response.text)["data"]


def alle_evaluering_specialer():
    url = "https://stamdatakatalog-api-prod.azurewebsites.net/api/Evalueringsstatistik/specialerForSelect"

    payload = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://uddannelseslaege.dk/",
        "Origin": "https://uddannelseslaege.dk",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Priority": "u=4",
        "Cookie": "ARRAffinity=6baab673920cdd72d5292ed70f53157373a58e78fa4d23722efa3ae6748c9e7b; ARRAffinitySameSite=6baab673920cdd72d5292ed70f53157373a58e78fa4d23722efa3ae6748c9e7b",
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # {
    # "failed": false,
    # "data": [
    #     {
    #         "id": "e21fd32b-eb14-4069-acbc-352916bbb708",
    #         "text": "Akutmedicin",
    #         "groupText": null,
    #         "subText": null
    #     },
    # ...
    return json.loads(response.text)["data"]


def extractText(x):
    if isinstance(x, dict):
        return x["text"]
    else:
        return x


def alle_afdelinger():
    import requests
    import json

    url = "https://stamdatakatalog-api-prod.azurewebsites.net/api/Evalueringsstatistik/afdelinger/"

    payload = json.dumps(
        {
            "regionIds": [
                "09f81f66-5166-44fb-a6c7-2bc6d551f1ca",
                "7b004954-ff3e-4469-ab3f-bad145a2ee88",
                "8bcf060f-f28f-405f-ab23-fb51391ca69c",
                "00fc2b0f-9a66-44d9-b45f-c6b638c39cea",
                "7e28dde8-05a1-4ed8-ac8c-90f5d26719f0",
                "4433acdd-e5d9-4588-ba2c-9cda1cea811f",
                "5c799b4a-8a0a-4bea-926e-7dd62393d396",
            ],
            "sygehusIds": [],
            "specialeIds": [],
            "includeInactive": False,
        }
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://uddannelseslaege.dk/",
        "content-type": "application/json",
        "Origin": "https://uddannelseslaege.dk",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Priority": "u=4",
        "Cookie": "ARRAffinity=6c5458dd548284d7396cd2cba264e633b6118968d745d1e82e3c3f7fc14794d7; ARRAffinitySameSite=6c5458dd548284d7396cd2cba264e633b6118968d745d1e82e3c3f7fc14794d7",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)["data"]


def afdelinger_fra_sygehus(sygehusId):
    import requests
    import json

    url = "https://stamdatakatalog-api-prod.azurewebsites.net/api/Evalueringsstatistik/afdelinger/"

    payload = json.dumps(
        {
            "regionIds": [
                "09f81f66-5166-44fb-a6c7-2bc6d551f1ca",
                "7b004954-ff3e-4469-ab3f-bad145a2ee88",
                "8bcf060f-f28f-405f-ab23-fb51391ca69c",
                "00fc2b0f-9a66-44d9-b45f-c6b638c39cea",
                "7e28dde8-05a1-4ed8-ac8c-90f5d26719f0",
                "4433acdd-e5d9-4588-ba2c-9cda1cea811f",
                "5c799b4a-8a0a-4bea-926e-7dd62393d396",
            ],
            "sygehusIds": [sygehusId],
            "includeInactive": False,
        }
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://uddannelseslaege.dk/",
        "content-type": "application/json",
        "Origin": "https://uddannelseslaege.dk",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Priority": "u=4",
        "Cookie": "ARRAffinity=6c5458dd548284d7396cd2cba264e633b6118968d745d1e82e3c3f7fc14794d7; ARRAffinitySameSite=6c5458dd548284d7396cd2cba264e633b6118968d745d1e82e3c3f7fc14794d7",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # {
    # "failed": false,
    # "data": [
    #     {
    #         "id": "0e6aafad-cb29-807c-dba2-7cca59f2dbba",
    #         "text": "662030 (Aarhus Universitetshospital)",
    #         "groupText": null,
    #         "subText": null
    #     },
    # ...
    return json.loads(response.text)["data"]


def unikke_enheder():
    enheder = set()
    for f in FILES:
        with open(f) as file:
            elements = json.load(file)
            for e in elements:
                enhed = e["enhed"]
                enheder.add(enhed)
    return enheder


def kbu_evalueringer_for_uddannelsessteder(uddannelsesstedIds):
    import requests
    import json

    url = "https://uddannelseslaege-api-prod.azurewebsites.net/api/EvalueringStatistikPublic/GetEvalueringsstatistik/"

    payload = json.dumps(
        {
            "startDato": "01/01/2022",
            "slutDato": "01/01/2026",
            "specialeIds": [],
            "uddannelsestyper": [1],
            "includeInactive": False,
            "uddannelsesstedIds": uddannelsesstedIds,
        }
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://uddannelseslaege.dk/",
        "content-type": "application/json",
        "Origin": "https://uddannelseslaege.dk",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Priority": "u=0",
        "Cookie": "ARRAffinity=9a4ccea8379f299e8d7188a1e64268fdd53fa391960ddbaf1933188eede43423; ARRAffinitySameSite=9a4ccea8379f299e8d7188a1e64268fdd53fa391960ddbaf1933188eede43423",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # {
    # "data": [
    #     {
    #         "uddannelsesstedId": "2f604602-306b-4b04-a398-be88a1bc4a7c",
    #         "antalForloeb": 62,
    #         "antalForloebEvalueret": 49,
    #         "omraadeNavn": null,
    #         "uddannelsesstedNavn": "HVH, Gastroenheden, kirurgisk",
    #         "antalEvalueringerMedAdgangTil": null,
    #         "antalKommentarer": null,
    #         "sygehusNavn": "Amager og Hvidovre Hospital",
    #         "gruppeScore": [
    #             {
    #                 "svarGruppeEnum": 1,
    #                 "averageScore": 5.1
    #             },
    #             {
    #                 "svarGruppeEnum": 2,
    #                 "averageScore": 5.0
    #             },
    #             {
    #                 "svarGruppeEnum": 3,
    #                 "averageScore": 4.9
    #             },
    #             {
    #                 "svarGruppeEnum": 4,
    #                 "averageScore": 4.9
    #             },
    #             {
    #                 "svarGruppeEnum": 5,
    #                 "averageScore": 4.3
    #             },
    #             {
    #                 "svarGruppeEnum": 6,
    #                 "averageScore": 5.4
    #             },
    #             {
    #                 "svarGruppeEnum": 7,
    #                 "averageScore": 5.4
    #             }
    #         ],
    #         "singleAverageScore": [
    #             5.0,
    #             4.9,
    #             5.2,
    #             5.2,
    #             5.3,
    #             4.6,
    #             4.9,
    #             4.9,
    #             4.8,
    #             4.8,
    #             4.6,
    #             5.2,
    #             5.0,
    #             5.3,
    #             5.3,
    #             4.6,
    #             4.3,
    #             4.1,
    #             4.5,
    #             4.4,
    #             5.2,
    #             5.5,
    #             5.4,
    #             5.6,
    #             5.4,
    #             5.4
    #         ],
    #         "evalueringMedKommentarerIdsMedAdgangTil": null,
    #         "hasAccessToUddannelsessted": false,
    #         "maxAntalEvalueringer": 62,
    #         "antalForloebEvalueretTotal": 49
    #     }
    # ...
    return json.loads(response.text)["data"]


def fuzzy_select(query, processExtracts):
    if len(processExtracts) == 0:
        # If not matches return none
        print("Unknown")
        return None
    # elif processExtracts[0][1] == 100:
    #     # If 100 % match return that
    #     return processExtracts[0][0]
    else:
        print(query, "?")
        # List options and take user input
        i = 0
        for f in processExtracts:
            print(f"\t{i}: {f}")
            i += 1

        choice = input("> ")
        if choice == "break" or choice == "none":
            return None
        elif not choice:
            choice = 0

        return processExtracts[int(choice)][0]


# Målet er at finde uddannelsesstedId for hvert enhed:afdeling par, der optræder i KBU forløb filerne
# Løgn: Sygehus navnene er et 1-til-1 match med "enhed" navnene (i hvert fald case-insensitive)
# Uddannelsesstednavn fra "afdeling" navn skal være manuelt verificeret (med fuzzy matching som hjælp)

# Eksempel:
# {"enhed": "Aarhus Universitetshospital", "sygehusNavn": "Aarhus Universitetshospital", ("sygehusId": ""61bd65fb-d324-4fbb-b8ae-adbca6d3e746",) "afdeling": "Lungesygdomme", "uddannelsesstedNavn": "Lungesygdomme", "uddannelsesstedId": "36d4d506-bece-42f1-bd8e-d593b9fb78e2"}

alle_kbu_evalueringer = None
if os.path.exists("alle-kbu-evalueringer.json"):
    with open("alle-kbu-evalueringer.json") as temp:
        alle_kbu_evalueringer = json.load(temp)
else:
    alle_afdelinger = alle_afdelinger()
    alle_afdelinger_ids = [a["id"] for a in alle_afdelinger]
    alle_kbu_evalueringer = kbu_evalueringer_for_uddannelsessteder(alle_afdelinger_ids)

    with open("alle-kbu-evalueringer.json", "w") as temp:
        json.dump(alle_kbu_evalueringer, temp, ensure_ascii=False)

enhed_afdelinger = unikke_enhed_afdelinger()

alle_sygehuse = alle_evaluering_sygehuse()

enhed_sygehuse = {}
if os.path.exists("enhed_sygehuse.json"):
    with open("enhed_sygehuse.json") as temp:
        enhed_sygehuse = json.load(temp)
else:
    for e in unikke_enheder():
        fuzzySygehus = process.extract(e, set([x["text"] for x in alle_sygehuse]))
        match = fuzzy_select(e, fuzzySygehus)

        chosen_sygehus = [x for x in alle_sygehuse if x["text"] == match][0]
        enhed_sygehus = {
            "sygehus": chosen_sygehus["text"],
            "sygehusId": chosen_sygehus["id"],
        }
        print(e, enhed_sygehus)
        enhed_sygehuse[e] = enhed_sygehus

    with open("enhed_sygehuse.json", "w") as temp:
        print(enhed_sygehuse)
        json.dump(enhed_sygehuse, temp, ensure_ascii=False)

afdeling_uddannelsessteder = []
for ea in enhed_afdelinger[1:100]:
    fuzzySygehus = process.extract(
        ea.enhed, set([x["sygehusNavn"] for x in alle_kbu_evalueringer])
    )
    sygehus = fuzzy_select(ea.enhed, fuzzySygehus)

    fuzzyUddannelsessted = process.extract(
        ea.afdeling,
        set([
            x["uddannelsesstedNavn"]
            for x in alle_kbu_evalueringer
            if x["sygehusNavn"] == sygehus
        ]),
        limit=100,
    )
    match = fuzzy_select(f"{ea.afdeling} ({sygehus})", fuzzyUddannelsessted)

    # if len(fuzzyUddannelsessted) == 0:
    #     print("Unknown", ea)
    #     continue
    # elif fuzzyUddannelsessted[0][1] == 100:
    #     match = fuzzyUddannelsessted[0][0]
    # else:
    #     print(ea.afdeling, "?")
    #     i = 0
    #     for f in fuzzyUddannelsessted:
    #         print(f"\t{i}: {f}")
    #         i += 1
    #     choice = input("> ")
    #     if choice == "break":
    #         afdeling_uddannelsessted = {
    #             "enhed": ea.enhed,
    #             "sygehus": enhed_sygehuse[ea.enhed],
    #             "afdeling": ea.afdeling,
    #         }
    #         print(afdeling_uddannelsessted)
    #         print()
    #         afdeling_uddannelsessteder.append(afdeling_uddannelsessted)
    #         break
    #     elif not choice:
    #         choice = 0
    #     match = fuzzyUddannelsessted[int(choice)][0]
    chosen_uddannelsessted = next(
        (x for x in alle_kbu_evalueringer if x["uddannelsesstedNavn"] == match),
        {"uddannelsesstedNavn": None, "uddannelsesstedId": None},
    )
    afdeling_uddannelsessted = {
        "enhed": ea.enhed,
        "sygehus": enhed_sygehuse[ea.enhed],
        "afdeling": ea.afdeling,
        "uddannelsesstedNavn": chosen_uddannelsessted["uddannelsesstedNavn"],
        "uddannelsesstedId": chosen_uddannelsessted["uddannelsesstedId"],
    }

    print(afdeling_uddannelsessted)
    print()
    afdeling_uddannelsessteder.append(afdeling_uddannelsessted)

with open("afdeling_uddannelsessteder.json", "w") as temp:
    json.dump(afdeling_uddannelsessteder, temp, ensure_ascii=False)
