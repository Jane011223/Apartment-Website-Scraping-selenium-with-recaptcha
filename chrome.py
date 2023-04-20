from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver import ActionChains
#from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager


TARGET_URLs = ["https://www.portalinmobiliario.com/arriendo/departamento/particular/las-condes-metropolitana", "https://www.portalinmobiliario.com/arriendo/departamento/particular/nunoa-metropolitana", "https://www.portalinmobiliario.com/arriendo/departamento/particular/providencia-metropolitana"]
#LOGIN_URL = "https://www2.yapo.cl/login"

driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install())
driver.maximize_window()

list_xpath = '//*[@id="root-app"]/div/div[2]/section/ol'
name_publication_path = '//*[@id="header"]/div/div[2]/h1'
priceunit_path = '//*[@id="price"]/div/div/span/span[2]'
price_path = '//*[@id="price"]/div/div/span/span[3]'
sqr_meter_path = '//*[@id="highlighted_specs_res"]/div/div[1]/span'
number_bedroom_path = '//*[@id="highlighted_specs_res"]/div/div[2]/span'
number_bathroom_path = '//*[@id="highlighted_specs_res"]/div/div[3]/span'
address_path = '//*[@id="location"]/div/div[1]/div/p'
parking_path = '//*[@id="technical_specifications"]/div/div[1]/table/tbody/tr[6]/td/span'
description_path = '/html/body/app-root/adview-index/div/div[2]/div/div[1]/adview-description/div/p'
contact_name_path = '/html/body/app-root/adview-index/div/div[2]/div/div[2]/div/adview-publisher/div/adview-user-avatar/div/div[2]/p'
phone_btn_path = '/html/body/app-root/adview-index/div/div[2]/div/div[2]/div/adview-publisher/div/div[1]/adview-publisher-button/adview-phone-button/button'
phone_num_path = '/html/body/app-root/adview-index/div/div[2]/div/div[2]/div/adview-publisher/div/div[1]/adview-publisher-button/adview-phone-button/div/img[2]'
date_publication_path = '//*[@id="header"]/div/p'

name_publications = []
prices = []
sqr_meters = []
number_bedrooms = []
number_bathrooms = []
addresses = []
parkings = []
descriptions = []
contact_names = []
phone_numbers = []
date_publications = []

def log_in():
    driver.get(LOGIN_URL)
    time.sleep(10)
    email_field = driver.find_element(By.ID, 'email_input')
    password_field = driver.find_element(By.ID, 'password_input')
    
    email = "bastian@pluscapitalcl.com"
    password = "2023contodo"
    
    email_field.send_keys(email)
    password_field.send_keys(password)
    
    login_btn = driver.find_element(By.XPATH, '//*[@id="submit_button"]')
    login_btn.click()
    time.sleep(10)


def scrape_eachlink(link):
    print(link)
    
    name_publication = ""
    price = ""
    sqr_meter = ""
    number_bedroom = ""
    number_bathroom = ""
    address = ""
    parking = ""
    description = ""
    contact_name = ""
    phone_number = ""
    date_publication = ""
           
    try:
        driver.get(link)
        time.sleep(5)
        
        try:
            name_publication = driver.find_element(By.XPATH, name_publication_path).get_attribute('innerHTML')
        except:
            print("No such name_publication element")

        try:
            price = driver.find_element(By.XPATH, price_path).get_attribute('innerHTML')
        except:
            print("No such price element")

        try:
            sqr_meter = driver.find_element(By.XPATH, sqr_meter_path).get_attribute('innerHTML')
        except:
            print("No such sqr_meter element")

        try:
            number_bedroom = driver.find_element(By.XPATH, number_bedroom_path).get_attribute('innerHTML')
        except:
            print("No such number_bedroom element")

        try:
            number_bathroom = driver.find_element(By.XPATH, number_bathroom_path).get_attribute('innerHTML')
        except:
            print("No such number_bathroom element")

        try:
            address = driver.find_element(By.XPATH, address_path).get_attribute('innerHTML')
        except:
            print("No such address element")

        try:
            parking = driver.find_element(By.XPATH, parking_path).get_attribute('innerHTML')
        except:
            print("No such parking element")

        try:
            description = driver.find_element(By.XPATH, description_path).get_attribute('innerHTML')
        except:
            print("No such description element")

        try:
            contact_name = driver.find_element(By.XPATH, contact_name_path).get_attribute('innerHTML')
        except:
            print("No such contact_name element")

        try:
            date_publication = driver.find_element(By.XPATH, date_publication_path).get_attribute('innerHTML')
        except:
            print("No such date_publication element")

        try:
            phone_btn = driver.find_element(By.XPATH, phone_btn_path)
            phone_btn.click()
            time.sleep(10)
            phone_num_img = driver.find_element(By.XPATH, phone_num_path)
            phone_number = get_str_from_img(phone_num_img)
        except:
            print("Phone Number Error")
        
        print(phone_number)
        
        name_publications.append(name_publication)
        prices.append(price)
        sqr_meters.append(sqr_meter)
        number_bedrooms.append(number_bedroom)
        number_bathrooms.append(number_bathroom)
        addresses.append(address)
        parkings.append(parking)
        descriptions.append(description)
        contact_names.append(contact_name)
        phone_numbers.append(phone_number)
        date_publications.append(date_publication)
        add_expenses.append(add_expense)

    except:
        print("cannot reach this url")

def get_urls(links_array):
    # Scrape the data from the current page
    list = driver.find_element(By.XPATH, list_xpath)
    lists = list.find_elements(By.XPATH, './li')
    for i in range(len(lists)):
        list_item = lists[i]
        link = list_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
        links_array.append(link)

def scrape_site(url):
    driver.get(url)
    time.sleep(10)
    links_array = []

    get_urls(links_array)
    next_btn = driver.find_element(By.CLASS_NAME, "andes-pagination__button--next").find_element(By.TAG_NAME, 'a')
    while next_btn:
        url = next_btn.get_attribute('href')
        driver.get(url)
        time.sleep(10)
        get_urls(links_array)

        try:
            next_btn = driver.find_element(By.CLASS_NAME, "andes-pagination__button--next").find_element(By.TAG_NAME, 'a')
        except:
            next_btn = None

    
    for j in range(len(links_array)):
        link = links_array[j]
        scrape_eachlink(link)
    
    # #scrape_eachlink("https://new.yapo.cl/inmuebles/pieza-en-san-miguel_86589121")
    # df = pd.DataFrame({'Name publication': name_publications, 'prices': prices, 'sqr meters': sqr_meters, 'number of bedrooms': number_bedrooms, 'number of bathrooms': number_bathrooms, 'address': addresses, 'parking': parkings, 'cellar': cellars, 'contact name': contact_names, 'phone number': phone_numbers, 'date of publication': date_publications, 'additional expenses': add_expenses})  # Create a DF with the lists

    # with pd.ExcelWriter('result.xlsx') as writer:
    #     df.to_excel(writer, sheet_name='Sheet1')

def main():
    #log_in()

    for url in TARGET_URLs:
        driver.get(url)
        scrape_site(url)
        driver.quit()

if __name__ == '__main__':
    main()

