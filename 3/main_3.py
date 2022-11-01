import mysql.connector as mysql
import prettytable
import matplotlib.pyplot as plt
import numpy as np

DATABASE_NAME = 'PSZ_baza'
TABLE_NAME = 'Nekretnina'

PATH_TO_CHARTS_FILE = 'results/main_3_charts/'


def print_all_data_from_query_to_table(columns, query):
    table = prettytable.PrettyTable(columns)
    cursor.execute(query)
    results = cursor.fetchall()
    for result in results:
        table.add_row(result)
    print(table)
    print("\n")


def draw_graph(x, y, xlabel, ylabel, title, save_to_file):
    fig = plt.figure()
    plt.style.use('ggplot')
    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x_pos, y, color='green', width=0.5, bottom=None, align='center')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(x_pos, x, fontsize=7)
    plt.show()
    fig.savefig(save_to_file)


def multiple_queries(queries, xlabel, ylabel, title, more, save_to_file, replace_spaces_with_new_lines=False):
    x = []
    y = []
    for query in queries:
        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            if result[0] != '':
                if replace_spaces_with_new_lines:
                    x_string = result[0].replace(' ', '\n') + '\n(' + str(result[1]) + ')'
                else:
                    x_string = result[0] + '\n(' + str(result[1]) + ')'
                if more:
                    x_string = x_string + '\n(' + str(result[2]) + '%)'
                x.append(x_string)
                y.append(result[1])
    if save_to_file != '':
        draw_graph(x, y, xlabel, ylabel, title, save_to_file)
    return x, y


def a():
    q = "SELECT (CASE " \
        "WHEN SUBSTRING(SUBSTRING_INDEX(Lokacija, ' (', 1), 10, 12) = 'Novi Beograd' THEN 'Novi Beograd' " \
        "ELSE SUBSTRING(SUBSTRING_INDEX(Lokacija, ' (', 1), 10) " \
        "END), COUNT(*) " \
        "FROM " + TABLE_NAME + " " \
        "WHERE SUBSTRING(Lokacija, 1, 7) = 'Beograd' " \
        "GROUP BY (CASE " \
        "WHEN SUBSTRING(SUBSTRING_INDEX(Lokacija, ' (', 1), 10, 12) = 'Novi Beograd' THEN 'Novi Beograd' " \
        "ELSE SUBSTRING(SUBSTRING_INDEX(Lokacija, ' (', 1), 10) " \
        "END) " \
        "ORDER BY COUNT(*) DESC " \
        "LIMIT 10;"
    cursor.execute(q)
    results = cursor.fetchall()
    x = []
    y = []
    for result in results:
        x.append(result[0].replace(' ', '\n') + '\n(' + str(result[1]) + ')')
        y.append(result[1])
    draw_graph(x, y, "Deo Beograda", "Broj nekretnina", "Delovi Beograda koji imaju najveći broj nekretnina u ponudi", f'{PATH_TO_CHARTS_FILE}3a).jpg')


def b():
    q = []
    q1 = "SELECT CASE " \
         "WHEN TRUNCATE(kvadratura, 0) <= 35 THEN '<= 35m²' " \
         "WHEN TRUNCATE(kvadratura, 0) BETWEEN 36 AND 50 THEN '36m² - 50m²' " \
         "WHEN TRUNCATE(kvadratura, 0) BETWEEN 51 AND 65 THEN '51m² - 65m²' " \
         "ELSE '' " \
         "END, COUNT(*) " \
         "FROM " + TABLE_NAME + " " \
                                "WHERE tip_nekretnine = 'Stan' and tip_ponude = 'Prodaja' " \
                                "GROUP BY CASE " \
                                "WHEN TRUNCATE(kvadratura, 0) <= 35 THEN '<= 35m²' " \
                                "WHEN TRUNCATE(kvadratura, 0) BETWEEN 36 AND 50 THEN '36m² - 50m²' " \
                                "WHEN TRUNCATE(kvadratura, 0) BETWEEN 51 AND 65 THEN '51m² - 65m²' " \
                                "ELSE ''" \
                                "END " \
                                "ORDER BY CONVERT(kvadratura, UNSIGNED INTEGER);"
    q2 = "SELECT CASE " \
         "WHEN TRUNCATE(kvadratura, 0) BETWEEN 66 AND 80 THEN '66m² - 80m²' " \
         "WHEN TRUNCATE(kvadratura, 0) BETWEEN 81 AND 96 THEN '81m² - 95m²' " \
         "WHEN TRUNCATE(kvadratura, 0) BETWEEN 96 AND 110 THEN '96m² - 110m²' " \
         "ELSE '' " \
         "END, COUNT(*) " \
         "FROM " + TABLE_NAME + " " \
                                "WHERE tip_nekretnine = 'Stan' and tip_ponude = 'Prodaja' " \
                                "GROUP BY CASE " \
                                "WHEN TRUNCATE(kvadratura, 0) BETWEEN 66 AND 80 THEN '66m² - 80m²' " \
                                "WHEN TRUNCATE(kvadratura, 0) BETWEEN 81 AND 95 THEN '81m² - 95m²' " \
                                "WHEN TRUNCATE(kvadratura, 0) BETWEEN 96 AND 110 THEN '96m² - 110m²' " \
                                "ELSE ''" \
                                "END " \
                                "ORDER BY CONVERT(kvadratura, UNSIGNED INTEGER);"
    q3 = "SELECT CASE " \
         "WHEN TRUNCATE(kvadratura, 0) >= 111 THEN '>= 111m²' " \
         "ELSE '' " \
         "END, COUNT(*) " \
         "FROM " + TABLE_NAME + " " \
                                "WHERE tip_nekretnine = 'Stan' and tip_ponude = 'Prodaja' " \
                                "GROUP BY CASE " \
                                "WHEN TRUNCATE(kvadratura, 0) >= 111 THEN '>= 111m²' " \
                                "ELSE ''" \
                                "END " \
                                "ORDER BY CONVERT(kvadratura, UNSIGNED INTEGER);"
    q.append(q1)
    q.append(q2)
    q.append(q3)
    multiple_queries(q, "Kvadratura", "Broj stanova", "Broj stanova za pordaju prema kvadraturi", False, f'{PATH_TO_CHARTS_FILE}3b).jpg')


def c():
    q = []
    q1 = "SELECT CASE " \
         "WHEN godina_izgradnje REGEXP '^-?[0-9]+$' and godina_izgradnje <= 1950 THEN '<= 1950' " \
         "WHEN godina_izgradnje BETWEEN 1951 AND 1960 THEN '1951-1960' " \
         "WHEN godina_izgradnje BETWEEN 1961 AND 1970 THEN '1961-1970' " \
         "ELSE '' " \
         "END, COUNT(*) " \
         "FROM psz_baza.nekretnina " \
         "GROUP BY CASE " \
         "WHEN godina_izgradnje REGEXP '^-?[0-9]+$' and godina_izgradnje <= 1950 THEN '<= 1950' " \
         "WHEN godina_izgradnje BETWEEN 1951 AND 1960 THEN '1951-1960' " \
         "WHEN godina_izgradnje BETWEEN 1961 AND 1970 THEN '1961-1970' " \
         "ELSE '' " \
         "END   " \
         "ORDER BY CONVERT(godina_izgradnje, UNSIGNED INTEGER);"
    q2 = "SELECT CASE " \
         "WHEN godina_izgradnje BETWEEN 1971 AND 1980 THEN '1971-1980' " \
         "WHEN godina_izgradnje BETWEEN 1981 AND 1990 THEN '1981-1990' " \
         "WHEN godina_izgradnje BETWEEN 1991 AND 2000 THEN '1991-2000' " \
         "ELSE '' " \
         "END, COUNT(*) " \
         "FROM psz_baza.nekretnina " \
         "GROUP BY CASE " \
         "WHEN godina_izgradnje BETWEEN 1971 AND 1980 THEN '1971-1980' " \
         "WHEN godina_izgradnje BETWEEN 1981 AND 1990 THEN '1981-1990' " \
         "WHEN godina_izgradnje BETWEEN 1991 AND 2000 THEN '1991-2000' " \
         "ELSE '' " \
         "END   " \
         "ORDER BY CONVERT(godina_izgradnje, UNSIGNED INTEGER);"
    q3 = "SELECT CASE " \
         "WHEN godina_izgradnje BETWEEN 2001 AND 2010 THEN '2001-2010' " \
         "WHEN godina_izgradnje BETWEEN 2011 AND 2020 THEN '2011-2020' " \
         "WHEN godina_izgradnje >= 2021 THEN '>= 2021' " \
         "ELSE '' " \
         "END, COUNT(*) " \
         "FROM psz_baza.nekretnina " \
         "GROUP BY CASE " \
         "WHEN godina_izgradnje BETWEEN 2001 AND 2010 THEN '2001-2010' " \
         "WHEN godina_izgradnje BETWEEN 2011 AND 2020 THEN '2011-2020' " \
         "WHEN godina_izgradnje >= 2021 THEN '>= 2021' " \
         "ELSE '' " \
         "END   " \
         "ORDER BY CONVERT(godina_izgradnje, UNSIGNED INTEGER);"
    q4 = "SELECT CASE " \
         "WHEN godina_izgradnje NOT REGEXP '^-?[0-9]+$' THEN (CASE WHEN stanje_nekretnine = '' THEN 'Nepoznatno' ELSE stanje_nekretnine END) " \
         "ELSE '' " \
         "END, COUNT(*) " \
         "FROM psz_baza.nekretnina " \
         "GROUP BY CASE " \
         "WHEN godina_izgradnje NOT REGEXP '^-?[0-9]+$' THEN (CASE WHEN stanje_nekretnine = '' THEN 'Nepoznatno' ELSE stanje_nekretnine END) " \
         "ELSE '' " \
         "END   " \
         "ORDER BY CONVERT(godina_izgradnje, UNSIGNED INTEGER);"
    q.append(q1)
    q.append(q2)
    q.append(q3)
    q.append(q4)
    multiple_queries(q, "Dekade/Stanje objekta", "Broj nekretnina", "Broj izgrađenih nekretnina po dekadama/stanje objekta", False, f'{PATH_TO_CHARTS_FILE}3c).jpg', True)


def d():
    q = "SELECT SUBSTRING_INDEX(Lokacija, ',', 1) AS Location, " \
        "(SELECT COUNT(*) FROM psz_baza.nekretnina WHERE tip_ponude = 'Prodaja' AND SUBSTRING_INDEX(Lokacija, ',', 1) = Location), " \
        "(SELECT COUNT(*) FROM psz_baza.nekretnina WHERE tip_ponude = 'Izdavanje' AND SUBSTRING_INDEX(Lokacija, ',', 1) = Location) " \
        "FROM psz_baza.nekretnina  " \
        "WHERE SUBSTRING_INDEX(Lokacija, ',', 1) IN (" \
            "SELECT TOWN FROM (" \
            "SELECT SUBSTRING_INDEX(Lokacija, ',', 1) AS TOWN " \
            "FROM psz_baza.nekretnina  B " \
            "GROUP BY TOWN " \
            "ORDER BY COUNT(*) DESC " \
            "LIMIT 5 " \
        ") AS C " \
    ") GROUP BY Location " \
    "ORDER BY COUNT(*) DESC;"
    cursor.execute(q)
    results = cursor.fetchall()
    index = 1
    for result in results:
        x = ['Broj nekretnina za\nprodaju (' + str(result[1]) + ")", 'Broj nekretnina\nza iznajmljivanje\n(' + str(result[2]) + ")"]
        y = [result[1], result[2]]
        fig = plt.figure()
        ax1 = fig.add_subplot()
        ax1.pie(y, labels=x, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.title.set_text(f'Broj (i procentualni odnos) nekretnina za prodaju i iznajmljivanje za \n{index}. grad po broju nekretnina ({result[0]})')
        plt.show()
        fig.savefig(f'{PATH_TO_CHARTS_FILE}3d)_{index}.grad po broju nekretnina ({result[0]}).jpg')
        index = index + 1


def e():
    q = []
    q1 = "SELECT CASE " \
        "WHEN TRUNCATE(CONVERT(REPLACE(SUBSTRING_INDEX(cena, 'EUR', 1), ' ', ''), UNSIGNED INTEGER), 0) <= 49999 THEN '<= 49999€' " \
        "ELSE '' " \
        "END, COUNT(*), ROUND(COUNT(*) / (SELECT COUNT(*) FROM psz_baza.nekretnina WHERE tip_ponude = 'Prodaja') * 100, 1) " \
        "FROM psz_baza.nekretnina " \
        "WHERE tip_ponude = 'Prodaja' " \
        "GROUP BY CASE " \
         "WHEN TRUNCATE(CONVERT(REPLACE(SUBSTRING_INDEX(cena, 'EUR', 1), ' ', ''), UNSIGNED INTEGER), 0) <= 49999 THEN '<= 49999€' " \
        "ELSE '' " \
        "END " \
        "ORDER BY CONVERT(cena, UNSIGNED INTEGER)"
    q2 = "SELECT CASE " \
         "WHEN TRUNCATE(CONVERT(REPLACE(SUBSTRING_INDEX(cena, 'EUR', 1), ' ', ''), UNSIGNED INTEGER), 0) BETWEEN 50000 AND 99999 THEN '[50000€, 99999€]' " \
         "ELSE '' " \
         "END, COUNT(*), ROUND(COUNT(*) / (SELECT COUNT(*) FROM psz_baza.nekretnina WHERE tip_ponude = 'Prodaja') * 100, 1) " \
         "FROM psz_baza.nekretnina " \
         "WHERE tip_ponude = 'Prodaja' " \
         "GROUP BY CASE " \
         "WHEN TRUNCATE(CONVERT(REPLACE(SUBSTRING_INDEX(cena, 'EUR', 1), ' ', ''), UNSIGNED INTEGER), 0) BETWEEN 50000 AND 99999 THEN '[50000€, 99999€]' " \
         "ELSE '' " \
         "END " \
         "ORDER BY CONVERT(cena, UNSIGNED INTEGER)"
    q3 = "SELECT CASE " \
         "WHEN CONVERT(REPLACE(SUBSTRING_INDEX(cena, 'EUR', 1), ' ', ''), UNSIGNED INTEGER) BETWEEN 100000 AND 149999 THEN '[100000€, 149999€]' " \
         "ELSE '' " \
         "END, COUNT(*), ROUND(COUNT(*) / (SELECT COUNT(*) FROM psz_baza.nekretnina WHERE tip_ponude = 'Prodaja') * 100, 1) " \
         "FROM psz_baza.nekretnina " \
         "WHERE tip_ponude = 'Prodaja' " \
         "GROUP BY CASE " \
         "WHEN CONVERT(REPLACE(SUBSTRING_INDEX(cena, 'EUR', 1), ' ', ''), UNSIGNED INTEGER) BETWEEN 100000 AND 149999 THEN '[100000€, 149999€]' " \
         "ELSE '' " \
         "END " \
         "ORDER BY CONVERT(cena, UNSIGNED INTEGER)"
    q4 = "SELECT CASE " \
         "WHEN CONVERT(REPLACE(SUBSTRING_INDEX(cena, 'EUR', 1), ' ', ''), UNSIGNED INTEGER) BETWEEN 150000 AND 199999 THEN '[150000€, 199999€]' " \
         "ELSE '' " \
         "END, COUNT(*), ROUND(COUNT(*) / (SELECT COUNT(*) FROM psz_baza.nekretnina WHERE tip_ponude = 'Prodaja') * 100, 1) " \
         "FROM psz_baza.nekretnina " \
         "WHERE tip_ponude = 'Prodaja' " \
         "GROUP BY CASE " \
         "WHEN CONVERT(REPLACE(SUBSTRING_INDEX(cena, 'EUR', 1), ' ', ''), UNSIGNED INTEGER) BETWEEN 150000 AND 199999 THEN '[150000€, 199999€]' " \
         "ELSE '' " \
         "END " \
         "ORDER BY CONVERT(cena, UNSIGNED INTEGER)"
    q5 = "SELECT CASE " \
         "WHEN TRUNCATE(CONVERT(REPLACE(SUBSTRING_INDEX(cena, 'EUR', 1), ' ', ''), UNSIGNED INTEGER), 0) >= 200000 THEN '>= 200000€' " \
         "ELSE '' " \
         "END, COUNT(*), ROUND(COUNT(*) / (SELECT COUNT(*) FROM psz_baza.nekretnina WHERE tip_ponude = 'Prodaja') * 100, 1) " \
         "FROM psz_baza.nekretnina " \
         "WHERE tip_ponude = 'Prodaja' " \
         "GROUP BY CASE " \
         "WHEN TRUNCATE(CONVERT(REPLACE(SUBSTRING_INDEX(cena, 'EUR', 1), ' ', ''), UNSIGNED INTEGER), 0) >= 200000 THEN '>= 200000€' " \
         "ELSE '' " \
         "END " \
         "ORDER BY CONVERT(cena, UNSIGNED INTEGER)"
    q.append(q1)
    q.append(q2)
    q.append(q3)
    q.append(q4)
    q.append(q5)
    x, y = multiple_queries(q, "Cenovni opseg", "Broj nekretnina", "Broj (i procentualni odnos) nekretnina za prodaju koji pripadaju cenovnom opsegu", True, '')
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.pie(y, labels=x, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.title.set_text('Broj i procentualni odnos nekretnina za prodaju koji pripadaju cenovnom opsegu\n')
    plt.show()
    fig.savefig(f'{PATH_TO_CHARTS_FILE}3e).jpg')


def f():
    q = "SELECT (SELECT COUNT(*) FROM psz_baza.nekretnina WHERE tip_ponude = 'Prodaja' AND SUBSTRING_INDEX(Lokacija, ',', 1) = 'Beograd' AND parking = 'Da'), COUNT(*) " \
        "FROM psz_baza.nekretnina " \
        "WHERE tip_ponude = 'Prodaja' AND SUBSTRING_INDEX(Lokacija, ',', 1) = 'Beograd'"
    cursor.execute(q)
    results = cursor.fetchall()
    x = []
    y = []
    for result in results:
        x = ['Broj nekretnina koje\nimaju parking (' + str(result[0]) + ")", 'Broj nekretnina\nkoje nemaju\nparking (' + str(result[1]-result[0]) + ")"]
        y = [result[0], result[1] - result[0]]
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.pie(y, labels=x, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.title.set_text('Broj nekretnina za prodaju koje imaju parking,\nu odnosu na ukupan broj nekretnina za prodaju (samo za Beograd)')
    plt.show()
    fig.savefig(f'{PATH_TO_CHARTS_FILE}3f).jpg')


db = mysql.connect(
    host="localhost",
    user="root",
    password="123#Madmin",
    database=DATABASE_NAME,
)
cursor = db.cursor()

a()
b()
c()
d()
e()
f()
