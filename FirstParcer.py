import requests
from bs4 import BeautifulSoup

r = requests.get("http://abitur.penzgtu.ru/ru/entrants/09.03.01/665/")

soup = BeautifulSoup(r.text, "lxml")

table_post = soup.find("div", class_="table").find("tbody", id="abitTable")
all_abit = table_post.find_all("tr")

abits = list()

for i in all_abit:
    all_inf = i.find_all("td")
    abit_num = all_inf[0].text.strip()
    abit_snils = all_inf[1].text.strip()
    abits.append([abit_num, abit_snils])

for i in abits:
    if i[1] == "148-061-749 68":
        print(i[0], i[1])
        break
