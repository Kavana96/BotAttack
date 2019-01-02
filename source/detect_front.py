import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings, time
import tweepy
import urllib3
import time
import csv
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField 

import category as category
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'randomthing'


consumer_key = '3WjVqtiVFAIvbQCvh7QhYdUpe'
consumer_secret = 'Fd45MFcAV9et2o3iEH9lGBCxX8D0H9hTdLNsWGX5KMjnaPitzr'
access_token = '772597859715780608-OD7jGeZbEymEDK9i4EXOlCZ3HbT2SDl'
access_token_secret = 'JcXxN52DE4n1QMJ7YY8Pq7RUx69yi8pe9xQCaWjy37c35'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def hello():
        form = ReusableForm(request.form)
        #name = TextField('Name:', validators=[validators.required()])
        print form.errors
        if request.method == 'POST':
            name=request.form['name']
            #print name
            if form.validate():
                # Save the comment here.
                value = get_data_from_twitter(name)
                if value > 3:
                    mycategory = category.who_am_i(name)
                    flash(name + " is a " + mycategory + " bot")
                    #flash(name + " is a bot")
                elif value == -1:
                    flash(name + " is a verified account")
                elif value == -100:
                    flash("Error: "+name + " User doesnot exist")
                elif value == -200:
                    flash("It is a private account")
                else :
                    flash(name + " is not a bot")
            else:
                flash('Error: All the form fields are required. ')
 
        return render_template('front.html', form=form)


def bot_prediction_algorithm(data):
        # creating copy of dataframe
        flag = 0
        #We created two bag of words because more bow is stringent on test data, so on all small dataset we check less
        bag_of_words_bot = ['bot','b0t','butt','fuck','XXX','sex','fake','free','virus','funky','xx','ffd','emoji','joke','troll','droop','free','marketing','money','lotto','click','buisness','profit',
                            'startup','follow','trial','mention','tweet','biz','clicks','try','sell','online','buy' 'win','with me','government',
                            'me','freedom','time','hour','minutes','generate','like','job','apply','porn','tmj',
                            'lucky','call','people','gif','email','mail']
        #print data.description
        name = data.name.lower()
        description = data.description.lower()
        screen_name = data.screen_name.lower()
        #print description
        for w in bag_of_words_bot:
            #print w
            if (name.find(w)) > -1:
                flag = flag + 4
                #print flag
            elif (description.find(w)) > -1:
                #print (description.find(w))
                flag = flag + 4
                #print flag
            elif (screen_name.find(w)) > -1:
                flag = flag + 4
                #print flag
            elif flag >= 4:
                break
        # check if the user is verified
        #print flag
        if data.verified == True:
            # print "NOT A BOT"
            # print data.verified
            return (-1)
            #exit()
        # if data.verified == False:
        #     flag = flag + 1
        #     #print flag
        
        if (((data.statuses_count < 2000) & (data.followers_count < 2000)) | ((data.statuses_count < 500) & (data.followers_count > 2000))):
            flag = flag + 1
            #print flag
        # if ((data.listed_count < 500)):
        #     flag = flag + 1
        if (((data.friends_count > 2000) & (data.statuses_count < 1000)) | ((data.friends_count < 200) & (data.statuses_count > 300))):
            flag = flag + 1
            #print flag
        if ((data.friends_count < 170) & (data.followers_count < 3000) & (data.followers_count > 1000)):
            flag = flag + 1
            #print flag
        if ((data.listed_count < 100) | (data.favourites_count < 100)):
            flag = flag + 1
        if (data.listed_count == 0):
            flag = flag + 1
        if (data.followers_count == 0):
            flag = flag + 1
        if (data.statuses_count == 0):
            flag = flag + 1
        return flag

def get_data_from_twitter(username):
        #outputFile = "userData.csv"
        errorCount = 0
        # fc = csv.writer(open(outputFile, 'w'))
        # fc.writerow(["id", "id_str", "name", "screen_name", "description", "followers_count", "friends_count", "created_at", "favourites_count", "verified", "statuses_count", "listed_count", "location","bot"])
        #user = api.get_user(username)
        try:
            user = api.get_user(username)
        except tweepy.TweepError:
            print "USER DOESNOT EXIST!!!"
            return (-100)
        try:
            print user.description
        except UnicodeEncodeError:
            return (-200)
            #print user.description
            # print user.followers_count
            # print user.statuses_count
        except tweepy.TweepError:
            print "USER DOESNOT EXIST!!!"
            return (-100)
        value = bot_prediction_algorithm(user)
        #print user.verified
        #print value
        return value


if __name__ == '__main__':
    app.run()

    
