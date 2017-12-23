from twilio.rest import Client
import credentials
import send_sms
import time

account_sid = credentials.account_sid
auth_token  = credentials.auth_token
client = Client(account_sid, auth_token)


for old_message in client.messages.list():
	client.messages(old_message.sid).update(body="")
# keep running
while True:
  for message in client.messages.list():
  	# print message when sent in
  	if len(message.body) > 0:
  		print(message.body)
  		# delete message body
    	client.messages(message.sid).update(body="")

    #send_sms.send_message(message)


  time.sleep(10)