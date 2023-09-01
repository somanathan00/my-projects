# Import Required Modules
from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px

import snscrape.modules.twitter as sntwitter
import pandas as pd

from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request

tokenizer = None
model = None

# Create Home Page Route
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("landingPage.html")


@app.route('/analyse', methods=['GET', 'POST'])
def bar_with_plotly():
    hash1 = request.form.get("hash1")
    hash2 = request.form.get("hash2")

    year1 = request.form.get("year1")
    year2 = request.form.get("year2")
    year3 = request.form.get("year3")
    year4 = request.form.get("year4")
    month1 = request.form.get("month1")
    month2 = request.form.get("month2")
    month3 = request.form.get("month3")
    month4 = request.form.get("month4")
    date1 = request.form.get("date1")
    date2 = request.form.get("date2")
    date3 = request.form.get("date3")
    date4 = request.form.get("date4")

    tweets_list1 = []
    search_query = "hashtags:#" + hash1 + " lang:en since:" + int(year1) + "-" + int(month1) + "-" + int(
        date1) + " until:" + int(year2) + "-" + int(month2) + "-" + int(date2)

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
        tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

    tweets_list2 = []
    search_query = "hashtags:#" + hash2 + " lang:en since:" + int(year3) + "-" + int(month3) + "-" + int(
        date3) + " until:" + int(year4) + "-" + int(month4) + "-" + int(date4)

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
        tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

    for i in range(len(tweets_list1)):
        # Removing hashtags and mentions
        tweets_list1[i] = re.sub("@[A-Za-z0-9_]+", "", tweets_list1[i])
        tweets_list1[i] = re.sub("#[A-Za-z0-9_]+", "", tweets_list1[i])
        # tweets_list1 Removing links  
        tweets_list1[i] = re.sub(r"http\S+", "", tweets_list1[i])
        tweets_list1[i] = re.sub(r"www.\S+", "", tweets_list1[i])
        # tweets_list1 Removing punctuations
        tweets_list1[i] = re.sub('[()!?]', ' ', tweets_list1[i])
        tweets_list1[i] = re.sub('\[.*?\]', ' ', tweets_list1[i])
        # tweets_list1 Filtering non-alphanumeric characters
        tweets_list1[i] = re.sub("[^a-z0-9]", " ", tweets_list1[i])
        # tweets_list1 removing whitespaces
        tweets_list1[i] = tweets_list1[i].strip()
        # print(i," ",sentiment_pipeline(i))

    for i in range(len(tweets_list2)):
        # Removing hashtags and mentions
        tweets_list2[i] = re.sub("@[A-Za-z0-9_]+", "", tweets_list2[i])
        tweets_list2[i] = re.sub("#[A-Za-z0-9_]+", "", tweets_list2[i])
        # tweets_list1 Removing links  
        tweets_list2[i] = re.sub(r"http\S+", "", tweets_list2[i])
        tweets_list2[i] = re.sub(r"www.\S+", "", tweets_list2[i])
        # tweets_list1 Removing punctuations
        tweets_list2[i] = re.sub('[()!?]', ' ', tweets_list2[i])
        tweets_list2[i] = re.sub('\[.*?\]', ' ', tweets_list2[i])
        # tweets_list1 Filtering non-alphanumeric characters
        tweets_list2[i] = re.sub("[^a-z0-9]", " ", tweets_list2[i])
        # tweets_list1 removing whitespaces
        tweets_list2[i] = tweets_list2[i].strip()
        # print(i," ",sentiment_pipeline(i))

    ANSWER_ARRAY = ["NEGATIVE", "NEUTRAL", "POSITIVE"]

    tweet1_postive = 0
    tweet1_neutral = 0
    tweet1_negative = 0

    tweet2_postive = 0
    tweet2_neutral = 0
    tweet2_negative = 0

    for i in tweets_list1:
        if len(i.strip()) == 0:
            continue
        # print(i," ",sentiment_pipeline(i)[0]['label'])
        encoded_input = tokenizer(i, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        # print("input sentence is: \n",i)
        # for ind in range(3):
        #   print(ANSWER_ARRAY[ind]," - ",scores[ind])

        if np.argmax(scores) == 0:
            tweet1_negative += 1
        elif np.argmax(scores) == 1:
            tweet1_neutral += 1
        elif np.argmax(scores) == 2:
            tweet1_positive += 1

        # print("sentiment value of  ",i," is - ",ANSWER_ARRAY[np.argmax(scores)]) 
        # print("---------------------------")    

    for i in tweets_list2:
        if len(i.strip()) == 0:
            continue
        # print(i," ",sentiment_pipeline(i)[0]['label'])
        encoded_input = tokenizer(i, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        # print("input sentence is: \n",i)
        # for ind in range(3):
        #   print(ANSWER_ARRAY[ind]," - ",scores[ind])

        if np.argmax(scores) == 0:
            tweet2_negative += 1
        elif np.argmax(scores) == 1:
            tweet2_neutral += 1
        elif np.argmax(scores) == 2:
            tweet2_positive += 1

        # print("sentiment value of  ",i," is - ",ANSWER_ARRAY[np.argmax(scores)]) 
        # print("---------------------------")    

    # Students data available in a list of list
    results = [[hash1, tweet1_postive, ANSWER_ARRAY[2]],
               [hash1, tweet1_neutral, ANSWER_ARRAY[1]],
               [hash1, tweet1_negative, ANSWER_ARRAY[0]],
               [hash2, tweet2_postive, ANSWER_ARRAY[2]],
               [hash2, tweet2_neutral, ANSWER_ARRAY[1]],
               [hash2, tweet2_negative, ANSWER_ARRAY[0]]]

    # Convert list to dataframe and assign column values
    df = pd.DataFrame(results,
                      columns=['hashtags', 'count', 'sentiment'],
                      index=['a', 'b', 'c', 'd', 'e', 'f'])

    # Create Bar chart
    fig = px.bar(df, x='hashtags', y='count', color='count', barmode='group')

    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Use render_template to pass graphJSON to html
    return render_template('result.html', graphJSON=graphJSON)


if __name__ == '__main__':
    tokenizer = AutoTokenizer.from_pretrained("saved_tokenizer")
    model = AutoModelForSequenceClassification.from_pretrained("saved_model")
    app.run(debug=True)
