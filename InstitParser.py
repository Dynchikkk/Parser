import requests
from bs4 import BeautifulSoup


def return_soup_obj(link):
    global headers
    r = requests.get(link, headers)
    soup = BeautifulSoup(r.text, "lxml")
    return soup


def vtuz_pars(link, snils):
    soup = return_soup_obj(link)

    try:
        name_of_fac = soup.find("div", class_="container declaration-table").find("h2", class_="title").text.strip()
    except Exception:
        return ["Not in list"]

    table_post = soup.find("div", class_="table").find("tbody", id="abitTable")
    all_abit = table_post.find_all("tr")

    for i in all_abit:
        all_inf = i.find_all("td")
        abit_snils = all_inf[1].text.strip()
        if abit_snils == snils:
            abit_num = all_inf[0].text.strip()
            return ["ВТУЗ", abit_num, abit_snils, name_of_fac]

    return ["Not in list"]


def pgu_pars(link, snils):
    global headers
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
            return ["ПГУ", str(counter), str(i[0]), i[1][0], i[1][1]]
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


def add_data():
    snils = input("Введисте снилс: ")
    link_list = list()
    while True:
        link = input("Введите ссылку (Если все сслыки введены - 0): ")
        if link == "0":
            break
        link_list.append(link)
    with open("data.txt", "w", encoding="utf-8") as data_file:
        data_file.write(snils + "\n")
        for i in link_list:
            data_file.write(i.replace("\n", "") + "\n")
    return ["Данные записаны"]


def read_data():
    with open("data.txt", "r") as data_file:
        st_snils = data_file.readline().replace("\n", "")
        if st_snils == "":
            return ["Нет файла"]
        links = data_file.readlines()
        return [st_snils, links]


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

st_snils = "148-061-749 68"
st_pgu_link = ["https://www.pnzgu.ru/apply/list/faculty/31429808/speciality/1995/edu_level/2/edu_form/1/edu_quote1/1/edu_base/1/sort_field/name/sort_type/asc/",
               "https://www.pnzgu.ru/apply/list/faculty/31429808/speciality/2006/edu_level/2/edu_form/1/edu_quote1/1/edu_base/1/sort_field/name/sort_type/asc/",
               "https://www.pnzgu.ru/apply/list/faculty/31429808/speciality/2012/edu_level/2/edu_form/1/edu_quote1/1/edu_base/1/sort_field/name/sort_type/asc/"]
st_vtuz_link = ["http://abitur.penzgtu.ru/ru/entrants/09.03.01/665/",
                "http://abitur.penzgtu.ru/ru/entrants/09.03.02/668/",
                "http://abitur.penzgtu.ru/ru/entrants/09.03.04/674/",
                "http://abitur.penzgtu.ru/ru/entrants/09.03.03/671/"]

while True:
    step = int(input("1 - вставить ссылку, 2 - стандартные ссылки, 3 - добавить/редактировать стандартные ссылки, "
                     "0 - выход: "))
    if step == 0:
        break
    elif step == 1:
        link = input("Вставьте сслыку: ")
        snils = input("Вставьте снилс: ")
        print("\n" + ", ".join(ask_parcer(link, snils)) + "\n")
    elif step == 2:
        stand = read_data()
        if stand[0] == "Нет файла":
            print("Нет стандартных ссылок")
            continue
        print("Считывание данных\n")
        for i in stand[1]:
            print(", ".join(ask_parcer(i.replace("\n", ""), stand[0])))
        print("\nДанные считаны")
    elif step == 3:
        print(", ".join(add_data()))




