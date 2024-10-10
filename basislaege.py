import datetime
import os
import requests
import sys
from bs4 import BeautifulSoup
import csv

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        with open(f"basislaege-{datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.html", "w") as temp:
            temp.write(fetch())
            exit(0)
    
    basislaege = None
    if os.path.exists("basislaege.html"):
        with open("basislaege.html") as temp:
            basislaege = temp.read()
    else:
        result = fetch()
        with open("basislaege.html", "w") as temp:
            temp.write(result)
            basislaege = result
    
    print(len(basislaege))  
    soup = BeautifulSoup(basislaege, 'html.parser')
    print("Title of the Page:", soup.title.text)  # Access the title element

    tags = soup.select(".tag")
    print(tags)
    specialer = {}
    sygehuse = {}
    regioner = {}
    for t in tags:
        if t.has_attr("data-specialeid"):
            specialer[t.get("data-specialeid")] = t.select_one("span").text
        elif t.has_attr("data-sygehusid"):
            sygehuse[t.get("data-sygehusid")] = t.select_one("span").text 
        elif t.has_attr("data-regionid"):
            regioner[t.get("data-regionid")] = t.select_one("span").text
    print(specialer)
    print(sygehuse)
    print(regioner)

    print(len(soup.select("div.enkelt-forloeb-div")))

    forloeb = []
    for d in soup.select("div.enkelt-forloeb-div"):
        print(d['data-searchable'])
        region = d['data-region']
        sygehus = d['data-sygehus']
        speciale = d['data-speciale']
        speciale2 = d['data-speciale2']
        status = d['data-status']
        forloeb.append({"region": regioner[region], "sygehus": sygehuse[sygehus], "speciale": specialer[speciale], "speciale2": specialer[speciale2], "status": status})
    
    with open('forloeb.csv', 'w') as temp:
        writer = csv.DictWriter(temp    , fieldnames=["region", "sygehus", "speciale", "speciale2", "status"])
        writer.writeheader()
        writer.writerows(forloeb)               

def fetch():
    url = "https://basislaege.dk/#"

    payload = {}
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text

main()  

# <div class="panel panel-default enkelt-forloeb-div"
#                          id="enkelt-forloeb-div-3"
#                          data-id="enkelt-forloeb-div-3"
#                          data-clp-btn="collapseBtn3"
#                          data-collapse-id="forloebCollapse3"
#                          data-prioritering=""
#                          data-infobox-header="Forløb #70"
#                          data-infobox-body="Amager og Hvidovre Hospital"
#                          data-tooltip="Amager og Hvidovre Hospital"
#                          data-forloebid="02d349b2-9a8d-4ae1-967a-b7a0a88800d4"
#                          data-region="4"
#                          data-speciale="2574aa81-8672-41e2-80b1-74554113b7f0"
#                          data-speciale2="f6bfce57-d201-4f7b-97de-e0de07e9b6d8"
#                          data-sygehus="11"
#                          data-searchable="Amager og Hvidovre HospitalAMH, Afdeling for Medicinske Sygdomme01-02-2025Hovedstaden - SydL&#xE6;gerne Vesterbrogade 73 BIntern medicinAlmen medicin&#xD8;st&#xD8;stHovedstadenHovedstadenAfdelingen er under omstrukturering. KBU-forl&#xF8;b &#xD;&#xA;p&#xE5; denne afdeling vil ved ans&#xE6;ttelsesstart v&#xE6;re fordelt s&#xE5;ledes: &quot;Forl&#xF8;b #70 - Afd. for Lunge- Hormon og Stofskiftesygdomme, Amager&quot; &#xD;&#xA;&quot;Forl&#xF8;b #238 - Afd. for Lunge- Hormon og Stofskiftesygdomme, Amager&quot; &#xD;&#xA;&quot;Forl&#xF8;b #287 - Afd. for Lunge- Hormon og Stofskiftesygdomme, Amager&quot; &#xD;&#xA;&quot;Forl&#xF8;b #568 - Afd. for &#xC6;ldresygdomme, Amager&quot; &#xD;&#xA;&quot;Forl&#xF8;b #343 - Afd. for &#xC6;ldresygdomme, Amager&quot; &#xD;&#xA;For yderligere information kontaktes afdelingerne; &#xC6;ldresygdomme: Chefl&#xE6;ge Martin Schultz, tlf. 38622852 Lunge- hormon og stofskiftesygdomme: Specialist Christina Belbin, tlf. 38628588&#xD;&#xA;"
#                          data-longitude="12.4702054"
#                          data-latitude="55.6487798"
#                          data-status="optaget"
#                          data-favorit="False">