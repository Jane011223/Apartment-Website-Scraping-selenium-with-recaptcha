from selenium import webdriver
from twocaptcha import TwoCaptcha
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse, parse_qs
#from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
#import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

TARGET_URLs = ["https://www.portalinmobiliario.com/arriendo/departamento/particular/las-condes-metropolitana", "https://www.portalinmobiliario.com/arriendo/departamento/particular/nunoa-metropolitana", "https://www.portalinmobiliario.com/arriendo/departamento/particular/providencia-metropolitana"]
LOGIN_URL = "https://www.mercadolibre.com/jms/mlc/lgz/msl/login/H4sIAAAAAAAEAzWOQQ7CMBAD_-JzBPcc-Ui0tE4bkZJqsyWgqn9HKeJo2R57Ry5Tegb7rITHyChbNjisWSwWXUIa4bFkONRk_MuhR0RloVEr_N45E8cbY9FOMt0IB9lsDjGXBv9bgkOqgW-jPiWHxvsrsbtRcu2NqcBjNlurv15ba5eFOshYcrorL0M_opxSNSr7tXPocIhSLZjK8IA_WccXNRkjxNwAAAA/user"

api_key = 'd34b6cea5d999aea03766d376434a179'
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
phone_btn_path = '//*[@id="grouped_main_actions"]/div/form/div/button'
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

def solve_captcha():
    #set up the 2captcha solver
    solver = TwoCaptcha(api_key)

    url = driver.find_element(By.XPATH, '//*[@id="g-recaptcha"]/div/div/iframe').get_attribute('src')
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    site_key =query_params["k"][0]
    
    # Solve the reCAPTCHA challenge using 2captcha
    result = solver.recaptcha(site_key, driver.current_url)
    print(result)
        
    # Inject the solution into the page and submit the form
    driver.execute_script('document.getElementById("g-recaptcha-response").style.display = "block"')
    driver.execute_script('document.getElementById("g-recaptcha-response").value = "{}";'.format(result['code']))
    
    time.sleep(30)

    submit_btn = driver.find_element(By.XPATH, '//*[@id="login_user_form"]/div[2]/button')
    submit_btn.click()
    print("submit_btn")

    time.sleep(30)

    # Wait for the reCAPTCHA iframe to load
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="g-recaptcha"]/div/div/iframe')))

    check_btn = driver.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]')
    check_btn.click()
    print("check_btn")

    # Switch back to the default content
    driver.switch_to.default_content()
    
    # try:
    #     result = solver.recaptcha(site_key, driver.current_url)
    #     print(result)
        
    #     # Inject the solution into the page and submit the form
    #     driver.execute_script('document.getElementById("g-recaptcha-response").style.display = "block"')
    #     driver.execute_script('document.getElementById("g-recaptcha-response").value = "{}";'.format(result['code']))
    #     time.sleep(10)
    #     print("recaptcha")

    #     submit_btn = driver.find_element(By.XPATH, '//*[@id="login_user_form"]/div[2]/button')
    #     submit_btn.click()
    #     print("submit_btn")

    #     check_btn = driver.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]')
    #     check_btn.click()
    #     print("check_btn")
    # except:
    #     print("Recaptcha Error")

    submit_btn = driver.find_element(By.XPATH, '//*[@id="login_user_form"]/div[2]/button')
    submit_btn.click()

def log_in():
    driver.get(LOGIN_URL)
    time.sleep(10)

    email = "bastian@pluscapitalcl.com"
    password = "2023contodo"

    id_field = driver.find_element(By.ID, 'user_id')
    id_field.send_keys(email)

    submit_btn = driver.find_element(By.XPATH, '//*[@id="login_user_form"]/div[2]/button')
    submit_btn.click()

    time.sleep(50)
    solve_captcha()
    time.sleep(20)

    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(password)
    
    login_btn = driver.find_element(By.XPATH, '//*[@id="action-complete"]')
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
    # df = pd.DataFrame({'Name publication': name_publications, 'prices': prices, 'sqr meters': sqr_meters, 'number of bedrooms': number_bedrooms, 'number of bathrooms': number_bathrooms, 'address': addresses, 'parking': parkings, 'cellar': cellars, 'contact name': contact_names, 'phone number': phone_numbers, 'date of publication': date_publications})  # Create a DF with the lists

    # with pd.ExcelWriter('result.xlsx') as writer:
    #     df.to_excel(writer, sheet_name='Sheet1')

def main():
    log_in()

    for url in TARGET_URLs:
        driver.get(url)
        scrape_site(url)
        driver.quit()

if __name__ == '__main__':
    main()

