from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
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
    fileName = "tripadvisor_" + datetime.now().strftime('%Y%m%d_%H%M') + ".csv"
    global titleList
    titleList = []
    global writer
    fw = open(fileName, 'w', newline=',')
    writer = csv.writer(fw, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['number', 'link', 'date', 'name', 'text', 'rating', 'n_reviews'])

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

    print("Analyze index page %s" %(url))

    host = urllib.parse.urlparse(url).netloc
    soup = BeautifulSoup(urllib.request.urlopen(url))
    listLinks = []

    for link in soup.findAll(href=re.compile("Show"))


def analyze_story_page(url):
    """
    """

    global itemCount, Max_items, fileName

    if (Max_items > 0)  and (item_Count > Max_items):
        print("Stopped scrapping after %d restaurants \n" %(Max_items))
        sys.exit
    
    # Show what page we are looking at
    print("   %s - analyzeStoryPage %s" % (str(itemCount).zfill(5), url))
    try :
        soup = BeautifulSoup(urllib.request.urlopen(url))
        #divs = soup.findAll("div", class_="restaurants-list-ListCell__cellContainer--2mpJS")
        divs = soup.findAll("div", class_="restaurants-list-ListCell__infoWrapper--3agHz")
        for div in divs:
            itemCount += 1

            # Extract name of the restaurant
            name_ = div.find("div", class_="restaurants-list-ListCell__restaurantName--2aSdo").get_text(" ", strip=True)
            
            # Extract review
            if div.find("span", class_="ui_bubble_rating bubble_5") is not None:
                review_ = 5
            elif div.find("span", class_="ui_bubble_rating bubble_10") is not None:
                review_ = 10
            elif div.find("span", class_="ui_bubble_rating bubble_15") is not None:
                review_ = 15
            elif div.find("span", class_="ui_bubble_rating bubble_20") is not None:
                review_ = 20
            elif div.find("span", class_="ui_bubble_rating bubble_25") is not None:
                review_ = 25
            elif div.find("span", class_="ui_bubble_rating bubble_30") is not None:
                review_ = 30
            elif div.find("span", class_="ui_bubble_rating bubble_35") is not None:
                review_ = 35
            elif div.find("span", class_="ui_bubble_rating bubble_40") is not None:
                review_ = 40
            elif div.find("span", class_="ui_bubble_rating bubble_45") is not None:
                review_ = 45
            elif div.find("span", class_="ui_bubble_rating bubble_50") is not None:
                review_ = 50
            
            # Extract number of reviews
            n_reviews_ = div.find("span", class_="restaurants-list-ListCell__userReviewCount--2a61M").get_text(" ", strip=True)

            # Extract first review
            text_ = div.find("span", class="restaurants-list-components-ReviewSnippets__snippetText--22Umt").get_text(" ", strip=True)