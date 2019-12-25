from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import requests
import sys
import csv
from datetime import datetime
import re
from collections import OrderedDict

Max_items = 2

def main():

    global itemCount
    itemCount = 0
    global fileName
    fileName = "tripadvisor_" + datetime.now().strftime('%Y%m%d_%H%M') + ".csv"
    global titleList
    titleList = []
    global writer
    fw = open(fileName, 'w', newline='')
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

    global itemCount

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
            
            # Extract review
            if div.find("span", class_="ui_bubble_rating bubble_5"):
                review_ = 5
            elif div.find("span", class_="ui_bubble_rating bubble_10"):
                review_ = 10
            elif div.find("span", class_="ui_bubble_rating bubble_15"):
                review_ = 15
            elif div.find("span", class_="ui_bubble_rating bubble_20"):
                review_ = 20
            elif div.find("span", class_="ui_bubble_rating bubble_25"):
                review_ = 25
            elif div.find("span", class_="ui_bubble_rating bubble_30"):
                review_ = 30
            elif div.find("span", class_="ui_bubble_rating bubble_35"):
                review_ = 35
            elif div.find("span", class_="ui_bubble_rating bubble_40"):
                review_ = 40
            elif div.find("span", class_="ui_bubble_rating bubble_45"):
                review_ = 45
            elif div.find("span", class_="ui_bubble_rating bubble_50"):
                review_ = 50
            else:
                review_ = 0
            
            # Extract number of reviews
            text_reviews_ = div.find("span", class_="restaurants-list-ListCell__userReviewCount--2a61M").get_text(" ", strip=True)
            text_reviews_ = text_reviews_.replace(',', '')
            print(text_reviews_)
            print(int(text_reviews_[:text_reviews_.rfind(' ')]))
            n_reviews_ = int(text_reviews_[:text_reviews_.rfind(' ')])

            # Extract first review
            text_ = div.find("span", class_="restaurants-list-components-ReviewSnippets__snippetText--22Umt").get_text(" ", strip=True)

            # date
            date_ = datetime.now().strftime('%Y%m%d_%H%M')

            writer.writerow( (itemCount, url, date_, name_, text_, review_, n_reviews_) )
        except:
            print("problem")

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
        r = requests.get(url)
        print("Status code of the page in try: ", r.status_code)
        soup = BeautifulSoup(r.text)
        #soup = BeautifulSoup(urllib.request.urlopen(url))
        #divs = soup.findAll("div", class_="restaurants-list-ListCell__cellContainer--2mpJS")
        divs = soup.findAll("div", class_="restaurants-list-ListCell__infoWrapper--3agHz")
        for div in divs:
            itemCount += 1

            # Extract name of the restaurant
            name_ = div.find("div", class_="restaurants-list-ListCell__restaurantName--2aSdo").get_text(" ", strip=True)
            
            # Extract review
            if div.find("span", class_="ui_bubble_rating bubble_5"):
                review_ = 5
            elif div.find("span", class_="ui_bubble_rating bubble_10"):
                review_ = 10
            elif div.find("span", class_="ui_bubble_rating bubble_15"):
                review_ = 15
            elif div.find("span", class_="ui_bubble_rating bubble_20"):
                review_ = 20
            elif div.find("span", class_="ui_bubble_rating bubble_25"):
                review_ = 25
            elif div.find("span", class_="ui_bubble_rating bubble_30"):
                review_ = 30
            elif div.find("span", class_="ui_bubble_rating bubble_35"):
                review_ = 35
            elif div.find("span", class_="ui_bubble_rating bubble_40"):
                review_ = 40
            elif div.find("span", class_="ui_bubble_rating bubble_45"):
                review_ = 45
            elif div.find("span", class_="ui_bubble_rating bubble_50"):
                review_ = 50
            else:
                review_ = 0
            
            # Extract number of reviews
            n_reviews_ = div.find("span", class_="restaurants-list-ListCell__userReviewCount--2a61M").get_text(" ", strip=True)

            # Extract first review
            text_ = div.find("span", class_="restaurants-list-components-ReviewSnippets__snippetText--22Umt").get_text(" ", strip=True)

        # Find next page
        nextAnchor = soup.find("a", class_="")
        if nextAnchor:
            nextLink = nextAnchor.get('href')
            if nextLink:
                nextLink = "https://www.tripadvisor.com/" + nextLink
                analyze_story_page(nextLink)
        return None
        
    except urllib.error.HTTPError as e:
        # Exception handling. Be verbose on HTTP errors such as 404 (not found).
        sys.stdout.write("    HTTPError: {0}\n".format(e))
        return
    except:
        # Exceptions thrown by operations on non-existing structures
        sys.stdout.write("    Structure exception: {0}\n".format(sys.exc_info()[0]))
        return


if __name__ == '__main__':
    main()#!/usr/bin/env python