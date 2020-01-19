from bs4 import BeautifulSoup
import urllib.error
import requests
import sys
import csv
from datetime import datetime
import re
from collections import OrderedDict

def main():

    itemCount = 0
    path = "../../data/external/"
    fileName = path + "tripadvisor_" + datetime.now().strftime('%Y%m%d_%H%M') + ".csv"

    titleList = []

    global writer
    fw = open(fileName, 'w', newline='')
    writer = csv.writer(fw, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['number', 'link', 'date', 'name', 'rating', 'n_reviews', 'price_type', 'location', 'borough',
                    'price_range', 'cuisines', 'special_diets', 'meals', 'features',
                    'n_review_excellent', 'n_review_verygood', 'n_review_average', 'n_review_poor', 'n_review_terrible',
                    'list_reviews'])

    print("The output csv file is: %s " %(fileName))
    print("-----------------------------------------")

    nextLink = "https://www.tripadvisor.com/Restaurants-g60713-San_Francisco_California.html"
    endLink = "https://www.tripadvisor.com/Restaurants-g60713-oa4770-San_Francisco_California.html#EATERY_LIST_CONTENTS"

    while nextLink != None and nextLink != endLink:
        nextLink, itemCount = get_link_restaurant(nextLink, itemCount)
    

    # Done doing the scrapping
    print("Process completed with %d restaurants" % (itemCount))



def get_link_restaurant(url, itemCount):

    print("Analyze index page %s" %(url))

    host = "www.tripadvisor.com"
    r = requests.get(url)
    print("Status code of the page: ", r.status_code)
    soup = BeautifulSoup(r.text, features="html.parser")

    divs = soup.findAll("div", class_="restaurants-list-ListCell__infoWrapper--3agHz")
    for div in divs:
        restaurantAnchor = div.find("a", class_="restaurants-list-ListCell__restaurantName--2aSdo")
    
        if restaurantAnchor:
            restaurantLink = restaurantAnchor.get('href')
            restaurantLink = "https://" + host + restaurantLink
            analyze_restaurant_page(restaurantLink, itemCount)
            itemCount += 1

        else:
            name_ = div.find("div", class_="restaurants-list-ListCell__nameBlock--1hL7F").get_text(" ", strip=True)
            print("No link for the restaurant: ", name_)
    
    nextAnchor = soup.find("a", class_="nav next rndBtn ui_button primary taLnk")
    if nextAnchor:
        nextLink = nextAnchor.get('href')
        if (nextLink):
            nextLink = "https://" + host + nextLink
            return nextLink, itemCount
    return None, itemCount



def analyze_restaurant_page(url, itemCount, n_max_reviews=5):

    host = "www.tripadvisor.com"
    r = requests.get(url)
    print("Status code of the page: ", r.status_code)
    soup = BeautifulSoup(r.text, features="html.parser")

    # date
    date = datetime.now().strftime('%Y%m%d_%H%M')

    # Name
    try:
        name = soup.find("h1", class_="ui_header h1").get_text(" ", strip=True)
        print("name: ", name)
    except:
        return None

    # Extract rating
    try:
        rating_str = soup.find("span", class_="restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl").get_text(" ", strip=True)
        rating = float(rating_str)
    except:
        rating = 0.

    # Number of reviews
    try:
        reviews = soup.find('a', class_="restaurants-detail-overview-cards-RatingsOverviewCard__ratingCount--DFxkG").get_text(" ", strip=True)
        reviews = reviews.replace(',', '')
        n_reviews = int(reviews[:reviews.rfind(' ')])
    except:
        n_reviews = 0
    
    # Price
    try:
        detail_tags = soup.find('div', class_="prw_rup prw_restaurants_restaurant_detail_tags tagsContainer").get_text(" ", strip=True)
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
        div = soup.find("div", class_="restaurants-detail-overview-cards-LocationOverviewCard__cardColumn--2ALwF")
        div = div.find("div", class_="restaurants-detail-overview-cards-LocationOverviewCard__addressLink--1pLK4 restaurants-detail-overview-cards-LocationOverviewCard__detailLink--iyzJI")
        print("url_loc: ", div.find("a").get('href'))
        url_loc = string(span_loc.find("a").get('href'))
        location = url_loc[url_loc.find('@'):]
    except:
        location = ""

    # Borough
    try:
        div = soup.find("div", class_="restaurants-detail-overview-cards-LocationOverviewCard__cardColumn--2ALwF")
        nearby_text = div.find("span", class_="restaurants-detail-overview-cards-LocationOverviewCard__detailLinkText--co3ei restaurants-detail-overview-cards-LocationOverviewCard__nearbyText--6M5-L")
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

    div_det_sec = soup.find("div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__detailCard--WpImp")
    div_details = soup.find("div", class_="restaurants-details-card-DetailsCard__innerDiv--1Imq5")
    
    # More detailed card
    if div_details:
        divs = div_details.find_all("div")
        for div_el in divs:
            div_head = div_el.find("div", class_="restaurants-details-card-TagCategories__categoryTitle--28rB6")
            if div_head:
                header = div_head.get_text(" ", strip=True)
                if header == "CUISINES":
                    try:
                        cuisines = div_el.find("div", class_="restaurants-details-card-TagCategories__tagText--Yt3iG").get_text(" ", strip=True)
                    except:
                        cuisines = ""
                elif header == "Special Diets":
                    try:
                        special_diets = div_el.find("div", class_="restaurants-details-card-TagCategories__tagText--Yt3iG").get_text(" ", strip=True)
                    except:
                        special_diets = ""
                elif header == "PRICE RANGE":
                    try:
                        price_range = div_el.find("div", class_="restaurants-details-card-TagCategories__tagText--Yt3iG").get_text(" ", strip=True)
                    except:
                        price_range = ""
                elif header == "Meals":
                    try:
                        meals = div_el.find("div", class_="restaurants-details-card-TagCategories__tagText--Yt3iG").get_text(" ", strip=True)
                    except:
                        meals = ""
                elif header == "FEATURES":
                    try:
                        features = div_el.find("div", class_="restaurants-details-card-TagCategories__tagText--Yt3iG").get_text(" ", strip=True)
                    except:
                        features = ""

    # Small detailed card
    elif div_det_sec:
        div = div_det_sec.find("div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__detailsSummary--evhlS")
        divs = div.find_all("div")
        for div_el in divs:
            div_det = div_el.find("div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__categoryTitle--2RJP_")
            if div_det:
                header = div_det.get_text(" ", strip=True)
                if  header == "CUISINES":
                    cuisines = div_el.find("div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h").get_text(" ", strip=True)
                elif header == "PRICE RANGE":
                    price_range = div_el.find("div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h").get_text(" ", strip=True)
                elif header == "Special Diets":
                    special_diets = div_el.find("div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h").get_text(" ", strip=True)
                elif header == "Meals":
                    meals = div_el.find("div", class_="restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h").get_text(" ", strip=True)
        
    ####
    # Reviews

    # Distribution rating
    div_rev = soup.find("div", class_="ratings_and_types block_wrap ui_section")
    div_filt = div_rev.find("div", class_="collapsibleContent ppr_rup ppr_priv_detail_filters")
    div_choice = div_filt.find("div", class_="choices")
    divs = div_choice.find_all("div", class_="ui_checkbox item")

    n_reviews = [0]*5
    for i in range(len(divs)):
        try:
            n_reviews_text = divs[i].find("span", class_="row_num is-shown-at-tablet").get_text(" ", strip=True).replace(",", "")
            n_reviews[i] = int(n_reviews_text)
        except:
            n_reviews[i] = 0
    
    # Reviews
    list_reviews = [""]*n_max_reviews
    div_list_rev = div_rev.find("div", class_="ppr_rup ppr_priv_location_reviews_list_resp")

    try:
        divs = div_list_rev.find_all("div", class_="ui_column is-9")
        max_rev = min(len(divs), n_max_reviews)
        for i in range(max_rev):
            list_reviews[i] = divs[i].find("div", class_="prw_rup prw_reviews_text_summary_hsx").get_text(" ", strip=True)
    except:
        list_reviews = [""]*n_max_reviews


    writer.writerow( (itemCount, url, date, name, rating, n_reviews, price, location, borough,
                    price_range, cuisines, special_diets, meals, features,
                    n_reviews[0], n_reviews[1], n_reviews[2], n_reviews[3], n_reviews[4],
                    list_reviews) )

if __name__ == '__main__':
    main()#!/usr/bin/env python