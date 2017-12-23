from twilio.rest import Client
import sys
import time
import credentials
import urllib
import requests

account_sid = credentials.account_sid
auth_token  = credentials.auth_token
client = Client(account_sid, auth_token)



# Listener function to take in messages
def Listener():
    while True:
        try:
            for message in client.messages.list():
                if (message.direction == "inbound"):
                  
                    print (message.body)
                    client.messages(message.sid).update(body="")
        except KeyboardInterrupt:
            break
            #send_sms.send_message(searchResult)
    # wait to not get too much at once
    time.sleep(10)


# wait until value is texted, true if no timeout 
def wait_until(max_time):
  print("enter something")
  timeout = time.time() + max_time
  current_time = time.time()
  while current_time < timeout:
    # get latest message
    current_message = client.messages.list()[0]
    print(current_message.body)

    # check if value was entered
    if (current_message.direction == "inbound"):
      print("value entered!!!")
      return current_message.body
    
    time.sleep(10)
    current_time = time.time()
  return "Timed Out"


