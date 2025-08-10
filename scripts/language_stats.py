import os
import requests

path = "./key.json"

TOKEN = os.getenv("GH_TOKEN")
headers = {
    "Authorization": f"token {TOKEN}"
}

repos = []
page = 1
while True:
    # print(f"Fetching page {page}...")
    response = requests.get(f"https://api.github.com/user/repos",
                     headers=headers,
                     params={"per_page": 100, "page": page })
    # print(f"Status code: {response.status_code}")

    data = response.json()

    if response.status_code != 200 or len(data) == 0:
        break
    repos.extend(data)
    page += 1

lang_perc = {}
if repos != []:
    lang_totals = {}
    total: int = 0
    for repo in repos:
        response = requests.get(repo["languages_url"], headers=headers)
        # print(f"Fetching language info...")
        # print(f"Status code: {response.status_code}")

        data = response.json()
        for lang, byte_count in data.items():
            try:
                lang_totals[lang] += byte_count
            except:
                lang_totals[lang] = byte_count
            total += byte_count

    for lang in lang_totals:
        bc = lang_totals[lang]
        lang_perc[lang] = round((bc/total) * 100, 1)
    sorted_lp = dict(sorted(lang_perc.items(), key=lambda item: item[1], reverse=True))
    
    input_string = "<!--START_SECTION:languages-->\nLanguages used:\n"
    for lang, perc in sorted_lp.items():
        input_string += f"{lang} --- {perc}%\n"


    with open("README.md", "r") as file:
        readme = file.read()

    updated = readme.replace("<!--START_SECTION:languages-->", input_string)


    with open("README.md", "w") as file:
        file.write(updated)
