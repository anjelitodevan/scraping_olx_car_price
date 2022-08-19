import csv
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
import time

# use edge
options= EdgeOptions()
options.use_chromium= True
driver= Edge(options= options, executable_path= "C:\Additional Packages\edgedriver_win64\msedgedriver.exe")

# create url builder function
def get_url(search_term):
    """Generate URL from search term"""
    template= "https://www.olx.co.id/mobil-bekas_c198/q-{}"
    search_term= search_term.replace(" ", "-")
    return template.format(search_term)

# create record extractor
def extract_record(item):
    """Extract and return data from a single record"""
    
    try:
        product= item.find("div", {"class": "_4aNdc"}).text
        price= item.find("span", {"data-aut-id": "itemPrice"}).text
        year_and_km= item.find("div", {"data-aut-id": "itemSubTitle"}).text
    except AttributeError:
        pass
    
    try:
        loc_time= item.find("div", {"data-aut-id": "itemDetails"}).text
        time= item.find("div", {"data-aut-id": "itemDetails"}).span.text
        loc= loc_time.replace(time, "")
    except AttributeError:
        loc_time= ""
        time= ""
        loc= ""
    
    result= (product, price, year_and_km, loc)
    return(result)

# create function to click next page
def click_next_page(n):
    """Click next page n number of times"""
    list= range(n)
    for i in list:
        try:
            next_button = driver.find_element(By.CLASS_NAME, "JbJAl")
            next_button.click()
            time.sleep(10)
        except:
            pass


list_car_to_crawl= [
    "toyota avanza",
    "mitsubishi expander",
    "toyota rush", 
    "toyota innova",
    "honda brio",
    "daihatsu sigra",
    "toyota calya",
    "toyota fortuner",
    "toyota raize",
    "daihatsu alya"
]

for car in list_car_to_crawl:
    
    # open url in browser and grab
    url= get_url(car)
    driver.get(url)

    # load next page
    click_next_page(100)

    soup= BeautifulSoup(driver.page_source, "html.parser")

    records= []
    results= soup.find_all("div", {"class": "_3ZUR4"})

    for item in results:
        record= extract_record(item)
        if record:  
            records.append(extract_record(item))

    # append result to csv
    with open("result.csv", "a", newline= "", encoding= "utf-8") as f:
        writer= csv.writer(f)
        writer.writerows(records)

driver.close()

print("Task finished.")