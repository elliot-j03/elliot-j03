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
    
    input_string: str = "\n### Top 5 Languages used:<br>\n"
    lang_count: int = 0
    for lang, perc in sorted_lp.items():
        if lang_count == 5:
            break
        bar_length: int = round((perc/4))
        empty_length: int = round((100/4 - bar_length))
        input_string += f"**{lang}**<br>\n{"█" * bar_length}{"░" * empty_length} - {perc}%<br>\n"
        lang_count += 1


    with open("./README.md", "r") as file:
        readme = file.read()

    start_string = "<!--START_SECTION:languages-->"
    end_string = "<!--END_SECTION:languages-->"

    start_idx = readme.index(start_string) + len(start_string)
    end_idx = readme.index(end_string)

    updated_readme = readme[:start_idx] + input_string + readme[(end_idx - 1):]

    with open("./README.md", "w") as file:
        file.write(updated_readme)
