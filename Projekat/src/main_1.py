import time
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from enum import Enum
import mysql.connector as mysql

DATABASE_NAME = 'PSZ_baza'
TABLE_NAME = 'Nekretnina'


class Property:
    def __init__(self, property_type, offer_type, location, square_footage, object_condition, construction_year, land_area, floor,
                 number_of_floors, registration, type_of_heating, number_of_rooms, number_of_bathrooms, parking,
                 elevator, terrace, balcony, loggia):
        self.property_type = property_type
        self.offer_type = offer_type
        self.location = location
        self.square_footage = square_footage
        self.object_condition = object_condition
        self.construction_year = construction_year
        self.land_area = land_area
        self.floor = floor
        self.number_of_floors = number_of_floors
        self.registration = registration
        self.type_of_heating = type_of_heating
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.parking = parking
        self.elevator = elevator
        self.terrace = terrace
        self.balcony = balcony
        self.loggia = loggia

    def to_string(self):
        return ' | Tip nekretine: ' + self.property_type.value + ' | Tip ponude: ' + self.offer_type.value + \
               ' | Lokacija: ' + self.location + ' | Kvadratura: ' + self.square_footage + \
               ' | Stanje objekta: ' + self.object_condition + ' | Godina izgradnje: ' + self.construction_year + \
               ' | Površina zemljišta: ' + self.land_area + ' | Sprat: ' + self.floor + \
               ' | Ukupna spratnost: ' + self.number_of_floors + ' | Uknjiženost: ' + self.registration + \
               ' | Tip grejanja: ' + self.type_of_heating + ' | Broj soba: ' + self.number_of_rooms + \
               ' | Broj kupatila: ' + self.number_of_bathrooms + ' | Parking: ' + self.parking + \
               ' | Lift: ' + self.elevator + ' | Terasa: ' + self.terrace + ' | Balkon: ' + self.balcony + \
               ' | Loda: ' + self.loggia


class OfferType(Enum):
    SALE = 'Prodaja'
    RENT = 'Izdavanje'


class PropertyType(Enum):
    FLAT = 'Stan'
    HOUSE = 'Kuća'


def get_element_from_next_line_of_xpath(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath).text.splitlines()[1]
    except NoSuchElementException:
        return ''


def get_element_by_xpath(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath).text
    except NoSuchElementException:
        return ''


def get_does_element_exist_by_xpath(driver, xpath):
    try:
        if driver.find_element_by_xpath(xpath):
            return 'Da'
        else:
            return 'Ne'
    except NoSuchElementException:
        return 'Ne'


def go_to_sale_or_rent_page(offer_type, property_type, db, cursor):
    driver = webdriver.Chrome(PATH, options=options)
    driver.set_page_load_timeout(300)
    try:
        driver.get(url)
    except WebDriverException as e:
        print('greska')
        print(e)
    print(property_type)
    print(driver.current_url)
    content = driver.find_element_by_xpath('//body')
    if offer_type == OfferType.RENT:
        content.find_elements_by_class_name("form-check-input")[1].click()
    content.find_element_by_xpath("//div[@class='dropdown']").click()
    if property_type == PropertyType.HOUSE:
        content.find_elements_by_xpath("//div[@class='ml-2']")[1].click()
    button = content.find_element_by_xpath("//button[@class='btn btn-primary adv-search-form-search-btn']")
    button.click()
    while True:
        window_after = driver.window_handles[0]
        driver.switch_to.window(window_after)
        time.sleep(0.5)
        links_on_the_page = []
        current = driver.current_window_handle
        for links in driver.find_elements_by_xpath("//h2[@class='offer-title text-truncate w-100']"):
            links_on_the_page.append(links.find_element_by_css_selector('a').get_attribute('href'))
        for row_offer in links_on_the_page:
            print(row_offer)
            try:
                driver.execute_script("window.open('')")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(row_offer)
                content = driver.find_element_by_xpath('//body')
                price = content.find_element_by_xpath("//div[@class='stickyBox']//h4").text.partition('\n')[0]
                location = content.find_element_by_xpath("//div[@class='stickyBox']").find_elements_by_css_selector('h3')[0].text
                square_footage = get_element_from_next_line_of_xpath(content, "//div[@class='property__main-details']//li[contains(.,'Kvadratura:')]")
                object_condition = get_element_by_xpath(content, "//div[@class='property__amenities']//ul//li[contains(.,'Stanje nekretnine:')]//strong")
                construction_year = get_element_by_xpath(content, "//div[@class='property__amenities']//li[contains(.,'Godina izgradnje:')]//strong")
                land_area = ''
                if property_type == PropertyType.HOUSE:
                    land_area = get_element_from_next_line_of_xpath(content, "//div[@class='property__main-details']//li//span[contains(., 'Površina zemljišta:')]")
                floor = ''
                number_of_floors = ''
                if property_type == PropertyType.FLAT:
                    try:
                        floor, number_of_floors = content.find_element_by_xpath(
                            "//div[@class='property__main-details']//li//span[contains(., 'Sprat:')]").text.splitlines()[1].split(' / ')
                    except NoSuchElementException:
                        floor = ''
                        number_of_floors = ''
                registration = get_element_from_next_line_of_xpath(content, "//div[@class='property__main-details']//li//span[contains(., 'Uknjiženo:')]")
                type_of_heating = get_element_from_next_line_of_xpath(content, "//div[@class='property__main-details']//li//span[contains(., 'Grejanje:')]")
                number_of_rooms = get_element_from_next_line_of_xpath(content, "//div[@class='property__main-details']//li//span[contains(., 'Sobe:')]")
                number_of_bathrooms = get_element_by_xpath(content, "//div[@class='property__amenities']//li[contains(.,'Broj kupatila:')]//strong")
                parking = get_element_from_next_line_of_xpath(content, "//div[@class='property__main-details']//li//span[contains(., 'Parking:')]")
                elevator = get_does_element_exist_by_xpath(content, "//div[@class='property__amenities']//li[contains(., 'Lift')]")
                terrace = get_does_element_exist_by_xpath(content, "//div[@class='property__amenities']//li[contains(., 'Terasa')]")
                balcony = get_does_element_exist_by_xpath(content, "//div[@class='property__amenities']//li[contains(., 'Balkon')]")
                loggia = get_does_element_exist_by_xpath(content, "//div[@class='property__amenities']//li[contains(., 'Loda')]")
                print(property_type.name, offer_type.name, location, square_footage, object_condition,
                      construction_year, land_area, floor, number_of_floors, registration, type_of_heating,
                      number_of_rooms, number_of_bathrooms, parking, elevator, terrace, balcony, loggia)
                property_ = Property(property_type, offer_type, location, square_footage, object_condition,
                                     construction_year, land_area, floor, number_of_floors, registration,
                                     type_of_heating, number_of_rooms, number_of_bathrooms, parking, elevator, terrace,
                                     balcony, loggia)
                print(property_.to_string())
                row_offer_url = (row_offer[:255]) if len(row_offer) > 255 else row_offer
                cursor.execute("INSERT INTO " + TABLE_NAME +
                                "(tip_nekretnine, tip_ponude, lokacija, kvadratura, stanje_nekretnine, godina_izgradnje, povrsina_zemljista, "
                                "sprat, ukupna_spratnost, uknjizenost, tip_grejanja, broj_soba, broj_kupatila, parking, "
                                "lift, terasa, balkon, lodja, url, cena) VALUES ('" + property_type.value + "', '" + offer_type.value +
                                "', '" + location + "', '" + square_footage + "', '" + object_condition + "', '" + construction_year +
                                "', '" + land_area + "', '" + floor + "', '" + number_of_floors + "', '" + registration +
                                "', '" + type_of_heating + "', '" + number_of_rooms + "', '" + number_of_bathrooms +
                                "', '" + parking + "', '" + elevator + "', '" + terrace + "', '" + balcony + "', '" + loggia +
                                "', '" + row_offer_url + "', '" + price + "' )")
                db.commit()
                driver.close()
                driver.switch_to.window(current)
            except Exception as e:
                print('Error---', datetime.now().strftime("%H:%M:%S"), '\n', e)
                driver = webdriver.Chrome(PATH, options=options)
                driver.set_page_load_timeout(300)
                driver.get(current)
                time.sleep(3)
                driver.refresh()
                continue
        try:
            next_page_url = driver.find_element_by_xpath("//div[@class='col-5 col-lg-3 mt-2']//a").get_attribute('href')
            driver.get(next_page_url)
        except NoSuchElementException:
            break
    print('-----')
    driver.quit()


def connect_to_db_and_delete_database_if_exists():
    db_ = mysql.connect(
        host="localhost",
        user="root",
        password="123#Madmin",
    )

    cursor_ = db_.cursor()
    cursor_.execute("DROP DATABASE IF EXISTS " + DATABASE_NAME)
    cursor_.execute("CREATE DATABASE " + DATABASE_NAME)
    db_.close()


def connect_to_db_and_create_database():
    db_ = mysql.connect(
        host="localhost",
        user="root",
        password="123#Madmin",
        database=DATABASE_NAME,
    )
    cursor_ = db_.cursor()
    cursor_.execute(
        "CREATE TABLE " + TABLE_NAME + "(" +
        "id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, "
        "tip_nekretnine VARCHAR(255), "
        "tip_ponude VARCHAR(255), "
        "lokacija VARCHAR(255), "
        "kvadratura VARCHAR(255), "
        "stanje_nekretnine VARCHAR(255), "
        "godina_izgradnje VARCHAR(5), "
        "povrsina_zemljista VARCHAR(255), "
        "sprat VARCHAR(255), "
        "ukupna_spratnost VARCHAR(2), "
        "uknjizenost VARCHAR(2), "
        "tip_grejanja VARCHAR(255), "
        "broj_soba VARCHAR(3), "
        "broj_kupatila VARCHAR(3), "
        "parking VARCHAR(2), "
        "lift VARCHAR(2), "
        "terasa VARCHAR(2), "
        "balkon VARCHAR(2), "
        "lodja VARCHAR(2), "
        "url VARCHAR(255), "
        "cena VARCHAR(255)"
        ")"
    )
    return db_, cursor_


def connect_to_db():
    db_ = mysql.connect(
        host="localhost",
        user="root",
        password="123#Madmin",
        database=DATABASE_NAME,
    )
    cursor_ = db_.cursor()
    return db_, cursor_


PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver_win32_98\chromedriver.exe"
url = 'https://www.nekretnine.rs/'
options = Options()
options.add_argument('--no-sandbox')

connect_to_db_and_delete_database_if_exists()
db, cursor = connect_to_db_and_create_database()

go_to_sale_or_rent_page(OfferType.SALE, PropertyType.HOUSE, db, cursor)
go_to_sale_or_rent_page(OfferType.RENT, PropertyType.HOUSE, db, cursor)
go_to_sale_or_rent_page(OfferType.RENT, PropertyType.FLAT, db, cursor)
go_to_sale_or_rent_page(OfferType.SALE, PropertyType.FLAT, db, cursor)
db.close()
