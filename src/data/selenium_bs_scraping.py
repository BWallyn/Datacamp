from bs4 import BeautifulSoup
import urllib.error
import requests
import sys
import csv
from datetime import datetime
import re
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd


def main():

    path = "../../data/external/"
    fileName = path + "tripadvisor_" + datetime.now().strftime('%Y%m%d_%H%M') + ".csv"

    global writer
    fw = open(fileName, 'w', newline='')
    writer = csv.writer(fw, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['link', 'name', 'rating', 'n_reviews', 'price_type', 'location', 'borough',
                     'price_range', 'cuisines', 'special_diets', 'meals', 'features',
                     'n_review_excellent', 'n_review_verygood', 'n_review_average', 'n_review_poor', 'n_review_terrible',
                     'list_reviews'])

    print("The output csv file is: %s " % (fileName))
    print("-----------------------------------------")

    dataset = pd.read_csv('../../data/interim/enhanced_restaurant_scores.csv')
    restaurants_name = dataset['business_name'].unique()
    nb_restaurants = len(restaurants_name)
    for index, name in enumerate(restaurants_name):
        print("Searching '{}' on TripAdvisor ({}/{})".format(name,
                                                             index+1, nb_restaurants))
        get_link_restaurant(name)
    # Done doing the scrapping
    print("Process completed")


def get_link_restaurant(name):

    host = "https://www.tripadvisor.com/Restaurants-g60713-San_Francisco_California.html"

    # Create a headless chrome diver
    chrome_option = Options()
    chrome_option.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_option)
    driver.get(host)

    # Find the seach input. There are two versions of Tripadvisor seach bar, hence we manage both of them
    # with the version_1 boolean
    version_1 = True
    search_input = driver.find_elements_by_xpath("//div[@title='Search']")
    if(not search_input):
        version_1 = not version_1
        search_input = driver.find_elements_by_xpath("//input[@type='search']")
        if(not search_input):
            print('Problem with TripAdvisor search bar!')
            driver.close()
            return None
    search_input[0].click()
    if(version_1):
        try:
            text_area = WebDriverWait(driver, 2).until(
                expected_conditions.visibility_of_element_located((By.ID, "mainSearch")))
        except:
            print('No result found !')
            driver.close()
            return None
    else:
        text_area = search_input[0]

    # Write the restaurant name in the search bar
    text_area.send_keys(name)
    text_area.send_keys(Keys.RETURN)

    # Get the URL of the top matching restaurant
    try:
        top_matching_div = WebDriverWait(driver, 1).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "result-title")))
        print('Restaurant found !')
        url = 'https://www.tripadvisor.com' + \
            top_matching_div.get_attribute('onclick').split(',')[
                3].split("'")[1]
        driver.close()
        # Analyze the restaurant page
        analyze_restaurant_page(url, n_max_reviews=5)
    except:
        print('Restaurant not found :(')
        driver.close()


def analyze_restaurant_page(url, n_max_reviews=5):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")

    # Name
    try:
        name = soup.find("h1", class_="ui_header h1").get_text(" ", strip=True)
    except:
        return None

    # Extract rating
    try:
        rating_str = soup.find(
            "span", class_="restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl").get_text(" ", strip=True)
        rating = float(rating_str)
    except:
        rating = 0.

    # Number of reviews
    try:
        reviews = soup.find(
            'a', class_="restaurants-detail-overview-cards-RatingsOverviewCard__ratingCount--DFxkG").get_text(" ", strip=True)
        reviews = reviews.replace(',', '')
        n_reviews = int(reviews[:reviews.rfind(' ')])
    except:
        n_reviews = 0

    # Price
    try:
        detail_tags = soup.find(
            'div', class_="prw_rup prw_restaurants_restaurant_detail_tags tagsContainer").get_text(" ", strip=True)
        n_dollar = detail_tags.count('$')
        if n_dollar == 1:
            price = "cheap_eats"
        elif n_dollar == 5:
            price = "mid_range"
        elif n_dollar == 4:
            price = "fine_dining"
        else:
            price = "Other_category"
    except:
        price = ""

    # Location
    try:
        div = soup.find(
            "div", class_="restaurants-detail-overview-cards-LocationOverviewCard__cardColumn--2ALwF")
        div = div.find("div", class_="restaurants-detail-overview-cards-LocationOverviewCard__addressLink--1pLK4 restaurants-detail-overview-cards-LocationOverviewCard__detailLink--iyzJI")
        print("url_loc: ", div.find("a").get('href'))
        url_loc = string(span_loc.find("a").get('href'))
        location = url_loc[url_loc.find('@'):]
    except:
        location = ""

    # Borough
    try:
        div = soup.find(
            "div", class_="restaurants-detail-overview-cards-LocationOverviewCard__cardColumn--2ALwF")
        nearby_text = div.find(
            "span", class_="restaurants-detail-overview-cards-LocationOverviewCard__detailLinkText--co3ei restaurants-detail-overview-cards-LocationOverviewCard__nearbyText--6M5-L")
        borough = nearby_text.find("div").get_text(" ", strip=True)
    except:
        borough = ""

    ####
    # Details
    price_range = ""
    cuisines = ""
    special_diets = ""
    meals = ""
    features = ""

    div_det_sec = soup.find(
        "div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__detailCard--WpImp")
    div_details = soup.find(
        "div", class_="restaurants-details-card-DetailsCard__innerDiv--1Imq5")

    # More detailed card
    if div_details:
        divs = div_details.find_all("div")
        for div_el in divs:
            div_head = div_el.find(
                "div", class_="restaurants-details-card-TagCategories__categoryTitle--28rB6")
            if div_head:
                header = div_head.get_text(" ", strip=True)
                if header == "CUISINES":
                    try:
                        cuisines = div_el.find(
                            "div", class_="restaurants-details-card-TagCategories__tagText--Yt3iG").get_text(" ", strip=True)
                    except:
                        cuisines = ""
                elif header == "Special Diets":
                    try:
                        special_diets = div_el.find(
                            "div", class_="restaurants-details-card-TagCategories__tagText--Yt3iG").get_text(" ", strip=True)
                    except:
                        special_diets = ""
                elif header == "PRICE RANGE":
                    try:
                        price_range = div_el.find(
                            "div", class_="restaurants-details-card-TagCategories__tagText--Yt3iG").get_text(" ", strip=True)
                    except:
                        price_range = ""
                elif header == "Meals":
                    try:
                        meals = div_el.find(
                            "div", class_="restaurants-details-card-TagCategories__tagText--Yt3iG").get_text(" ", strip=True)
                    except:
                        meals = ""
                elif header == "FEATURES":
                    try:
                        features = div_el.find(
                            "div", class_="restaurants-details-card-TagCategories__tagText--Yt3iG").get_text(" ", strip=True)
                    except:
                        features = ""

    # Small detailed card
    elif div_det_sec:
        div = div_det_sec.find(
            "div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__detailsSummary--evhlS")
        divs = div.find_all("div")
        for div_el in divs:
            div_det = div_el.find(
                "div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__categoryTitle--2RJP_")
            if div_det:
                header = div_det.get_text(" ", strip=True)
                if header == "CUISINES":
                    cuisines = div_el.find(
                        "div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h").get_text(" ", strip=True)
                elif header == "PRICE RANGE":
                    price_range = div_el.find(
                        "div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h").get_text(" ", strip=True)
                elif header == "Special Diets":
                    special_diets = div_el.find(
                        "div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h").get_text(" ", strip=True)
                elif header == "Meals":
                    meals = div_el.find(
                        "div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h").get_text(" ", strip=True)

    ####
    # Reviews

    # Distribution rating
    n_reviews = [0]*5
    div_rev = soup.find(
        "div", class_="ratings_and_types block_wrap ui_section")
    if div_rev:
        div_filt = div_rev.find(
            "div", class_="collapsibleContent ppr_rup ppr_priv_detail_filters")
    else:
        div_filt = None

    if div_filt:
        div_choice = div_filt.find("div", class_="choices")
        divs = div_choice.find_all("div", class_="ui_checkbox item")

        for i in range(len(divs)):
            try:
                n_reviews_text = divs[i].find(
                    "span", class_="row_num is-shown-at-tablet").get_text(" ", strip=True).replace(",", "")
                n_reviews[i] = int(n_reviews_text)
            except:
                n_reviews[i] = 0

    # Reviews
    list_reviews = [""]*n_max_reviews
    if div_rev:
        div_list_rev = div_rev.find(
            "div", class_="ppr_rup ppr_priv_location_reviews_list_resp")

        try:
            divs = div_list_rev.find_all("div", class_="ui_column is-9")
            max_rev = min(len(divs), n_max_reviews)
            for i in range(max_rev):
                list_reviews[i] = re.sub('[^a-zA-Z.\d\s]', '', divs[i].find(
                    "div", class_="prw_rup prw_reviews_text_summary_hsx").get_text(" ", strip=True))

        except:
            list_reviews = [""]*n_max_reviews

    writer.writerow((url, name, rating, n_reviews, price, location, borough,
                     price_range, cuisines, special_diets, meals, features,
                     n_reviews[0], n_reviews[1], n_reviews[2], n_reviews[3], n_reviews[4],
                     str(list_reviews)))


if __name__ == '__main__':
    main()  # !/usr/bin/env python
