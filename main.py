import requests
import json
import time
from datetime import datetime
import pytz
from twilio.rest import Client



companyShares = {
    "GOOGL": 0,
    "AAPL": 0,
    "MSFT": 0,
    "AMZN": 0,
    "META": 0,
    "TSLA": 0,
    "NFLX": 0,
    "IBM": 0,
    "INTC": 0,
    "ADBE": 0
}

balance = float(input("Enter your starting wealth: "))
isHolding = str(input("Are you holding any shares currently? (y/n): "))
if(isHolding == 'y'):
    isDone = False
    while(isDone != True):
        name = str(input("Enter the NASDAQ Symbol of the company"))
        if(name in companyShares):
            amount = int(input("Enter the amount of shares you got: "))
            companyShares[name] = amount
        
        else:
            name = str(input("Invalid. press X to continue or enter a company name to continue"))
        
        name = input("Do you have any more shares in other companies? (y/n)")
        if(name == "n"):
            isDone == True
        else:
            continue


invest = input("In which company would you like to invest? (NASDAQ Symbol)?: ")

apiKey = "5Y3W8EABQIMY2SFY"

# with open("data.json", "w") as jsonFile:
#     json.dump(data, jsonFile, indent=4)

rawData = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={invest}&apikey={apiKey}")
rawData.raise_for_status()
data = rawData.json()

def buyShares(price):
    quantity = int(input("How much? "))
    if(balance >= quantity * price):
        companyShares[invest] += quantity
        price -= quantity * price
    else:
        print("Not enough money")
    
def sellShares(price):
    quantity = int(input("How much? "))
    if(companyShares[invest] >= quantity):
        companyShares[invest] -= quantity
        price += quantity * price
    else:
        print("Not enough shares")


while(True):
    current_unix_time = int(time.time())
    current_datetime = datetime.utcfromtimestamp(current_unix_time)
    source_timezone = pytz.utc
    target_timezone = pytz.timezone('America/New_York')
    adjusted_datetime = current_datetime.replace(tzinfo=source_timezone).astimezone(target_timezone)
    theTime = adjusted_datetime.strftime('%Y-%m-%d') 

    highest = float(data["Time Series (Daily)"][theTime]["2. high"])
    lowest = float(data["Time Series (Daily)"][theTime]["3. low"])

    bodyMsg = f"The {invest} Share peaked today with the price of: {highest} and was in it's lowesest value with the price of: {lowest} - To take actions about the shares you got in the company, please connect to the app"

    account_sid = "YOUR SID HERE :)"
    auth_token = "YOUR AUTH HERE :)"
    client = Client(account_sid, auth_token)
    from_number = "+17069206277"
    to_number = "YOUR NUMBER HERE :)"

    message = client.messages.create(
        body=bodyMsg,
        from_=from_number,
        to=to_number
    )

    choice = input("What would you like to do? \n B - Buy shares, S - Sell shares, C - Continue")
    if(choice == "B"):
        buyShares(float(data["Time Series (Daily)"][theTime]["4. close"]))
    elif(choice == "S"):
        sellShares(float(data["Time Series (Daily)"][theTime]["4. close"]))

    time.sleep(86400)

    

         

