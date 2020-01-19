from bs4 import BeautifulSoup
import urllib.error
import requests
import sys
import csv
from datetime import datetime
import re
from collections import OrderedDict

Max_items = 0

def main():

    global itemCount
    itemCount = 0
    global fileName
    path = "../../data/external/"
    fileName = path + "tripadvisor_" + datetime.now().strftime('%Y%m%d_%H%M') + ".csv"
    global titleList
    titleList = []
    global writer
    fw = open(fileName, 'w', newline='')
    writer = csv.writer(fw, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['number', 'link', 'date', 'name', 'first_review', 'second_review', 'rating', 'n_reviews', 'type', 'price_range', 'price', 'review_pro'])

    print("The output csv file is: %s " %(fileName))
    print("-----------------------------------------")

    # Start scraping on a first listing page. the function does its work and it also returns the url
    # of a 'volgende' index page OR it returns None to indicate that there are no further index pages

    nextLink = "https://www.tripadvisor.com/Restaurants-g60713-San_Francisco_California.html"
    endLink = "https://www.tripadvisor.com/Restaurants-g60713-oa4770-San_Francisco_California.html#EATERY_LIST_CONTENTS"

    while nextLink != None and nextLink != endLink:
        nextLink = analyze_index_page(nextLink)
    
    # Done doing the scrapping
    print("Process completed with %d restaurants" % (itemCount))



def analyze_index_page(url):
    """
    """

    global itemCount
    global Max_items

    print("Analyze index page %s" %(url))

    #host = urllib.parse.urlparse(url).netloc
    #host = requests.compat.urlparse(url).hostname
    host = "www.tripadvisor.com"
    r = requests.get(url)
    print("Status code of the page: ", r.status_code)
    soup = BeautifulSoup(r.text, features="html.parser")

    divs = soup.findAll("div", class_="restaurants-list-ListCell__infoWrapper--3agHz")
    for div in divs:
        try:
            itemCount += 1

            # Extract name of the restaurant
            #name_ = div.find("div", class_="restaurants-list-ListCell__restaurantName--2aSdo").get_text(" ", strip=True)
            name_ = div.find("div", class_="restaurants-list-ListCell__nameBlock--1hL7F").get_text(" ", strip=True)
            
            # Extract rating
            try:
                if div.find("span", class_="ui_bubble_rating bubble_5"):
                    rating_ = 5
                elif div.find("span", class_="ui_bubble_rating bubble_10"):
                    rating_ = 10
                elif div.find("span", class_="ui_bubble_rating bubble_15"):
                    rating_ = 15
                elif div.find("span", class_="ui_bubble_rating bubble_20"):
                    rating_ = 20
                elif div.find("span", class_="ui_bubble_rating bubble_25"):
                    rating_ = 25
                elif div.find("span", class_="ui_bubble_rating bubble_30"):
                    rating_ = 30
                elif div.find("span", class_="ui_bubble_rating bubble_35"):
                    rating_ = 35
                elif div.find("span", class_="ui_bubble_rating bubble_40"):
                    rating_ = 40
                elif div.find("span", class_="ui_bubble_rating bubble_45"):
                    rating_ = 45
                elif div.find("span", class_="ui_bubble_rating bubble_50"):
                    rating_ = 50
                else:
                    rating_ = 0
            except:
                print("No rating")
                rating_ = 0
            
            # Extract number of ratings
            try:
                text_ratings_ = div.find("span", class_="restaurants-list-ListCell__userReviewCount--2a61M").get_text(" ", strip=True)
                text_ratings_ = text_ratings_.replace(',', '')
                n_ratings_ = int(text_ratings_[:text_ratings_.rfind(' ')])
            except:
                n_ratings_ = 0

            # Extract reviews
            try:
                first_review_ = div.find("span", class_="restaurants-list-components-ReviewSnippets__snippetText--22Umt").get_text(" ", strip=True)
            except:
                first_review_= ""
            try:
                second_review_ = div.find("span", class_="restaurants-list-components-ReviewSnippets__snippetText--22Umt").get_text(" ", strip=True)
            except:
                second_review_ = ""

            # date
            date_ = datetime.now().strftime('%Y%m%d_%H%M')


            # Type and price
            try:
                type_price_div = div.find("div", class_="restaurants-list-ListCell__infoRow--31xBt restaurants-list-ListCell__hideLeftDivider--3vXbe restaurants-list-ListCell__cuisinePriceMenu--r4-Re")
                type_price_text = type_price_div.get_text(" ", strip=True)

                # type of restaurant
                type_ = type_price_text[:type_price_text.find('$')-1]

                # price of the restaurant
                price_range = type_price_text[type_price_text.find('$'):type_price_text.rfind('$')+1]
                n_dollar = price_range.count('$')
                if n_dollar == 1:
                    price_ = "cheap_eats"
                elif n_dollar == 5:
                    price_ = "mid_range"
                elif n_dollar == 4:
                    price_ = "fine_dining"
            except:
                type_ = ""
                price_ = ""
            
            # Review from professionals
            try:
                review_pro_ = div.find("div", class_="restaurants-list-components-ListCellMentions__mentionsWrapper--1bbiT").get_text(" ", strip=True)
            except:
                review_pro_ = ""


            writer.writerow( (itemCount, url, date_, name_, first_review_, second_review_, rating_, n_ratings_, type_, price_range, price_, review_pro_) )
            # if (Max_items > 0)  and (itemCount > Max_items):
            #     print("Stopped scrapping after %d restaurants \n" %(Max_items))
            #     sys.exit
        except urllib.error.HTTPError as e:
            # Exception handling. Be verbose on HTTP errors such as 404 (not found).
            sys.stdout.write("    HTTPError: {0}\n".format(e))
        except:
            print("Overall problem")

    nextAnchor = soup.find("a", class_="nav next rndBtn ui_button primary taLnk")
    if nextAnchor:
        nextLink = nextAnchor.get('href')
        if (nextLink):
            #nextLink = requests.compat.urljoin("https:", host, nextLink)
            #nextLink_ = requests.compat.urljoin("https://", host)
            #nextLink = requests.compat.urljoin(nextLink_, nextLink)
            nextLink = "https://" + host + nextLink
            return nextLink
    return None
        


if __name__ == '__main__':
    main()#!/usr/bin/env python