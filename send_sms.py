from twilio.rest import Client
import credentials
import search

# Your Account SID from twilio.com/console
account_sid = credentials.account_sid
# Your Auth Token from twilio.com/console
auth_token  = credentials.auth_token

client = Client(account_sid, auth_token)

def send_message(messageStr, user):

	message = client.messages.create(
   		to =user,
    	from_=credentials.my_twilio,
    	body = messageStr)
