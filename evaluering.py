import json
import requests
from thefuzz import process
from rapidfuzz import fuzz


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


def main():
    evalueringData = None
    if FETCH:
        url = "https://uddannelseslaege-api-prod.azurewebsites.net/api/EvalueringStatistikPublic/GetEvalueringsstatistik/"

        payload = json.dumps(
            {
                "startDato": START_DATE,
                "slutDato": END_DATE,
                "specialeIds": [],
                "uddannelsestyper": [1],  # KBU
                "includeInactive": True,
                "uddannelsesstedIds": [
                    "1c1d0000-0000-0000-0000-000000000000",
                    "d11d0000-0000-0000-0000-000000000000",
                    "4b9371aa-d997-4833-bc9c-938368e877da",
                    "53af5dce-d5fc-48cb-aa5f-3d638d8d3e1c",
                    "163eefcd-6b26-4355-8d53-8f0216524d68",
                    "734ecced-a961-48f3-879b-1ff4cb50adcb",
                    "f64fb1f3-7d7d-44a7-b00b-0dc68f92b2ac",
                    "b01e0000-0000-0000-0000-000000000000",
                    "7c5ff544-0aaf-45d6-a3b4-43e56ae230aa",
                    "181e0000-0000-0000-0000-000000000000",
                    "4dac6b48-8236-4517-9a5a-d008a2a2047f",
                    "9d030000-0000-0000-0000-000000000000",
                    "bfa0b40a-d0c1-46a3-aff4-da88ec56b56f",
                    "d050faa8-1015-4282-af09-e96b3a696a69",
                    "f8435af6-7b9c-4e1f-ae3e-cbf2a86af980",
                    "9f3a53da-59e4-4f9d-a3a2-32a3085dda58",
                    "acbba8ca-4e1b-451a-8992-3b6275eeafa0",
                    "200b72a6-a188-434c-9c8a-a284a330d3c7",
                    "4b6fc5af-57ca-4853-9325-98a272918c29",
                    "dfe50ee6-e5bd-4b1a-90f8-05379680b1b7",
                    "bcf4e1c3-ffe4-4b97-be2c-9da3dd2352ec",
                    "678fe107-bea7-49a7-9b5d-4e211cd6df54",
                    "de117b22-0ee5-4d39-9632-2135a1c6214a",
                    "d841ce69-2313-4478-94ae-b35224260d8b",
                    "7dc6b320-93a5-40d6-aa84-b97e23cfe7d9",
                    "603527af-4749-4cf9-8747-3fcf415e3148",
                    "6df4a2a2-c853-4c9f-8773-20c514db2430",
                    "52733a30-b9a4-4951-a441-21c2cd3580b4",
                    "7e060000-0000-0000-0000-000000000000",
                    "df2f5ded-114b-4ca0-989a-d1ddf86023cb",
                    "3c36b012-24da-4091-a066-858a69aeb6d1",
                    "e7f0a202-7b13-4fd8-b43f-52f77c8d5c2f",
                    "78fab35e-70d0-49ea-add8-904bcd6c0da9",
                    "1c8be318-0805-462a-b8fb-b3fba062cdda",
                    "04a6d334-6f6f-494e-a30f-f49d21b21d96",
                    "3e3a72cc-69c1-4c4b-a0f2-3a97a9e05b0f",
                    "0005594f-3f63-4479-9be0-c3dfd9651711",
                    "df5320d5-a207-4b24-90a9-e74271ddded6",
                    "6116efc5-749e-4cb8-89db-64af0d3aaf13",
                    "a6e5535f-d1ef-4996-962a-3c760af40f22",
                    "d97ca761-92b8-48e6-b084-ed1306eb4cb2",
                    "20442734-3b7d-4dc0-b80e-a6fb9c3ad4f6",
                    "8dfdc617-d7d5-4842-b176-358aa859c12c",
                    "50289e64-59c8-49c7-8cb2-0362a64bf5a8",
                    "29c2b93a-f368-4212-a0b1-36f9f5d00cde",
                    "45892078-9e21-4d52-8dd7-eafe752b1b62",
                    "e983a724-bfc6-4724-b025-68f3c6be49f1",
                    "31d7f8bb-21bf-4ae6-8eab-ad181436013a",
                    "17bc928f-0e21-456f-a18c-e4126ab733b5",
                    "14e37f8c-50d6-44ae-a46b-9b2c85f4b269",
                    "8480d485-d28d-4c5c-926b-5aaac3fc0da5",
                    "9f030000-0000-0000-0000-000000000000",
                    "2dc2ab59-bebb-43ab-a39c-60bb4890c038",
                    "8aa6ec57-9055-44bd-bcb9-f5e5775bdd7c",
                    "800a0c0e-1332-49c6-af44-80aadf85c3e9",
                    "c761ae22-0052-49eb-9fc7-88df31581bd6",
                    "dc7bc093-d15a-480f-b028-b3863a477c00",
                    "af4d426e-d8bf-4542-bf4f-3cbb0ced6cf0",
                    "640c42ce-9d05-49ca-a620-acff2b1f24e7",
                    "b8e03610-8e45-4074-a99f-a163c583fa13",
                    "f9035a0c-bc2a-401a-9198-78eab756efbc",
                    "c7ccdec0-e829-45e3-96a9-59720ad9da16",
                    "32b85c14-8def-45a4-8470-4d53322a2349",
                    "d5ea1438-fed1-45d7-8d7e-8865ec4c54f7",
                    "79060000-0000-0000-0000-000000000000",
                    "7317e9e9-89a5-40f4-8902-73f70fe95517",
                    "70f73e5c-b695-41fd-9f44-9a1e9ac2a009",
                    "a6405efb-ee56-49b6-b222-daf6e6efaf30",
                    "1cafdaf3-bc73-460c-bdfd-80fdc9235045",
                    "5c6a2038-cf9b-4a59-9b13-829e5920ba4b",
                    "44b1f2ab-86b5-4669-9258-76ff20373a86",
                    "3bd50d70-92c2-4c0a-acd0-b2da26c11f2a",
                    "a3c26806-9ee4-4054-a2ef-e75096d29290",
                    "761d0000-0000-0000-0000-000000000000",
                    "f2bf5b6d-68ef-4526-b87e-6860427f1719",
                    "c3093155-4131-4864-9b0c-dae60fa6dab2",
                    "8aa880f4-a661-45b5-b927-d4ea15df71e9",
                    "81080000-0000-0000-0000-000000000000",
                    "414007e5-aa37-4cad-99b7-93c7199ff91d",
                    "ca706fa6-1523-471e-8329-4a5e9ed8e29a",
                    "4dba9a48-b254-4dc0-a535-6d106445d79d",
                    "0165a6d7-e88d-42ad-a65f-fc85e6e6bb2c",
                    "61bd65fb-d324-4fbb-b8ae-adbca6d3e746",
                ],
            }
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
            "Accept": "*/*",
            "content-type": "application/json",
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        with open(EVALUERING_FILE, mode="w") as file:
            json.dump(response.json(), file, ensure_ascii=False)

    with open(EVALUERING_FILE) as file:
        evalueringData = json.load(file)["data"]

    enhed_afdelinger = set()
    for f in FILES:
        with open(f) as file:
            elements = json.load(file)
            for e in elements:
                enhed = e["enhed"]
                afdeling = e["afdeling"]
                enhed_afdelinger.add(EnhedAfdeling(enhed, afdeling))
                # enhed_afdelinger.add(tuple(enhed, afdeling))

    enhed_afdeling_evalueringer = []
    unknown = 0
    with open(EVALUERING_FILE) as file:
        evalueringData = json.load(file)["data"]

        for ea in enhed_afdelinger:
            evaluering = process.extractOne(
                ea.afdeling,
                [
                    x
                    for x in evalueringData
                    if x["sygehusNavn"].casefold() == ea.enhed.casefold()
                ],
                extractUddannelsesstedNavn,
                scorer=fuzz.token_ratio,
            )
            if evaluering:
                enhed_afdeling_evalueringer.append(
                    {
                        "enhed": ea.enhed,
                        "afdeling": ea.afdeling,
                        "evaluering": evaluering[0],
                        "fuzzy_score": evaluering[1],
                    }
                )
            else:
                enhed_afdeling_evalueringer.append(
                    {
                        "enhed": ea.enhed,
                        "afdeling": ea.afdeling,
                        "evaluering": None,
                        "fuzzy_score": -1,
                    }
                )
                unknown += 1

    print("unknown: " + str(unknown))

    with open("evalueringer.json", mode="w") as result_file:
        json.dump(
            sorted(enhed_afdeling_evalueringer, key=lambda x: int(x["fuzzy_score"])),
            fp=result_file,
            ensure_ascii=False,
        )


def extractUddannelsesstedNavn(x):
    if isinstance(x, dict):
        return x["uddannelsesstedNavn"]
    else:
        return x


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


# main()

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

sygehuse_ids = json.loads(response.text)["data"]

url = "https://stamdatakatalog-api-prod.azurewebsites.net/api/Evalueringsstatistik/specialerForSelect"

payload = {}
headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'Referer': 'https://uddannelseslaege.dk/',
  'Origin': 'https://uddannelseslaege.dk',
  'Connection': 'keep-alive',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'cross-site',
  'Priority': 'u=4',
  'Cookie': 'ARRAffinity=6baab673920cdd72d5292ed70f53157373a58e78fa4d23722efa3ae6748c9e7b; ARRAffinitySameSite=6baab673920cdd72d5292ed70f53157373a58e78fa4d23722efa3ae6748c9e7b'
}

response = requests.request("GET", url, headers=headers, data=payload)

specialer_ids = json.loads(response.text)["data"]


def extractText(x):
    if isinstance(x, dict):
        return x["text"]
    else:
        return x


sygehuse = set()
specialer = set()
for f in FILES:
    with open(f) as file:
        elements = json.load(file)
        for e in elements:
            sygehus = e["enhed"]
            # afdeling = e["afdeling"]
            speciale = e["speciale"]

            sygehuse.add(sygehus)
            specialer.add(speciale)

            sygehus_id =  [x for x in sygehuse_ids if sygehus.casefold() in x["text"].casefold()][0]["id"]
            speciale_id = [x["id"] for x in specialer_ids if speciale.casefold() in x["text"].casefold()]

            print()
            # enheder.add(EnhedAfdeling(enhed, afdeling))
            # enhed_afdelinger.add(tuple(enhed, afdeling))

print()
print("START")
for ea in sygehuse:
    sygehus_id = process.extractOne(ea.enhed, sygehuse_ids, extractText, score_cutoff=80)[0]["id"]

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
            "sygehusIds": [sygehus_id],
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

    afdelinger = json.loads(response.text)["data"]

    afdeling_id = process.extractOne(
        ea.afdeling, afdelinger, extractText, score_cutoff=50
    )

    if afdeling_id is None:
        print(
            str(ea)
            + " - "
            + str(process.extractOne(ea.afdeling, afdelinger, extractText))
        )

    # afdeling_id2 = process.extract(f"({ea.afdeling} {ea.enhed})", afdelinger, extractText, scorer=fuzz.token_ratio)
    # afdeling_id3 = process.extract(f"({ea.afdeling} {ea.enhed})", afdelinger, extractText, scorer=fuzz.partial_ratio)
    # afdeling_id4 = process.extract(f"({ea.afdeling} {ea.enhed})", afdelinger, extractText, scorer=fuzz.QRatio)
    # afdeling_id5 = process.extract(f"({ea.afdeling} {ea.enhed})", afdelinger, extractText, scorer=fuzz.ratio)
    # print()
