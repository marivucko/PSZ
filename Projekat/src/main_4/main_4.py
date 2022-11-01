import os
import mysql.connector as mysql
from numpy import loadtxt
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time

DATABASE_NAME = 'PSZ_baza'


def get_location_distance_for_one_data(location):
    url = "https://www.google.com/maps/dir/%D0%A2%D1%80%D0%B3+%D1%80%D0%B5%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B5,+%D0%91%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D0%B4/%D0%A2%D1%80%D0%B3+%D1%80%D0%B5%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B5,+%D0%91%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D0%B4+11000/@44.8105531,20.4648601,15z/data=!4m14!4m13!1m5!1m1!1s0x475a7ab25c703261:0x99b65b127891b036!2m2!1d20.4599624!2d44.816088!1m5!1m1!1s0x475a7ab2453c4ba1:0xb81037438bba0036!2m2!1d20.4603199!2d44.8162551!3e0"
    PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver_win32_98\chromedriver.exe"
    options = Options()
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(PATH, options=options)
    driver.set_page_load_timeout(300)
    try:
        driver.get(url)
        driver.find_element_by_class_name("tactile-searchbox-input").clear()
        driver.find_element_by_class_name("tactile-searchbox-input").send_keys(location)
        driver.find_elements_by_class_name("nhb85d-BIqFsb")[0].click()
        time.sleep(7)
        distance = driver.find_elements_by_xpath("//div[@class='xB1mrd-T3iPGc-iSfDt-ij8cu']//div//div//div//div")[0].text
        if distance.split()[1] == 'm':
            distance = str(float(distance.split()[0]) * 0.001)
        else:
            distance = distance.split()[0]
        print(distance)
        driver.close()
        driver.quit()
        return float(distance.replace(',', '.'))
    except WebDriverException as e:
        print('greska')
        print(e)
        return -1


def get_min_max_year():
    q = "select min(godina_izgradnje), max(godina_izgradnje) from nekretnina where tip_nekretnine = 'Stan' and tip_ponude = 'Prodaja' and substring_index(Lokacija, ',', 1) = 'Beograd' and godina_izgradnje != '';"
    cursor.execute(q)
    results = cursor.fetchall()
    return results[0][0], results[0][1]


def fill_min_max_arrays(query, minimums, maximums):
    cursor.execute(query)
    results = cursor.fetchall()
    minimums.append(results[0][0])
    maximums.append(results[0][1])
    return minimums, maximums


def fill_minimums_maximums(num_of_parameters):
    minimums = []
    maximums = []
    q = ["select min(convert(left(kvadratura, char_length(kvadratura)-3), signed integer)), max(convert(left(kvadratura, char_length(kvadratura)-3), signed integer)) from nekretnina t where tip_nekretnine = 'Stan' and tip_ponude = 'Prodaja' and substring_index(Lokacija, ',', 1) = 'Beograd' and left(kvadratura, char_length(kvadratura)-3) REGEXP '^[0-9]+$';",
        "select min(convert(broj_soba, signed integer)), max(convert(broj_soba, signed integer)) from nekretnina t where tip_nekretnine = 'Stan' and tip_ponude = 'Prodaja' and substring_index(Lokacija, ',', 1) = 'Beograd' and broj_soba REGEXP '^[0-9]+$';",
         "select min(convert(replace(udaljenost, ' ', ''), float)), max(convert(replace(udaljenost, ' ', ''), float)) from udaljenosti;"]
    minimums, maximums = fill_min_max_arrays(q[0], minimums, maximums)      # square footage
    if num_of_parameters == 1:
        return minimums, maximums
    if num_of_parameters == 10:
        minimums.append(-2)      # object_condition
        maximums.append(6)      # object_condition
        minimums.append(int(min_year))      # construction_year
        maximums.append(int(max_year))      # construction_year
        minimums.append(-1)      # floor
        maximums.append(37)      # floor
        minimums.append(-1)      # num_of_floors
        maximums.append(44)      # num_of_floors
        minimums.append(-1)      # registration
        maximums.append(1)      # registration
    if num_of_parameters == 10 or num_of_parameters == 3:
        minimums, maximums = fill_min_max_arrays(q[1], minimums, maximums)  # num_of_rooms
    if num_of_parameters == 10:
        minimums.append(-1)  # parking
        maximums.append(1)  # parking
        minimums.append(-1)  # elevator
        maximums.append(1)  # elevator
    minimums, maximums = fill_min_max_arrays(q[2], minimums, maximums)  # location_distance
    return minimums, maximums


def calculate(xx, num_of_parameters):
    file = f'H:\Serije\PSZ\Projekat\src\main_4\main_4_{str(num_of_parameters)}_parameters\w.dat'
    if os.path.isfile(file):
        w = loadtxt(file, comments="#", delimiter=",", unpack=False)
    else:
        return 0
    value = w[0]
    for i in range(0, num_of_parameters):
        value = value + w[i + 1] * xx[i]
    return value


def linear_regression(num_of_parameters, input_data, message):
    minimums_of_variables, maximums_of_variables = fill_minimums_maximums(num_of_parameters)
    for i in range(0, len(input_data)):
        input_data[i] = ((input_data[i] - minimums_of_variables[i]) / (maximums_of_variables[i] - minimums_of_variables[i])) * 2 - 1
    print(message, round(calculate(input_data, num_of_parameters), 2), "EUR-a.")


def input_form():
    location = str(input("Unesite lokaciju stana: "))
    location_distance = get_location_distance_for_one_data(location)
    # location_distance = float(input("Unesite udaljenost stana od centra: "))
    square_footage = float(input("Unesite kvadraturu stana: "))
    object_condition = int(input("Unestie stanje stana:\n-2 -> Namenjeno rušenju\n-1 -> Delimična rekonstrukcija\n0 -> Kompletna rekonstrukcija ili Neodređeno\n1 -> Izvorno stanje\n2 -> Standardna gradnja\n3 -> U izgradnji\n4 -> Završena izgradnja\n5 -> U pripremi\n6 -> Novogradnja\n: "))
    construction_year = int(input("Unestie godinu izgradnje zgrade u kojoj je stan: "))
    floor = float(input("Unesite na kom je spratu (0 za prizemnje, -1 za suteren, 0.5 za visoko prizemlje ili broj sprata za vise spratove): "))
    num_of_floors = float(input("Unesite koliko spratova ima zgrada: "))
    registration = int(input("Unestie da li je stana uknjižen: 1 - ako jeste, -1 - ako nije: "))
    num_of_rooms = float(input("Unesite koliko soba ima stan: "))
    parking = int(input("Unestie da li postoji parking: 1 - ako ima, -1 - ako nema: "))
    elevator = int(input("Unestie da li zgrada ima lift: 1 - ako ima, -1 - ako nema: "))
    linear_regression(1, [square_footage], 'Linarna regersija korišćenjem gradijentnog spusta i 1 odlike (kvadratura) predviđa da je cena stana:')
    linear_regression(2, [square_footage, location_distance], 'Višestruka linarna regersija korišćenjem gradijentnog spusta i 2 odlike (kvadratura, lokacija) predviđa da je cena stana:')
    linear_regression(3, [square_footage, num_of_rooms, location_distance], 'Višestruka linarna regersija korišćenjem gradijentnog spusta i 3 odlike (kvadratura, broj soba, lokacija) predviđa da je cena stana:')
    linear_regression(10, [square_footage, object_condition, construction_year, floor, num_of_floors, registration, num_of_rooms, parking, elevator, location_distance], 'Višestruka linarna regersija korišćenjem gradijentnog spusta i 10 odlika '
                         '(kvadratura, stanje objekta, godina izgradnje, sprat, ukupna spratnost, uknjiženost, broj soba, parking, lift, lokacija) predviđa da je cena stana:')


db = mysql.connect(
    host="localhost",
    user="root",
    password="123#Madmin",
    database=DATABASE_NAME,
)
cursor = db.cursor()
min_year, max_year = get_min_max_year()
input_form()