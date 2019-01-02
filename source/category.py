from tweepy import OAuthHandler
from tweepy import API
import re
from political import *
from process_tweet_object import *
import tweepy
import spacy, nltk
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def is_political_bot(user):
    found = False
    in_progress = str(outtweets)
    #cleantweets = (emoji_pattern.sub(r'',  in_progress))
    predict = preprocess(in_progress)
    result = list(set(predict) & set(train))
    if len(result)>10:
        found = True
    return found
    
def Find(string):
    # findall() has been used 
    # with valid conditions for urls in string
    ret=False
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    if url is not None:
        ret=True
    return ret
    
def get_urls(status):
    ret = False
    if "entities" in status:
        entities = status["entities"]
        if "urls" in entities:
            for item in entities["urls"]:
                if item is not None:
                    if "expanded_url" in item:
                        url = item['expanded_url']
                        if url is not None:
                                ret = True
    return ret
    
def is_spam_bot(user):
    url_ct  =0
    found = False
    ret = False
    for each in outtweets:
        status = str(each)
        if Find(status) == True:
            url_ct +=1
    desc_matches = ["Check this", "How do you like my site", "How do you like me", "You love it harshly", "Do you like fast", "Do you like it gently", "Come to my site", "Come in", "Come on", "Come to me", "I want you", "You want me", "Your favorite", "Waiting you", "Waiting you at", "me2url.info", "url4.pro", "click2go.info", "move2.pro", "zen5go.pro", "go9to.pro"]
    if "description" in user:
        for d in desc_matches:
            if d in user["description"]:
                found = True
    if found == True or url_ct >= 10:
        ret = True
    return ret

def who_am_i(user):
    global outtweets, entities
    auth = OAuthHandler('36GL7WleHactwqkvq3bJ8xbRF', 'e7meWvB1sZpSxiH8aagE3F9TnG23BJT7v5xW4QdaoX35kLj9ZL')
    auth.set_access_token('2299716708-VD2EFUDYgUv6iy7v9wmV8ZydAybOrqBAW5ehRvI', 'uBlV0qRirQPLbZo8sX7lULB3EKLSKsSxO0SzsbnOfobtZ')
    api = tweepy.API(auth)
    
    alltweets = []
    new_tweets = api.user_timeline(screen_name = user,count=50)
    alltweets.extend(new_tweets)
    
    outtweets = [tweet.text.encode("utf-8") for tweet in alltweets]

    if is_spam_bot(user):
        return "spam"
    elif is_political_bot(user):
        return "political"
    else:
        return "social"

    
if __name__ == '__main__':
    who_am_i(user)
