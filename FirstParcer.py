import requests
from bs4 import BeautifulSoup


def return_soup_obj(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "lxml")
    return soup


def vtuz_pars(link):
    soup = return_soup_obj(link)

    name_of_fac = soup.find("div", class_="container declaration-table").find("h2", class_="title").text.strip()

    table_post = soup.find("div", class_="table").find("tbody", id="abitTable")
    all_abit = table_post.find_all("tr")

    for i in all_abit:
        all_inf = i.find_all("td")
        abit_num = all_inf[0].text.strip()
        abit_snils = all_inf[1].text.strip()
        if abit_snils == "148-061-749 63":
            return [abit_num, abit_snils, name_of_fac]

    return "Not in list"


def pgu_pars(link):
    page = 1

    local_link = link + "p/" + str(page)
    name_of_fac1 = return_soup_obj(local_link).find("div", class_="content-page")
    name_of_fac_fin = name_of_fac1.find("a", href="/apply/list/faculty/").text.strip()

    while True:
        local_link = link + "p/" + str(page)
        soup = return_soup_obj(local_link)

        try:
            table_post = soup.find("table", class_="list_table").find("tbody")
        except AttributeError:
            break

        all_abit = table_post.find_all("tr", class_="list_row_1 display_true")

        for i in all_abit:
            all_inf = i.find_all("td")
            abit_num = all_inf[0].text.strip()
            abit_snils = all_inf[1].find("a").text.strip()
            if abit_snils == "148-061-749 68":
                return [abit_num, abit_snils, name_of_fac_fin]

        page += 1
    return "Not in list"


# VTUZ
# http://abitur.penzgtu.ru/ru/entrants/09.03.01/665/ - inf and vyt texn
# http://abitur.penzgtu.ru/ru/entrants/09.03.02/668/ - inf syst and texn

# PGU
# https://www.pnzgu.ru/apply/list/faculty/31429808/speciality/1995/edu_level/2/edu_form/1/edu_quote1/1/edu_base/1/sort_field/name/sort_type/asc/

link = input("Вставьте сслыку: ")
print(*vtuz_pars(link))
# print(pgu_pars(link))

