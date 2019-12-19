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
    writer.writerow(['number', 'link', 'date', 'name', 'text', 'rating', 'number_reviews'])

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

            # Extract name
            name_ = div.find("div", class_="restaurants-list-ListCell__restaurantName--2aSdo").get_text(" ", strip=True)