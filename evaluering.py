import json
from rapidfuzz import fuzz
import os.path
import random

FETCH = False

START_DATE = "01/01/2022"
END_DATE = "01/01/2030"

FILES = [
    "KBU Forløb - Sommeren 2022 - Runde 29.json",
    "KBU Forløb - Vinter 2022_2023 - Runde 30.json",
    "KBU Forløb - Sommeren 2023 - Runde 31.json",
    "KBU Forløb - Vinter 2023_2024 - Runde 32.json",
]


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


def alle_afdelinger(inactive = False):
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
            "includeInactive": inactive,
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


def kbu_evalueringer_for_uddannelsessteder(uddannelsesstedIds, inactive = False):
    import requests
    import json

    url = "https://uddannelseslaege-api-prod.azurewebsites.net/api/EvalueringStatistikPublic/GetEvalueringsstatistik/"

    payload = json.dumps(
        {
            "startDato": "01/01/2022",
            "slutDato": "01/01/2026",
            "specialeIds": [],
            "uddannelsestyper": [1],
            "includeInactive": inactive,
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


# Målet er at finde uddannelsesstedId for hvert enhed:afdeling par, der optræder i KBU forløb filerne
# Løgn: Sygehus navnene er et 1-til-1 match med "enhed" navnene (i hvert fald case-insensitive)
# Uddannelsesstednavn fra "afdeling" navn skal være manuelt verificeret (med fuzzy matching som hjælp)

# Eksempel:
# {"enhed": "Aarhus Universitetshospital", "sygehusNavn": "Aarhus Universitetshospital", ("sygehusId": ""61bd65fb-d324-4fbb-b8ae-adbca6d3e746",) "afdeling": "Lungesygdomme", "uddannelsesstedNavn": "Lungesygdomme", "uddannelsesstedId": "36d4d506-bece-42f1-bd8e-d593b9fb78e2"}

afdelinger = None
if os.path.exists("afdelinger.json"):
    with open("afdelinger.json") as temp:
        afdelinger = json.load(temp)
else:
    afdelinger = alle_afdelinger(True)
    with open("afdelinger.json", "w") as temp:
        json.dump(afdelinger, temp, ensure_ascii=False)

alle_kbu_evalueringer = None
if os.path.exists("alle-kbu-evalueringer.json"):
    with open("alle-kbu-evalueringer.json") as temp:
        alle_kbu_evalueringer = json.load(temp)
else:
    alle_afdelinger_ids = [a["id"] for a in afdelinger]
    alle_kbu_evalueringer = kbu_evalueringer_for_uddannelsessteder(alle_afdelinger_ids)

    with open("alle-kbu-evalueringer.json", "w") as temp:
        json.dump(alle_kbu_evalueringer, temp, ensure_ascii=False)

enhed_afdelinger = unikke_enhed_afdelinger()

evalueringer = []
if os.path.exists("evalueringer.json"):
    with open("evalueringer.json") as temp:
        evalueringer = json.load(temp)

# clean up evalueringer
if False:
    no_duplicates = []

    for e in evalueringer:
        is_duplicate = next((x for x in no_duplicates if e["enhed"] == x["enhed"] and e["afdeling"] == x["afdeling"]), None) is not None
        if not is_duplicate:
            no_duplicates.append(e)

    print(len(evalueringer))
    print(len(no_duplicates))

    with open("evalueringer.json", "w") as temp:
        json.dump(no_duplicates, temp, ensure_ascii=False)


def missing():
    return [x for x in enhed_afdelinger if len([y for y in evalueringer if y["enhed"] == x.enhed and y["afdeling"] == x.afdeling]) == 0 or len([y for y in evalueringer if y["enhed"] == x.enhed and y["afdeling"] == x.afdeling and y["evaluering"] is None]) > 0]

while len(missing()) > 0    :
    for ea in random.choices(missing()):
        possibilities = []
        for sygehus in set([x["sygehusNavn"] for x in alle_kbu_evalueringer]):
            for uddannelsessted in set(
                [
                    x["uddannelsesstedNavn"]
                    for x in alle_kbu_evalueringer
                    if x["sygehusNavn"] == sygehus
                ]
            ):
                possibilities.append(
                    (
                        uddannelsessted,
                        sygehus,
                        (
                            fuzz.WRatio(ea.enhed, sygehus)
                            + fuzz.WRatio(ea.afdeling, uddannelsessted)
                        )
                        / 2,
                    )
                )
        sortedPossibilities = sorted(possibilities, key=lambda x: x[2], reverse=True)
        i = 0
        sortedPossibilities.reverse()
        for sp in sortedPossibilities:
            print(len(sortedPossibilities) - i - 1, sp[0], sp[1])
            i += 1
        print()
        print(ea.afdeling, ea.enhed)
        choice = input("> ")
        if not choice:
            print("Ingen evalueringer fundet for", ea.afdeling, ea.enhed)
            match = None
        else:
            temp = sortedPossibilities[len(sortedPossibilities) - int(choice) - 1]
            match = next(
                x
                for x in alle_kbu_evalueringer
                if x["uddannelsesstedNavn"] == temp[0] and x["sygehusNavn"] == temp[1]
            )

        afdeling_uddannelsessted = {
            "enhed": ea.enhed,
            "afdeling": ea.afdeling,
            "evaluering": match,
        }

        print(afdeling_uddannelsessted)
        print()
        evalueringer = [x for x in evalueringer if not (x["enhed"] == ea.enhed and x["afdeling"] == ea.afdeling)]
        evalueringer.append(afdeling_uddannelsessted)

    with open("evalueringer.json", "w") as temp:
        json.dump(evalueringer, temp, ensure_ascii=False)

    print("Progress", f"{len(enhed_afdelinger) - len(missing())}/{len(enhed_afdelinger)}")