from twilio.rest import Client
import time
import credentials
import send_sms
import search
import re
import scraper
import datetime

dt = datetime.datetime.now()
account_sid = credentials.account_sid
auth_token  = credentials.auth_token
client = Client(account_sid, auth_token)

user = ''

###########################################################################

def get_restaurant(restaurantStr):
  restaurant = {
    "64": "64 Degrees (Revelle College)",
    "64degrees": "64 Degrees (Revelle College)",
    "canyonvista": "Canyon Vista (Warren College)",
    "cv": "Canyon Vista (Warren College)",
    "cafeventanas": "Cafe Ventanas (Roosevelt College)",
    "cafev": "Cafe Ventanas (Roosevelt College)",
    "foodworx": "Foodworx (Sixth College)",
    "garbage": "Foodworx (Sixth College)",
    "oceanview": "OceanView (Marshall College)",
    "ovt": "OceanView (Marshall College)",
    "64north": "Sixty-Four North (Revelle College)",
    "pines": "Pines (Muir College)",
    "goodys": "Goody&#39;s (Marshall College)",
    "clubmed": "Club Med (School of Medicine)",
    "roots": "Roots (Muir College)",
    "thebistro": "The Bistro (The Village East)",
  }

  return restaurant.get(restaurantStr, "error")

###########################################################################

def is_restaurant(restaurantStr):
  return get_restaurant(restaurantStr) != "error"

###############################################################################
def help():
  return "The possible dining options are: 64 Degrees, Canyon Vista, \
  Cafe Ventanas, Foodworx, OceanView, 64 North, Pines, Goody's, Roots, \
  Roots, Bistro, Club Med."

###########################################################################

def get_menu(restaurantStr, meal_time):
  menu = scraper.get_menus(scraper.get_hall(restaurantStr))

  menu_str = "\n\n" + restaurantStr + "\n" +"[ " + meal_time + "] " + "\n" 

  for food in menu[meal_time]:
    menu_str = menu_str + str(food)+ "\n"

  return menu_str

###########################################################################

def get_meal_time():
  if dt.hour >= 0 and dt.hour <= 11:
    return "Breakfast"
  if dt.hour > 11 and dt.hour <= 4:
    return "Lunch"
  if dt.hour > 4 and dt.hour < 24:
    return "Dinner"

###########################################################################

while True:
  message = client.messages.list()[0]
  if (message.direction == 'inbound' and message.body != ''):
    messageStr = message.body.lower()
    messageStr = re.sub('[^A-Za-z0-9]+', "", messageStr)
    user = client.messages.list()[0].from_,
    print(message.body)

    #Check if its a valid restaurant
    if not is_restaurant(messageStr):
      client.messages(message.sid).update(body="")
      send_sms.send_message(help(), user)
    else:
      meal_time = get_meal_time()
      menu = get_menu(get_restaurant(messageStr), meal_time)

      send_sms.send_message(menu, user)
      send_sms.send_message("Enter the menu item for nutrition fact, or type NO to exit", user)
      
      response = search.wait_until(120).lower()
      if (response == "no" or response == "n"):
        continue
      else:
        menuDict = scraper.get_menus(scraper.get_hall(get_restaurant(messageStr)))
        food_str = scraper.get_food_str(menuDict, meal_time, response)

        nutrition = scraper.get_nutrition(menuDict, meal_time, food_str)
        if (nutrition == "error"):
          send_sms.send_message("The food item you entered was not found", user)
        else:
          send_sms.send_message(nutrition, user)

     