# import package
import africastalking

# Initialize SDK
username = "YOUR_USERNAME"
# use 'sandbox' for development in the test environment
api_key = "YOUR_API_KEY"
# use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)

# Initialize a service e.g. SMS
sms = africastalking.SMS

# Use the service synchronously
response = sms.send("Hello Message!", ["+2547xxxxxx"])
print(response)


# Or use it asynchronously
def on_finish(error, response):
    if error is not None:
        raise error
    print(response)


sms.send("Hello Message!", ["+2547xxxxxx"], callback=on_finish)
