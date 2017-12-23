import requests
import urllib
from bs4 import BeautifulSoup

home_link = 'https://hdh.ucsd.edu/DiningMenus/'
home_url = requests.get('https://hdh.ucsd.edu/DiningMenus/')
meal_time = ["Breakfast", "Lunch", "Dinner"]

#get link depending on which dining hall
def get_hall(dining_hall):
    soup = BeautifulSoup(home_url.content, 'html.parser')
    links = soup.find("div",{"class" : "navigation"})
    halls = {}
    for div in links.find_all('a'):
        name = div.text
        link = div.get('href')
        halls[name] = link
    return halls[dining_hall]

def get_menus(dining_hall_link):
    hall_link =  home_link + dining_hall_link
    hall_url = requests.get(hall_link )
    soup = BeautifulSoup(hall_url.content, 'html.parser')
    foods = soup.find_all("td", {"class" : "menuList"},'a')
    menu = {}

    #for div in foods.find_all('a'):
    #    name = div.text
    #    link = div.get('href')
    #    menu[name] = link


    counter = 0
    for div in foods:
        meal = {}
        for food in div.find_all('a'):
            name = food.text
            link = food.get('href')
            meal[name] = [link]
        menu[meal_time[counter % 3]] = meal
        counter += 1
    #for div in foods:
    #    name = div.text
    #    link = div.get('href')
    #    print(link)
    #    menu[name] = link

    return menu

########################################################
def get_nutrition(menu, meal_time, food):

    try: 
        food_link =  home_link + str(menu[meal_time][food])
        food_link = food_link.replace("['", "")
        food_link = food_link.replace("']", "")
        food_url = requests.get(food_link )
        soup = BeautifulSoup(food_url.content, 'html.parser')
        info = soup.find_all("td")
        #print(soup.findChildren('tblNutritionDetails'))
        #table = soup.find("table", id = 'tblNutritionDetails')

        nutrition = ''
        counter = 0;
        for row in info:
            if (counter > 1 and counter < 8):
                row_text = str(row.text).replace("\xa0", "")

                nutrition = nutrition + row_text.replace("\n\n", "\n") + "\n"

            counter += 1
    except KeyError as e:
        return "error"
        
    return nutrition

########################################################
def get_food_str(menu, meal_time, food_str):
        for food in menu[meal_time]:
            if (food_str.lower() in str(food).lower()):
                return str(food)



