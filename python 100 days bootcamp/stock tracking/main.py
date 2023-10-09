import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "stock api key"
NEWS_API_KEY = "news api key"
TWILIO_SID = "your twilio SID"
TWILIO_KEY = "your twilio key"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY

}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_closing_price = data_list[0]["4. close"]

day_before_yesterday_closing_price = data_list[1]["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = 0
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
difference_perc = round((abs(difference) / float(yesterday_closing_price)) * 100)
if difference_perc > 0:
    news_param = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_param)
    articles = news_response.json()["articles"]
    three_articles = articles[:4]

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
formatted_article = [
    f"{STOCK_NAME}{up_down}{difference_perc}% \nheadlines:{articles['title']} \nbrief:{articles['description']}" for
    articles in three_articles]

# TODO 9. - Send each article as a separate message via Twilio.
client = Client(TWILIO_SID, TWILIO_KEY)
for article in formatted_article:
    message = client.messages.create(
        body=article,
        from_='+17698889436',
        to='+917904738428'
    )

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
