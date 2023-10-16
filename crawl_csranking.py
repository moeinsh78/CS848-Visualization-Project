# Import libraries and modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from selenium import webdriver


def extract_row_data(row, field, time):
    row_data = [field, time]
    splitted_row = row.split("  ")
    # Extracting Ranking
    rank = int(splitted_row[0])
    row_data.append(rank)
    
    # Extracting University Name
    if splitted_row[1] == "":
        splitted_row.pop(1)
    
    university_name = splitted_row[1]
    reached_alpha = False
    while not reached_alpha:
        if university_name[0].isalpha():
            reached_alpha = True
        else: 
            university_name = university_name[1:]

    row_data.append(university_name)

    # Extracting Count and Faculty
    numbers = splitted_row[2].split()
    count = float(numbers[0])
    faculty = int(numbers[1])
    
    row_data.append(count)
    row_data.append(faculty)

    return row_data

search_criterion = [
    {"id": "1", "url": "https://csrankings.org/#/fromyear/1995/toyear/2005/index?ai&vision&mlmining&nlp&inforet&chi&ca", "field": "all", "time": "2000"},
    {"id": "2", "url": "https://csrankings.org/#/fromyear/1995/toyear/2005/index?ai&ca", "field": "ai", "time": "2000"},
    {"id": "3", "url": "https://csrankings.org/#/fromyear/1995/toyear/2005/index?vision&ca", "field": "cv", "time": "2000"},
    {"id": "4", "url": "https://csrankings.org/#/fromyear/1995/toyear/2005/index?mlmining&ca", "field": "ml", "time": "2000"},
    {"id": "5", "url": "https://csrankings.org/#/fromyear/1995/toyear/2005/index?nlp&inforet&ca", "field": "irnlp", "time": "2000"},
    {"id": "6", "url": "https://csrankings.org/#/fromyear/1995/toyear/2005/index?chi&ca", "field": "hci", "time": "2000"},
    {"id": "7", "url": "https://csrankings.org/#/fromyear/2005/toyear/2014/index?ai&vision&mlmining&nlp&inforet&chi&ca", "field": "all", "time": "2010"},
    {"id": "8", "url": "https://csrankings.org/#/fromyear/2005/toyear/2014/index?ai&ca", "field": "ai", "time": "2010"},
    {"id": "9", "url": "https://csrankings.org/#/fromyear/2005/toyear/2014/index?vision&ca", "field": "cv", "time": "2010"},
    {"id": "10", "url": "https://csrankings.org/#/fromyear/2005/toyear/2014/index?mlmining&ca", "field": "ml", "time": "2010"},
    {"id": "11", "url": "https://csrankings.org/#/fromyear/2005/toyear/2014/index?nlp&inforet&ca", "field": "irnlp", "time": "2010"},
    {"id": "12", "url": "https://csrankings.org/#/fromyear/2005/toyear/2014/index?chi&ca", "field": "hci", "time": "2010"},
    {"id": "13", "url": "https://csrankings.org/#/fromyear/2014/toyear/2023/index?ai&vision&mlmining&nlp&inforet&chi&ca", "field": "all", "time": "2020"},
    {"id": "14", "url": "https://csrankings.org/#/fromyear/2014/toyear/2023/index?ai&ca", "field": "ai", "time": "2020"},
    {"id": "15", "url": "https://csrankings.org/#/fromyear/2014/toyear/2023/index?vision&ca", "field": "cv", "time": "2020"},
    {"id": "16", "url": "https://csrankings.org/#/fromyear/2014/toyear/2023/index?mlmining&ca", "field": "ml", "time": "2020"},
    {"id": "17", "url": "https://csrankings.org/#/fromyear/2014/toyear/2023/index?nlp&inforet&ca", "field": "irnlp", "time": "2020"},
    {"id": "18", "url": "https://csrankings.org/#/fromyear/2014/toyear/2023/index?chi&ca", "field": "hci", "time": "2020"},
]

university_img_url = {
    "University of Alberta": "/assets/alberta.jpeg",
    "Carleton University": "/assets/carleton.jpeg",
    "Concordia University": "/assets/concordia.jpeg",
    "Dalhousie University": "/assets/dalhousie.jpeg",
    "ETS Montreal": "/assets/etsmontreal.avif",
    "University of Guelph": "/assets/guelph.jpeg",
    "McGill University": "/assets/mcgill.webp",
    "Queen’s University": "/assets/queens.jpeg",
    "Simon Fraser University": "/assets/sfu.jpeg",
    "University of British Columbia": "/assets/ubc.jpeg",
    "University of Calgary": "/assets/ucalgary.jpeg",
    "Université Laval": "/assets/ulaval.jpeg",
    "University of Manitoba": "/assets/umanitoba.jpeg",
    "University of Montreal": "/assets/umontreal.jpeg",
    "University of Toronto": "/assets/uoft.jpeg",
    "University of Ottawa": "/assets/uottawa.jpeg",
    "University of Saskatchewan": "/assets/usask.jpeg",
    "University of Victoria": "/assets/uvic.jpeg",
    "University of Waterloo": "/assets/waterloo.jpeg",
    "Western University": "/assets/western.jpeg",
    "York University": "/assets/york.jpeg",
}

table_data = []
for criteria in search_criterion:
    print(criteria["id"])
    # Create a driver object
    driver = webdriver.Chrome()
    driver.get(criteria["url"])

    # Wait for the page to load completely
    driver.implicitly_wait(10)

    # Find the table element by its id
    table = driver.find_element("id", "ranking")
    table_text = table.text

    # Find all the rows in the table
    rows = table.find_elements("xpath", "//tr")
    found_universities = False

    # Loop through each row
    for row in rows:
        # Find all the cells in the row
        if row.text == "":
            continue
        if not found_universities:
            if row.text.startswith("# Institution"):
                found_universities = True
            continue

        row_data_array = extract_row_data(row.text, criteria["field"], criteria["time"])
        table_data.append(row_data_array)

    # Close the driver
    driver.close()


table_df = pd.DataFrame(table_data, columns=["field", "time_period", 'ranking', 'university_name', "score", "faculty"])
table_df["image_url"] = table_df["university_name"].map(university_img_url)
table_df.to_csv("../Project/csranking_data.csv", index=True)