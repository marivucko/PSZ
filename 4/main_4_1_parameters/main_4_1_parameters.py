import math
import mysql.connector as mysql
from numpy import loadtxt, savetxt
from prettytable import prettytable
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import os

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

PATH_TO_LINEAR_REGRESSION_PARAMETERS = 'H:\Serije\PSZ\Projekat\src\main_4\main_4_2_paramteres\w.dat'


def fill_min_max_arrays(query, minimums, maximums):
    cursor.execute(query)
    results = cursor.fetchall()
    minimums.append(results[0][0])
    maximums.append(results[0][1])
    return minimums, maximums


def fill_minimums_maximums():
    minimums = []
    maximums = []
    q = ["select min(convert(left(kvadratura, char_length(kvadratura)-3), signed integer)), max(convert(left(kvadratura, char_length(kvadratura)-3), signed integer)) from nekretnina t where tip_nekretnine = 'Stan' and tip_ponude = 'Prodaja' and substring_index(Lokacija, ',', 1) = 'Beograd' and left(kvadratura, char_length(kvadratura)-3) REGEXP '^[0-9]+$';",
        "select min(convert(broj_soba, signed integer)), max(convert(broj_soba, signed integer)) from nekretnina t where tip_nekretnine = 'Stan' and tip_ponude = 'Prodaja' and substring_index(Lokacija, ',', 1) = 'Beograd' and broj_soba REGEXP '^[0-9]+$';",
         "select min(convert(replace(udaljenost, ' ', ''), float)), max(convert(replace(udaljenost, ' ', ''), float)) from udaljenosti;"]
    minimums, maximums = fill_min_max_arrays(q[0], minimums, maximums)      # square footage
    # minimums.append(-2)      # object_condition
    # maximums.append(6)      # object_condition
    # minimums.append(int(min_year))      # construction_year
    # maximums.append(int(max_year))      # construction_year
    # minimums.append(-1)      # floor
    # maximums.append(37)      # floor
    # minimums.append(-1)      # num_of_floors
    # maximums.append(44)      # num_of_floors
    # minimums.append(-1)      # registration
    # maximums.append(1)      # registration
    # minimums, maximums = fill_min_max_arrays(q[1], minimums, maximums)  # num_of_rooms
    # minimums.append(-1)  # parking
    # maximums.append(1)  # parking
    # minimums.append(-1)  # elevator
    # maximums.append(1)  # elevator
    # minimums, maximums = fill_min_max_arrays(q[2], minimums, maximums)  # location_distance
    return minimums, maximums


def convert_object_condition_str_to_int(object_condition):
    if object_condition == 'Namenjeno rušenju':
        return -2
    if object_condition == 'Delimicna rekonstrukcija':
        return -1
    if object_condition == 'Kompletna rekonstrukcija':
        return 0
    if object_condition == '':
        return 0
    if object_condition == 'Izvorno stanje':
        return 1
    if object_condition == 'Standardna gradnja':
        return 2
    elif object_condition == 'U izgradnji':
        return 3
    elif object_condition == 'Završena izgradnja':
        return 4
    elif object_condition == 'U pripremi':
        return 5
    elif object_condition == 'Novogradnja':
        return 6
    else:
        return 0


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
        object_condition = convert_object_condition_str_to_int(object_condition)
        if construction_year == '':
            construction_year = (float(min_year) + float(max_year)) / 2
        else:
            construction_year = float(construction_year)
    except ValueError:
        return None
    if floor == '-':
        floor = 1
    if floor == 'Visoko prizemlje':
        floor = 0.5
    if floor == 'Prizemlje':
        floor = 0
    if floor == 'Suteren':
        floor = -1
    floor = float(floor)
    if num_of_floors == '-':
        num_of_floors = floor
    if num_of_floors == 'Visoko prizemlje':
        num_of_floors = 0.5
    if num_of_floors == 'Prizemlje':
        num_of_floors = 0
    if num_of_floors == 'Suteren':
        num_of_floors = -1
    num_of_floors = float(num_of_floors)
    registration = 1 if registration == 'Da' else -1
    if num_of_rooms == '-':
        num_of_rooms = 0.5
    num_of_rooms = float(num_of_rooms)
    parking = 1 if parking == 'Da' else -1
    elevator = 1 if elevator == 'Da' else -1
    location_distance = float(location_distance.replace(',', '.'))
    # processed_data = [square_footage, object_condition, construction_year, floor, num_of_floors, registration, num_of_rooms, parking, elevator, price, location_distance]
    processed_data = [square_footage, price]
    return row_data, processed_data


def process_all_data_from_database(results):
    xx = []
    yy = []
    zz = []
    for result in results:
        try:
            row_data, processed_data = process_one_row_from_database(result)
            # square_footage, object_condition, construction_year, floor, num_of_floors, registration, num_of_rooms, parking, elevator, price, location_distance = processed_data
            square_footage, price = processed_data
        except TypeError:
            continue
        # xx.append([square_footage, object_condition, construction_year, floor, num_of_floors, registration, num_of_rooms, parking, elevator, location_distance])
        xx.append([square_footage])
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
    global x, y, minimums_of_variables, maximums_of_variables
    x, y, z = process_all_data_from_database(results)
    global n, m
    m = len(x)
    print(m, 'm')
    print(len(y), 'len(y)')
    n = len(minimums_of_variables)
    normalize_training_set()


def test_data():
    q = "SELECT t.*, (SELECT udaljenost FROM " + TABLE_NAME_LOCATION_DISTANCE + " WHERE lokacija = t.lokacija) " \
        "FROM (" \
                "SELECT t.*, ROW_NUMBER() OVER() AS seqnum, " \
                "COUNT(*) OVER() AS cnt FROM " + TABLE_NAME + " t " \
                "WHERE " + ROW_OFFER + " = '" + ROW_OFFER_FLAT + "' " \
                "AND " + ROW_PROPERTY + " = '" + ROW_PROPERTY_SALE + "' " \
                "AND SUBSTRING_INDEX(" + ROW_LOCATION + ", ',', 1) = 'Beograd' ) t " \
        "WHERE seqnum > cnt * 0.7;"
    cursor.execute(q)
    results = cursor.fetchall()
    table = prettytable.PrettyTable(['Predvidena vrednost', 'Prava vrednost', 'Greška', 'Povrsina stana', 'Stanje nekretnine', 'Godina izgradnje', 'Sprat', 'Spratnost', 'Uknjizenost', 'Broj soba', 'Parking', 'Lift', 'Udaljenost lokacije'])
    global test_data_x, test_data_y
    test_data_x, test_data_y, test_data_row_data_z = process_all_data_from_database(results)
    order = []
    normalize_test_set()
    k = 0
    for i in range(0, len(test_data_x)):
        predicted_value, real_value, error = calculate(test_data_x[i], test_data_y[i])
        if predicted_value < 0:
            k += 1
        order.append([round(predicted_value, 2), real_value, round(error, 2)] + test_data_row_data_z[i][:-1])
    for i in range(0, len(test_data_x) - 1):
        for j in range(i + 1, len(test_data_x)):
            if abs(order[i][2]) > abs(order[j][2]):
                p = order[i]
                order[i] = order[j]
                order[j] = p
    for i in range(0, len(test_data_x)):
        table.add_row(order[i])
    print(table)
    print(k)


def j_mse():
    mse = 0
    for i in range(0, m):
        mse = mse + math.pow(h(x, i) - y[i], 2)
    mse = mse / (2 * m)
    return mse


def h(x, i):
    global n
    sum_ = w[0]
    for j in range(0, n):
        sum_ = sum_ + x[i][j] * w[j + 1]
    return sum_


def sum_h_minus_y(x, j):
    sum_ = float(0)
    if j == 0:
        for i in range(0, m):
            sum_ = sum_ + (h(x, i) - y[i])
    else:
        for i in range(0, m):
            sum_ = sum_ + (h(x, i) - y[i]) * x[i][j - 1]
    return sum_


def gradient_descent():
    global w
    # w = [1156047.3511377622, 1229295.0771738398, 11671.611811556631, -4356.648419947488, 28471.27552830456, 136023.82395799138, -2683.955689783485, -53050.2359638173, 6843.217635579122, 3667.2800039516824, -212948.7692809165]
    if os.path.isfile(PATH_TO_LINEAR_REGRESSION_PARAMETERS):
        w = loadtxt(PATH_TO_LINEAR_REGRESSION_PARAMETERS, comments="#", delimiter=",", unpack=False)
        return
    training_data()
    temp = []
    for i in range(0, n + 1):
        w.append(float(0))
        temp.append(float(0))
    temp = [1004376.3436598646, 956421.6706603648]
    w = [1004378.4977231951, 956424.1292174953]
    mse_curr = j_mse()
    k = 0
    d = -1
    while d < 0:
        for j in range(0, n + 1):
            temp[j] = w[j] - alpha / m * sum_h_minus_y(x, j)
        for i in range(0, n + 1):
            w[i] = temp[i]
        mse_prev = mse_curr
        mse_curr = j_mse()
        d = mse_curr - mse_prev
        k = k + 1
        print(k, '. w after', w, d)
    w = temp
    savetxt(PATH_TO_LINEAR_REGRESSION_PARAMETERS, w, delimiter=',')


def get_location_distance_for_one_data(location):
    url = "https://www.google.com/maps/dir/%D0%A2%D1%80%D0%B3+%D1%80%D0%B5%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B5,+%D0%91%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D0%B4/%D0%A2%D1%80%D0%B3+%D1%80%D0%B5%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B5,+%D0%91%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D0%B4+11000/@44.8105531,20.4648601,15z/data=!4m14!4m13!1m5!1m1!1s0x475a7ab25c703261:0x99b65b127891b036!2m2!1d20.4599624!2d44.816088!1m5!1m1!1s0x475a7ab2453c4ba1:0xb81037438bba0036!2m2!1d20.4603199!2d44.8162551!3e0"
    PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver_win32 (2)\chromedriver.exe"
    options = Options()
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(PATH, options=options)
    driver.set_page_load_timeout(300)
    try:
        driver.get(url)
        driver.find_element_by_class_name("tactile-searchbox-input").clear()
        driver.find_element_by_class_name("tactile-searchbox-input").send_keys(location)
        driver.find_elements_by_class_name("nhb85d-BIqFsb")[0].click()
        time.sleep(5)
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


def get_distance(driver, location):
    driver.find_element_by_class_name("tactile-searchbox-input").clear()
    if location == "Beograd, Novi Beograd Blok 30 (B92)":
        location = "Beograd, Novi Beograd Blok 30"
    driver.find_element_by_class_name("tactile-searchbox-input").send_keys(location)
    driver.find_elements_by_class_name("nhb85d-BIqFsb")[0].click()
    time.sleep(2)
    distance = driver.find_elements_by_xpath("//div[@class='xB1mrd-T3iPGc-iSfDt-ij8cu']//div//div//div//div")[0].text
    if distance.split()[1] == 'm':
        distance = str(float(distance.split()[0]) * 0.001)
    else:
        distance = distance.split()[0]
    print(distance)
    cursor.execute("INSERT INTO " + TABLE_NAME_LOCATION_DISTANCE +
                   "(lokacija, udaljenost) VALUES "
                   "('" + location + "', '" + distance + "' )")
    db.commit()


def get_location_distance_from_center(results):
    cursor.execute("DROP TABLE IF EXISTS " + TABLE_NAME_LOCATION_DISTANCE)
    db.commit()
    cursor.execute(
        "CREATE TABLE " + TABLE_NAME_LOCATION_DISTANCE + "(" +
        "id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, "
        "lokacija VARCHAR(255), "
        "udaljenost VARCHAR(255)"
        ")"
    )
    db.commit()
    url = "https://www.google.com/maps/dir/%D0%A2%D1%80%D0%B3+%D1%80%D0%B5%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B5,+%D0%91%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D0%B4/%D0%A2%D1%80%D0%B3+%D1%80%D0%B5%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B5,+%D0%91%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D0%B4+11000/@44.8105531,20.4648601,15z/data=!4m14!4m13!1m5!1m1!1s0x475a7ab25c703261:0x99b65b127891b036!2m2!1d20.4599624!2d44.816088!1m5!1m1!1s0x475a7ab2453c4ba1:0xb81037438bba0036!2m2!1d20.4603199!2d44.8162551!3e0"
    PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
    options = Options()
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(PATH, options=options)
    driver.set_page_load_timeout(300)
    try:
        print(len(results), '***')
        driver.get(url)
        for result in results:
            print(result[0])
            get_distance(driver, result[0])
        #driver.close()
    except WebDriverException as e:
        print('greska')
        print(e)


def get_table_of_location_distance_from_center():
    q = "SELECT distinct Lokacija " \
        "FROM " + TABLE_NAME + " " \
        "WHERE tip_nekretnine = 'Stan' " \
        "AND SUBSTRING_INDEX(Lokacija, ',', 1) = 'Beograd' " \
        "order by lokacija"
    cursor.execute(q)
    results = cursor.fetchall()
    get_location_distance_from_center(results)


def normalize_training_set():
    for i in range(0, m):
        print('***', len(x[i]))
        for j in range(0, n):
            x[i][j] = ((x[i][j] - minimums_of_variables[j]) / (maximums_of_variables[j] - minimums_of_variables[j])) * 2 - 1
    for i in range(0, n):
        print("min: ", minimums_of_variables[i], " max: ", maximums_of_variables[i])


def normalize_test_set():
    for i in range(0, len(test_data_x)):
        for j in range(0, n):
            if maximums_of_variables[j] == minimums_of_variables[j]:
                test_data_x[i][j] = 0
            else:
                test_data_x[i][j] = ((test_data_x[i][j] - minimums_of_variables[j]) / (maximums_of_variables[j] - minimums_of_variables[j])) * 2 - 1


def calculate(xx, yy):
    value = w[0]
    for i in range(0, n):
        value = value + w[i + 1] * xx[i]
    return [value, yy, value - yy]


def input_form():
    square_footage = float(input("Unesite kvadraturu stana: "))
    input_data = [square_footage]
    for i in range(0, n):
        input_data[i] = ((input_data[i] - minimums_of_variables[i]) / (maximums_of_variables[i] - minimums_of_variables[i])) * 2 - 1
    print("Višestruka linarna regersija korišćenjem gradijentnog spusta predviđa da je cena stana: ", round(calculate(input_data, 0)[0], 2), "EUR-a.")


db = mysql.connect(
    host="localhost",
    user="root",
    password="123#Madmin",
    database=DATABASE_NAME,
)
cursor = db.cursor()
alpha = float(0.003)
w = []
y = []
x = []
global m
min_year, max_year = get_min_max_year()
minimums_of_variables, maximums_of_variables = fill_minimums_maximums()
n = len(minimums_of_variables)
gradient_descent()
# training_data()
test_data()
input_form()


# +racunanje udaljenosti lokacije
# +kako izabrati alpha 0.00001 0.00003 0.0001 0.0003 0.001 0.003 0.01 0.03 0.1 0.3 1
# +x prebaciti u ospeg -1,1
# +kako izabrati w0 w1 w2 ...
# + azuriranje w0 w1 ...
# + kada je konvergiralo
# uporedjivanje sa gotov funkcijom
# + unose podataka za koje zelimo da predvidimo vrednosti
# + izlaz y
# 1089275 . w after [1259989.8587517617, 1248168.1673004918] -7.963180541992188e-05
# 1089276 . w after [1259989.8589741471, 1248168.167554313] 2.86102294921875e-06