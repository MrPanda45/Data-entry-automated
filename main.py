from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import requests

chrome_driver_path = "C:\Development\chromedriver.exe"
FORMS_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdRpr0sb1fvvSM04qeLuNCbnb8TvSumYskix8tjBsav5DbQ3Q/viewform?usp=sf_link"
ZILLOW_URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B"pagination"%3A%7B%7D%2C"mapBounds"%3A%7B"west"%3A-122.86385573339844%2C"east"%3A-122.00280226660156%2C"south"%3A37.484901876961864%2C"north"%3A38.06454489093633%7D%2C"isMapVisible"%3Afalse%2C"filterState"%3A%7B"price"%3A%7B"max"%3A872627%7D%2C"beds"%3A%7B"min"%3A1%7D%2C"fore"%3A%7B"value"%3Afalse%7D%2C"mp"%3A%7B"max"%3A3000%7D%2C"auc"%3A%7B"value"%3Afalse%7D%2C"nc"%3A%7B"value"%3Afalse%7D%2C"fr"%3A%7B"value"%3Atrue%7D%2C"fsbo"%3A%7B"value"%3Afalse%7D%2C"cmsn"%3A%7B"value"%3Afalse%7D%2C"fsba"%3A%7B"value"%3Afalse%7D%7D%2C"isListVisible"%3Atrue%7D'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.52",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(ZILLOW_URL, headers=headers)
response.raise_for_status()
contents = response.text

soup = BeautifulSoup(contents, "html.parser")

######################## GETTING THE LINKS ########################

links = soup.select(".list-card-top a")
links_list = []
for link in links:
    true_link = link["href"]
    if "https://www.zillow.com" not in true_link:
        link_complete = f"https://www.zillow.com{true_link}"
        links_list.append(link_complete)
    else:
        links_list.append(true_link)

######################## GETTING THE PRICES OF THE LINKS ########################

prices = soup.select(".list-card-price")
prices_list = [price.text.strip()[0:6] for price in prices]
# for price in prices:
#     text = price.text
#     stripped_text = text.strip()
#     prices_list.append(stripped_text[0:6])

######################## GETTING THE ADDRESSES OF THE LINKS ########################

addresses = soup.select(".list-card-addr")
addresses_list = [address.text for address in addresses]

######################## FILLING THE FORMS ########################

driver = webdriver.Chrome(chrome_driver_path)
driver.get(FORMS_URL)
sleep(2)
i = 0

for n in range(len(links_list) - 1):
    address_write = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_write.send_keys(addresses_list[n])
    sleep(0.5)
    prices_write = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prices_write.send_keys(prices_list[n])
    sleep(0.5)
    links_write = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    links_write.send_keys(links_list[n])
    sleep(0.5)
    submit_button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    submit_button.click()
    sleep(1)
    submit_another_answer = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another_answer.click()
    sleep(2)
    i += 1

print(f"The total amount of answers was: {i}")

