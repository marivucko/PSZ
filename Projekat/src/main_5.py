import mysql.connector as mysql
import math
import prettytable
import mysql.connector as mysql
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
from src.main_3 import e

DATABASE_NAME = 'PSZ_baza'
TABLE_NAME = 'Nekretnina'
TABLE_NAME_LOCATION_DISTANCE = 'Udaljenosti'
ROW_LOCATION = 'Lokacija'
ROW_OFFER = 'tip_nekretnine'
ROW_OFFER_FLAT = 'Stan'
ROW_OFFER_HOUSE = 'Kuca'
ROW_PROPERTY = 'tip_ponude'
ROW_PROPERTY_SALE = 'Prodaja'
ROW_PROPERTY_RENT = 'Izdavanje'

PATH_TO_MAIN_5_RESULTS_FOR_TESTING_SET = 'results/main_5/results_for_testing_set.txt'
PATH_TO_MAIN_5_VISUAL_REPRESENTATION = 'results/main_5/visual_representation.jpg'

# class 0 --->      <= 49999€
# class 1 --->      [50 000€, 99 999€]
# class 2 --->      [100 000€, 149 999€]
# class 3 --->      [150000€, 199 999€]
# class 4 --->      >= 200 000€


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
        driver.close()
        return float(distance.replace(',', '.'))
    except WebDriverException as e:
        print('greska')
        print(e)
        return -1


def convert_object_condition_str_to_int(object_condition):  # if we don't know the construction year of a real estate the condtion of the object will help determinate
    if object_condition == 'Namenjeno rušenju':
        return -2, 1900
    if object_condition == 'Delimična rekonstrukcija':
        return -1, 2000
    if object_condition == 'Kompletna rekonstrukcija':
        return 0, 2010
    if object_condition == '':
        return 0, (float(min_year) + float(max_year)) / 2
    if object_condition == 'Izvorno stanje':
        return 1, 1970
    if object_condition == 'Standardna gradnja':
        return 2, 1990
    elif object_condition == 'U izgradnji':
        return 3, 2021
    elif object_condition == 'Završena izgradnja':
        return 4, 2021
    elif object_condition == 'U pripremi':
        return 5, 2021
    elif object_condition == 'Novogradnja':
        return 6, 2020


def get_min_max_year():
    q = "select min(godina_izgradnje), max(godina_izgradnje) from nekretnina where tip_nekretnine = 'Stan' and tip_ponude = 'Prodaja' and substring_index(Lokacija, ',', 1) = 'Beograd' and godina_izgradnje != '';"
    cursor.execute(q)
    results = cursor.fetchall()
    return results[0][0], results[0][1]


def process_one_row_from_database(result):
    square_footage = result[4]
    object_condition = result[5]
    construction_year = result[6]
    floor = result[8]
    num_of_floors = result[9]
    registration = result[10]
    num_of_rooms = result[12]
    parking = result[14]
    elevator = result[15]
    price = result[20]
    location_distance = result[23]
    row_data = [square_footage, object_condition, construction_year, floor, num_of_floors, registration, num_of_rooms, parking, elevator, location_distance, price]
    try:
        square_footage = float(square_footage.split('m²')[0])
        price = float(price.split(' EUR')[0].replace(' ', '').replace(',', '.'))
        object_condition, cy = convert_object_condition_str_to_int(object_condition)
        if construction_year == '':
            construction_year = cy
        else:
            construction_year = float(construction_year)
    except ValueError:
        return None
    if floor == '-':
        floor = 1
    elif floor == 'Visoko prizemlje':
        floor = 0.5
    elif floor == 'Prizemlje':
        floor = 0
    elif floor == 'Suteren':
        floor = -1
    else:
        floor = float(floor)
    if num_of_floors == '-':
        num_of_floors = floor
    elif num_of_floors == 'Visoko prizemlje':
        num_of_floors = 0.5
    elif num_of_floors == 'Prizemlje':
        num_of_floors = 0
    elif num_of_floors == 'Suteren':
        num_of_floors = -1
    else:
        num_of_floors = float(num_of_floors)
    registration = 1 if registration == 'Da' else -1
    if num_of_rooms == '-':
        num_of_rooms = 0.5
    num_of_rooms = float(num_of_rooms)
    parking = 1 if parking == 'Da' else -1
    elevator = 1 if elevator == 'Da' else -1
    location_distance = float(location_distance.replace(',', '.'))
    if price >= 200000:
        price_range = 4
    elif 150000 < price <= 199999:
        price_range = 3
    elif 100000 < price <= 149999:
        price_range = 2
    elif 50000 < price <= 99999:
        price_range = 1
    else:
        price_range = 0
    processed_data = [square_footage, object_condition, construction_year, floor, num_of_floors, registration, num_of_rooms, parking, elevator, price, price_range, location_distance]
    return row_data, processed_data


def process_all_data_from_database(results):
    xx = []
    yy = []
    zz = []
    for result in results:
        try:
            row_data, processed_data = process_one_row_from_database(result)
            square_footage, object_condition, construction_year, floor, num_of_floors, registration, num_of_rooms, parking, elevator, price, price_range, location_distance = processed_data
        except TypeError:
            continue
        xx.append([square_footage, object_condition, construction_year, floor, num_of_floors, registration, num_of_rooms, parking, elevator, location_distance, price_range])
        yy.append(price)
        zz.append(row_data)
    return xx, yy, zz


def training_data():
    q = "SELECT t.*, (SELECT udaljenost FROM " + TABLE_NAME_LOCATION_DISTANCE + " WHERE lokacija = t.lokacija) " \
        "FROM (" \
        "SELECT t.*, ROW_NUMBER() OVER() AS seqnum, " \
        "COUNT(*) OVER() AS cnt FROM " + TABLE_NAME + " t " \
        "WHERE " + ROW_OFFER + " = '" + ROW_OFFER_FLAT + "' " \
        "AND " + ROW_PROPERTY + " = '" + ROW_PROPERTY_SALE + "' " \
        "AND SUBSTRING_INDEX(" + ROW_LOCATION + ", ',', 1) = 'Beograd') t " \
        "WHERE seqnum <= cnt * 0.7;"
    cursor.execute(q)
    results = cursor.fetchall()
    global n, m, K, x, y
    x, y, z = process_all_data_from_database(results)
    m = len(x)
    var_k = math.trunc(math.sqrt(m))
    if K == -1:
        if var_k % 2 == 1:
            K = var_k
        else:
            K = var_k + 1


def test_data():
    q = "SELECT t.*, (SELECT udaljenost FROM " + TABLE_NAME_LOCATION_DISTANCE + " WHERE lokacija = t.lokacija) " \
        "FROM (" \
        "SELECT t.*, ROW_NUMBER() OVER() AS seqnum, " \
        "COUNT(*) OVER() AS cnt FROM " + TABLE_NAME + " t " \
        "WHERE " + ROW_OFFER + " = '" + ROW_OFFER_FLAT + "' " \
        "AND " + ROW_PROPERTY + " = '" + ROW_PROPERTY_SALE + "' " \
        "AND SUBSTRING_INDEX(" + ROW_LOCATION + ", ',', 1) = 'Beograd') t " \
        "WHERE seqnum > cnt * 0.7;"
    cursor.execute(q)
    results = cursor.fetchall()
    global test_data_x, test_data_y, test_data_row_data_z
    test_data_x, test_data_y, test_data_row_data_z = process_all_data_from_database(results)


def test():
    # e(other_condition="and tip_nekretnine = 'Stan' and SUBSTRING_INDEX(Lokacija, ',', 1) = 'Beograd' ", type_of_real_estate="stanova u Beogradu", path_and_name_of_file=PATH_TO_MAIN_5_VISUAL_REPRESENTATION)
    test_data()
    table = prettytable.PrettyTable(['Euclidean', 'Da li je dobro predvidjanje', 'Manhattan', 'Da li je dobro predvidjanje ', 'Povrsina stana', 'Stanje nekretnine', 'Godina izgradnje', 'Sprat', 'Spratnost', 'Uknjizenost', 'Broj soba', 'Parking', 'Lift', 'Udaljenost lokacije', 'Cena'])
    table.align["Euclidean"] = "l"
    table.padding_width = 1
    for i in range(0, len(test_data_x)):
        euclidean_result = euclidean_distance(test_data_x[i], test_data_y[i])
        manhattan_result = manhattan_distance(test_data_x[i], test_data_y[i])
        table.add_row(euclidean_result + manhattan_result + test_data_row_data_z[i])
        print(i, euclidean_result + manhattan_result)
    print(table)
    print("\n")
    with open(PATH_TO_MAIN_5_RESULTS_FOR_TESTING_SET, 'w') as w:
        w.write(str(table))


def get_class_from_distance(z, w, euclidean):
    var_x = []
    for i in range(0, m):
        distance = 0
        for j in range(0, n):
            if euclidean:
                distance = distance + math.pow(x[i][j] - z[j], 2)
            else:
                distance = distance + abs(x[i][j] - z[j])
        if euclidean:
            distance = math.sqrt(distance)
        var_x.append([x[i][n], distance])
    for i in range(0, m - 1):
        for j in range(i + 1, m):
            if var_x[i][1] > var_x[j][1]:
                p = var_x[i]
                var_x[i] = var_x[j]
                var_x[j] = p
    data_class = []
    for i in range(0, 5):
        data_class.append(0)
    for i in range(0, K):
        data_class[var_x[i][0]] = data_class[var_x[i][0]] + 1
    class_max_number_of_neighbours = 0
    class_index = 0
    for i in range(0, 5):
        if data_class[i] > class_max_number_of_neighbours:
            class_max_number_of_neighbours = data_class[i]
            class_index = i
    class_is_well_predicted = False
    if class_index == 4:
        predicted_class = '>= 200 000€'
        if w >= 200000:
            class_is_well_predicted = True
    elif class_index == 3:
        predicted_class = '[150 000€, 199 999€]'
        if 150000 <= w <= 199999:
            class_is_well_predicted = True
    elif class_index == 2:
        predicted_class = '[100 000€, 149 999€]'
        if 100000 <= w <= 149999:
            class_is_well_predicted = True
    elif class_index == 1:
        predicted_class = '[50 000€, 99 999€]'
        if 50000 <= w <= 99999:
            class_is_well_predicted = True
    else:
        predicted_class = '<= 49 999€'
        if w <= 49999:
            class_is_well_predicted = True
    return [predicted_class, class_is_well_predicted]


def euclidean_distance(z, w):
    return get_class_from_distance(z, w, True)


def manhattan_distance(z, w):
    return get_class_from_distance(z, w, False)


def input_form():
    global K
    K = -1
    val = str(input("Ukoliko zelite automatsku vrednost faktora K pritisnite enter, u suprotnom unesite zeljenju vrednost faktora K "))
    val = val.split('\n')[0]
    if val != '':
        try:
            K = int(val)
        except ValueError:
            print('Niste uneli dobar format faktora K')
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
    training_data()
    z = [square_footage, object_condition, construction_year, floor, num_of_floors, registration, num_of_rooms, parking, elevator, location_distance]
    ed = euclidean_distance(z, 500000)
    print("kNN koriscenjem Euklidovog rastojanja predvidja da je cena stana: ", ed[0])
    md = manhattan_distance(z, 500000)
    print("kNN koriscenjem Menhten rastojanja predvidja da je cena stana: ", md[0])


db = mysql.connect(
    host="localhost",
    user="root",
    password="123#Madmin",
    database=DATABASE_NAME,
)
cursor = db.cursor()
alpha = float(0.003)
y = []
x = []
test_data_y = []
test_data_x = []
test_data_row_data_z = []
global m
n = 10
K = -1
min_year, max_year = get_min_max_year()
# training_data()
# test()
input_form()


# +dodeliti training podacima klasu
# +normalizovati podatke
# +izracunati k
# +proci kroz podatke izracunati euklidsko rastojanje
# +proci kroz podatke izracunati menhetn rastojanje
# +naci k najblizih suseda
# +odrediti kojoj klasi pripada
# +test podaci da li je dobijena klasifikacija tacna
# +test podaci uspesnost sa euklid/menhtenom normalizacijom/standard
# +forma za promenu k
# +forma za unos podatka
# +izlaz
