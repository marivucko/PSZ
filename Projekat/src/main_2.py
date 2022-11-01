import mysql.connector as mysql
import prettytable

DATABASE_NAME = 'PSZ_baza'
TABLE_NAME = 'Nekretnina'
ROW_PROPERTY = 'tip_ponude'
ROW_PROPERTY_SALE = 'Prodaja'
ROW_PROPERTY_RENT = 'Izdavanje'
ROW_LOCATION = 'Lokacija'
ROW_OFFER = 'tip_nekretnine'
ROW_OFFER_FLAT = 'Stan'
ROW_OFFER_HOUSE = 'Kuća'
ROW_REGISTRATION = 'Uknjizenost'
ROW_REGISTRATION_REGISTERED = 'Da'
ROW_REGISTRATION_NOT_REGISTERED = 'Ne'
ROW_PRICE = 'Cena'
ROW_SQUARE_FOOTAGE = 'Kvadratura'
ROW_OBJECT_CONDITION = 'stanje_nekretnine'
ROW_TYPE_OF_HEATING = 'tip_grejanja'
ROW_CONSTRUCTION_YEAR = 'godina_izgradnje'
ROW_NUMBER_OF_ROOMS = 'broj_soba'
ROW_NUMBER_OF_BATHROOMS = 'broj_kupatila'
ROW_LAND_AREA = 'povrsina_zemljista'
ROW_FLOOR = 'sprat'
ROW_NUM_OF_FLOORS = 'ukupna_spratnost'
ROW_PARKING = 'parking'
ROW_ELEVATOR = 'lift'
ROW_TERRACE = 'terasa'
ROW_BALCONY = 'balkon'
ROW_URL = 'url'


def get_first_row_data_from_query(query):
    cursor.execute(query)
    return cursor.fetchone()[0]


def print_all_data_from_query_to_table(columns, query):
    table = prettytable.PrettyTable(columns)
    cursor.execute(query)
    results = cursor.fetchall()
    for result in results:
        table.add_row(result)
    print(table)
    print("\n")


def print_all_data_from_query_except_id_to_table(columns, query):
    table = prettytable.PrettyTable(columns)
    cursor.execute(query)
    results = cursor.fetchall()
    for result in results:
        table.add_row(result[1:])
    print(table)
    print("\n")


def query_for_top_30_most_expensive_offers(offer_type):
    if offer_type == ROW_OFFER_HOUSE:
        select_query = "SELECT " + ROW_LOCATION + ", " + ROW_SQUARE_FOOTAGE + ", " + ROW_OBJECT_CONDITION + ", " + ROW_CONSTRUCTION_YEAR + ", " + ROW_LAND_AREA + ", " + \
           ROW_REGISTRATION + ", " + ROW_TYPE_OF_HEATING + ", " + ROW_NUMBER_OF_ROOMS + ", " + \
           ROW_NUMBER_OF_BATHROOMS + ", " + ROW_PARKING + ", " + ROW_ELEVATOR + ", " + ROW_TERRACE + ", " + ROW_BALCONY + ", " + ROW_PRICE + ", " + ROW_URL + " "
    else:
        select_query = "SELECT " + ROW_LOCATION + ", " + ROW_SQUARE_FOOTAGE + ", " + ROW_OBJECT_CONDITION + ", " + ROW_CONSTRUCTION_YEAR + ", " +  \
           ROW_FLOOR + ", " + ROW_NUM_OF_FLOORS + ", " + ROW_REGISTRATION + ", " + ROW_TYPE_OF_HEATING + ", " + ROW_NUMBER_OF_ROOMS + ", " + \
           ROW_NUMBER_OF_BATHROOMS + ", " + ROW_PARKING + ", " + ROW_ELEVATOR + ", " + ROW_TERRACE + ", " + ROW_BALCONY + ", " + ROW_PRICE + ", " + ROW_URL + " "
    return select_query + \
        "FROM " + TABLE_NAME + " " \
        "WHERE REPLACE(SUBSTRING_INDEX(" + ROW_PRICE + ", 'EUR', 1), ' ', '') REGEXP '^-?[0-9]+$' " \
        "AND " + ROW_OFFER + " = '" + offer_type + "' " \
        "ORDER BY CONVERT(REPLACE(SUBSTRING_INDEX(" + ROW_PRICE + ", 'EUR', 1), ' ', ''), " \
        "UNSIGNED INTEGER) " \
        "DESC LIMIT 30"


def query_for_top_100_largest_offers(offer_type):
    if offer_type == ROW_OFFER_HOUSE:
        select_query = "SELECT " + ROW_LOCATION + ", " + ROW_SQUARE_FOOTAGE + ", " + ROW_OBJECT_CONDITION + ", " + ROW_CONSTRUCTION_YEAR + ", " + ROW_LAND_AREA + ", " + \
           ROW_REGISTRATION + ", " + ROW_TYPE_OF_HEATING + ", " + ROW_NUMBER_OF_ROOMS + ", " + \
           ROW_NUMBER_OF_BATHROOMS + ", " + ROW_PARKING + ", " + ROW_ELEVATOR + ", " + ROW_TERRACE + ", " + ROW_BALCONY + ", " + ROW_PRICE + ", " + ROW_PROPERTY + ", " + ROW_URL + " "
    else:
        select_query = "SELECT " + ROW_LOCATION + ", " + ROW_SQUARE_FOOTAGE + ", " + ROW_OBJECT_CONDITION + ", " + ROW_CONSTRUCTION_YEAR + ", " + \
           ROW_FLOOR + ", " + ROW_NUM_OF_FLOORS + ", " + ROW_REGISTRATION + ", " + ROW_TYPE_OF_HEATING + ", " + ROW_NUMBER_OF_ROOMS + ", " + \
           ROW_NUMBER_OF_BATHROOMS + ", " + ROW_PARKING + ", " + ROW_ELEVATOR + ", " + ROW_TERRACE + ", " + ROW_BALCONY + ", " + ROW_PRICE + ", " + ROW_PROPERTY + ", " + ROW_URL + " "
    return select_query + \
        "FROM " + TABLE_NAME + " " \
        "WHERE SUBSTRING_INDEX(" + ROW_SQUARE_FOOTAGE + ", ' m²', 1) REGEXP '^-?[0-9]+$' " \
        "AND " + ROW_OFFER + " = '" + offer_type + "' " \
        "ORDER BY CONVERT(SUBSTRING_INDEX(" + ROW_SQUARE_FOOTAGE + ", 'm²', 1), " \
        "SIGNED INTEGER) " \
        "DESC LIMIT 100"


def query_rang_list_for_properties_in_2020(property_type):
    return "SELECT * " \
           "FROM " + TABLE_NAME + " " \
           "WHERE REPLACE(SUBSTRING_INDEX(" + ROW_PRICE + ", 'EUR', 1), ' ', '') REGEXP '^-?[0-9]+$' " \
           "AND " + ROW_PROPERTY + " = '" + property_type + "' " \
           "AND " + ROW_CONSTRUCTION_YEAR + " = '2020' " \
           "ORDER BY CONVERT(REPLACE(SUBSTRING_INDEX(" + ROW_PRICE + ", 'EUR', 1), ' ', ''), " \
           "UNSIGNED INTEGER) " \
           "DESC"


def query_for_top_30_number_of_rooms():
    return "SELECT * " \
        "FROM " + TABLE_NAME + " " \
        "WHERE " + ROW_NUMBER_OF_ROOMS + " REGEXP '^-?[0-9]+$' " \
        "ORDER BY " + ROW_NUMBER_OF_ROOMS + " " \
        "DESC LIMIT 30"


def query_for_top_30_largest_flats():
    return "SELECT * " \
        "FROM " + TABLE_NAME + " " \
        "WHERE REPLACE(SUBSTRING_INDEX(" + ROW_SQUARE_FOOTAGE + ", 'm²', 1), ' ', '') REGEXP '^-?[0-9]+$' " \
        "AND " + ROW_OFFER + " = '" + ROW_OFFER_FLAT + "' " \
        "ORDER BY CONVERT(REPLACE(SUBSTRING_INDEX(" + ROW_SQUARE_FOOTAGE + ", 'm²', 1), ' ', ''), " \
        "SIGNED INTEGER) " \
        "DESC LIMIT 30"


def query_for_top_30_largest_land_area():
    return "SELECT * " \
        "FROM " + TABLE_NAME + " " \
        "WHERE LEFT(" + ROW_LAND_AREA + ", CHAR_LENGTH(" + ROW_LAND_AREA + ")-3) REGEXP '^-?[0-9]+$' " \
        "AND " + ROW_OFFER + " = '" + ROW_OFFER_HOUSE + "' " \
        "ORDER BY (CASE " \
            "WHEN RIGHT(" + ROW_LAND_AREA + ", 2) = 'ar' THEN CONVERT(LEFT(" + ROW_LAND_AREA + ", CHAR_LENGTH(povrsina_zemljista)-3), SIGNED INTEGER)*100 " \
            "WHEN RIGHT(" + ROW_LAND_AREA + ", 2) = 'm²' THEN CONVERT(LEFT(" + ROW_LAND_AREA + ", CHAR_LENGTH(povrsina_zemljista)-3), SIGNED INTEGER) " \
            "ELSE 0 " \
        "END) " \
        "DESC LIMIT 30"


def a():
    number_of_properties_for_sale = get_first_row_data_from_query("SELECT COUNT(*) FROM " + TABLE_NAME + " WHERE " + ROW_PROPERTY + " = '" + ROW_PROPERTY_SALE + "'")
    number_of_properties_for_rent = get_first_row_data_from_query("SELECT COUNT(*) FROM " + TABLE_NAME + " WHERE " + ROW_PROPERTY + " = '" + ROW_PROPERTY_RENT + "'")
    print(f"2.a) Broj nekretinina za prodaju je {str(number_of_properties_for_sale)}, dok je broj nekretnina za iznajmljivanje {str(number_of_properties_for_rent)}.")


def b():
    q = "SELECT " \
        "SUBSTRING_INDEX(" + ROW_LOCATION + ", ',', 1), COUNT(*) " \
        "FROM " + TABLE_NAME + " "\
        "WHERE " + ROW_PROPERTY + " = '" + ROW_PROPERTY_SALE + "' " \
        "GROUP BY SUBSTRING_INDEX(" + ROW_LOCATION + ", ',', 1) " \
        "ORDER BY SUBSTRING_INDEX(" + ROW_LOCATION + ", ',', 1) "

    print("2.b) Lista gradova i broja nekretnina koje se prodaju u gradu")
    print_all_data_from_query_to_table(["Grad", "Broj nekretnina koje se prodaju u ovom gradu"], q)


def c():
    number_of_registered_flats = get_first_row_data_from_query("SELECT COUNT(*) FROM " + TABLE_NAME + " WHERE " + ROW_OFFER + " = '" + ROW_OFFER_FLAT + "' AND " + ROW_REGISTRATION + " = '" + ROW_REGISTRATION_REGISTERED + "'")
    number_of_not_registered_flats = get_first_row_data_from_query("SELECT COUNT(*) FROM " + TABLE_NAME + " WHERE " + ROW_OFFER + " = '" + ROW_OFFER_FLAT + "' AND " + ROW_REGISTRATION + " = '" + ROW_REGISTRATION_NOT_REGISTERED + "'")
    number_of_registered_houses = get_first_row_data_from_query("SELECT COUNT(*) FROM " + TABLE_NAME + " WHERE " + ROW_OFFER + " = '" + ROW_OFFER_HOUSE + "' AND " + ROW_REGISTRATION + " = '" + ROW_REGISTRATION_REGISTERED + "'")
    number_of_not_registered_houses = get_first_row_data_from_query("SELECT COUNT(*) FROM " + TABLE_NAME + " WHERE " + ROW_OFFER + " = '" + ROW_OFFER_HOUSE + "' AND " + ROW_REGISTRATION + "= '" + ROW_REGISTRATION_NOT_REGISTERED + "'")
    print("2.c) Broj uknjiženih kuća je " + str(number_of_registered_houses) + ', dok je broj neuknjiženih kuća ' + str(number_of_not_registered_houses) + '.')
    print("Broj uknjiženih stanova je " + str(number_of_registered_flats) + ', dok je broj neuknjiženih stanova ' + str(number_of_not_registered_flats) + '.')


def d():
    print("2.d) 30 najskupljih kuća:")
    print_all_data_from_query_to_table(["Lokacija kuće", "Kvadaratura", "Stanje nekretnine", "Godina izgradnje", "Površina zemljišta", "Uknjizenost", "Tip grejanja", "Broj soba", "Broj kupatila", "Parking", "Lift", "Terasa", "Balkon", "Cena", "url"], query_for_top_30_most_expensive_offers(ROW_OFFER_HOUSE))
    print("30 najskupljih stanova:")
    print_all_data_from_query_to_table(["Lokacija stana", "Kvadaratura", "Stanje nekretnine", "Godina izgradnje", "Sprat", "Ukupna spratnost", "Uknjizenost", "Tip grejanja", "Broj soba", "Broj kupatila", "Parking", "Lift", "Terasa", "Balkon", "Cena", "url"], query_for_top_30_most_expensive_offers(ROW_OFFER_FLAT))


def e():
    print("2.e) 100 najvećih kuća:")
    print_all_data_from_query_to_table(["Lokacija kuće", "Kvadaratura", "Stanje nekretnine", "Godina izgradnje", "Površina zemljišta", "Uknjizenost", "Tip grejanja", "Broj soba", "Broj kupatila", "Parking", "Lift", "Terasa", "Balkon", "Cena", "Tip ponude", "url"], query_for_top_100_largest_offers(ROW_OFFER_HOUSE))
    print("100 najvećih stanova:")
    print_all_data_from_query_to_table(["Lokacija stana", "Kvadaratura", "Stanje nekretnine", "Godina izgradnje", "Sprat", "Ukupna spratnost", "Uknjizenost", "Tip grejanja", "Broj soba", "Broj kupatila", "Parking", "Lift", "Terasa", "Balkon", "Cena", "Tip ponude", "url"], query_for_top_100_largest_offers(ROW_OFFER_FLAT))


def f():
    print("2.f) Rang lista nekretnina izgrađenih 2020. godine koje se prodaju:")
    print_all_data_from_query_except_id_to_table(["Tip nekretnine", "Tip ponude", "Lokacija", "Kvadaratura", "Stanje nekretnine", "Godina izgradnje", "Površina zemljišta", "Sprat", "Ukupna spratnost", "Uknjiženost", "Tip grejanja", "Broj soba", "Broj kupatila", "Parking", "Lift", "Terasa", "Balkon", "Lodja", "url", "Cena"], query_rang_list_for_properties_in_2020(ROW_PROPERTY_SALE))
    print("Rang lista nekretnina izgrađenih 2020. godine koje se iznajmljuju:")
    print_all_data_from_query_except_id_to_table(["Tip nekretnine", "Tip ponude", "Lokacija", "Kvadaratura", "Stanje nekretnine", "Godina izgradnje", "Površina zemljišta", "Sprat", "Ukupna spratnost", "Uknjiženost", "Tip grejanja", "Broj soba", "Broj kupatila", "Parking", "Lift", "Terasa", "Balkon", "Lodja", "url", "Cena"], query_rang_list_for_properties_in_2020(ROW_PROPERTY_RENT))


def g():
    print("2.g) Top 30 nekretnina koje imaju najveći broj soba unutar nekretnine:")
    print_all_data_from_query_except_id_to_table(["Tip nekretnine", "Tip ponude", "Lokacija", "Kvadaratura", "Stanje nekretnine", "Godina izgradnje", "Površina zemljišta", "Sprat", "Ukupna spratnost", "Uknjiženost", "Tip grejanja", "Broj soba", "Broj kupatila", "Parking", "Lift", "Terasa", "Balkon", "Lodja", "url", "Cena"], query_for_top_30_number_of_rooms())
    print("Top 30 stanova sa najvećom kvadraturom:")
    print_all_data_from_query_except_id_to_table(["Tip nekretnine", "Tip ponude", "Lokacija", "Kvadaratura", "Stanje nekretnine", "Godina izgradnje", "Površina zemljišta", "Sprat", "Ukupna spratnost", "Uknjiženost", "Tip grejanja", "Broj soba", "Broj kupatila", "Parking", "Lift", "Terasa", "Balkon", "Lodja", "url", "Cena"], query_for_top_30_largest_flats())
    print("Top 30 kuća sa najvećom zemljištem:")
    print_all_data_from_query_except_id_to_table(["Tip nekretnine", "Tip ponude", "Lokacija", "Kvadaratura", "Stanje nekretnine", "Godina izgradnje", "Površina zemljišta", "Sprat", "Ukupna spratnost", "Uknjiženost", "Tip grejanja", "Broj soba", "Broj kupatila", "Parking", "Lift", "Terasa", "Balkon", "Lodja", "url", "Cena"], query_for_top_30_largest_land_area())


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
g()