from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pprint import pprint
import requests

s=Service("C:\Development\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, service=s)

url='https://www.lollydaskal.com/leadership/100-motivational-quotes-will-inspire-succeed/'
driver.get(url)

# scrapes data from url
data = driver.find_elements(By.CSS_SELECTOR, '.textBlock p')


quotes = []
# loops thru data list
for quote_data in data:
    # text turned to list of words
    quoteWordList = quote_data.text.split()
    try:
        # turns first word/element to an int or string
        is_num = int( quoteWordList[0].strip(".") )
        # turns 2nd word to list and letters to check if quotation is present
        is_quotation_mark = list(quoteWordList[1])
        # checks if is_num is int to check if it's a quote and checks if 1st word has a quotation
        if type(is_num) == int and '“' == is_quotation_mark[0]:
            # sentence turned to list of words
            quote_as_list = quote_data.text.split()[1::]
            # quotes joined
            quote = [" ".join(quote_as_list)]

        quotes.append(quote[0])
    except:
        pass

# adds cleaned data to txt file
with open("quotes_list.txt", mode="w", encoding="utf-8") as file:
    # loops through the quotes list then individually writes sentences to a new line in txt
    for each_item in quotes:
        file.write(f"{each_item}\n")

time.sleep(1)
driver.close()