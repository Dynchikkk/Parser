import requests
from bs4 import BeautifulSoup


def return_soup_obj(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "lxml")
    return soup


def vtuz_pars(link, snils):
    soup = return_soup_obj(link)

    name_of_fac = soup.find("div", class_="container declaration-table").find("h2", class_="title").text.strip()

    table_post = soup.find("div", class_="table").find("tbody", id="abitTable")
    all_abit = table_post.find_all("tr")

    for i in all_abit:
        all_inf = i.find_all("td")
        abit_snils = all_inf[1].text.strip()
        if abit_snils == snils:
            abit_num = all_inf[0].text.strip()
            return [abit_num, abit_snils, name_of_fac]

    return ["Not in list"]


def pgu_pars(link, snils):
    page = 1

    real_num = list()

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
            abit_snils = all_inf[1].find("a").text.strip()
            name_of_fac_fin = all_inf[2].find("a").text.strip()
            ball = all_inf[7].text.strip()
            real_num.append([int(ball), [abit_snils, name_of_fac_fin]])

        page += 1

    real_num.sort(reverse=True)

    counter = 1
    for i in real_num:
        if i[1][0] == snils:
            return [str(counter), str(i[0]), i[1][0], i[1][1]]
        counter += 1

    return ["Not in list"]


def ask_parcer(link, snils):
    # 1 - pgu
    # 2 - vtuz
    if "pnzgu" in link:
        return pgu_pars(link, snils)
    if "penzgtu" in link:
        return vtuz_pars(link, snils)
    return ["Not right vuz"]


st_snils = "148-061-749 68"
st_pgu_link = ["https://www.pnzgu.ru/apply/list/faculty/31429808/speciality/1995/edu_level/2/edu_form/1/edu_quote1/1/edu_base/1/sort_field/name/sort_type/asc/",
               "https://www.pnzgu.ru/apply/list/faculty/31429808/speciality/2006/edu_level/2/edu_form/1/edu_quote1/1/edu_base/1/sort_field/name/sort_type/asc/",
               "https://www.pnzgu.ru/apply/list/faculty/31429808/speciality/2012/edu_level/2/edu_form/1/edu_quote1/1/edu_base/1/sort_field/name/sort_type/asc/"]
st_vtuz_link = ["http://abitur.penzgtu.ru/ru/entrants/09.03.01/665/",
                "http://abitur.penzgtu.ru/ru/entrants/09.03.02/668/",
                "http://abitur.penzgtu.ru/ru/entrants/09.03.04/674/",
                "http://abitur.penzgtu.ru/ru/entrants/09.03.03/671/"]

while True:
    step = int(input("1 - вставить ссылку, 2 - стандартные ссылки, 0 - выход: "))
    if step == 0:
        break
    elif step == 1:

        link = input("Вставьте сслыку: ")
        snils = input("Вставьте снилс: ")
        print("\n" + ", ".join(ask_parcer(link, snils)) + "\n")
    elif step == 2:
        print("ПГУ")
        for i in st_pgu_link:
            print(", ".join(ask_parcer(i, st_snils)))
        print()
        print("ВТУЗ")
        for i in st_vtuz_link:
            print(", ".join(ask_parcer(i, st_snils)))
        print()



