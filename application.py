from tkinter import *
from flask import Flask
import pandas as pd
import pickle
import tweepy
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import json
import re
import nltk
import numpy as np
from nltk.corpus import stopwords
import nltk
import string
from nltk.stem.porter import PorterStemmer
import csv
from tkinter import messagebox

application = Flask(__name__)

consumer_key = 'dN83WDtuVeO17TakgbcZRklVB'
consumer_secret = 'CuWNXarGfxn7vQhDLjSPUOxPeAs7t0djLmAvT4pjQge9qzMZb6'
access_token = '1067272446053634048-w2xNV8zZ7rw6NohEK7esJMgNVHUZpt'
access_secret = 'KY588azcqgLUM3qCdSgtDY3I6zXHCBT28z1fk6QONqJ82'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

account_list = ['RoodramP']
api = tweepy.API(auth, wait_on_rate_limit=True)

stop_words = set(stopwords.words('english'))
t = str.maketrans('', '', string.punctuation)
porter = PorterStemmer()

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F" 
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
                           "]+", flags=re.UNICODE)
    s = emoji_pattern.sub(r'', s)
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return " ".join(tokens)
 


def fn(e,e1,e2):
	process(e)
	predict()
	loadNeed(e1)
	loadAvail(e2)

def loadNeed(e1):
    e1.delete('1.0',END)
    fn = pd.read_csv('need.csv')
    for line in fn['Tweets']:
        e1.insert(END, line)
        e1.insert(END, "\n")
    
    

def loadAvail(e2):
    e2.delete('1.0',END)
    fa = pd.read_csv('avail.csv')
    for line in fa['Tweets']:
        e2.insert(END, line)
        e2.insert(END, "\n\n")
      

def process(target):
    tweets = ['Tweets']
    target = target.get()
    print(target)
#    messagebox.showinfo("User", target)
    friend_list = [target]
    item = api.get_user(target)
    for friend in item.friends():
        friend_list.append(friend.screen_name)

    f = csv.writer(open('predict.csv','w'))
    for target in friend_list:
        for status in Cursor(api.user_timeline, id=target).items(10):
            if hasattr(status, "text"):
                tweet = status.text
                tweet = preprocess(tweet)
                tweets.append(tweet)

        for item in tweets:
            f.writerow([item])

def predict():
    openFile = 'LogisticRegressionModel'
    saveVectorizer = 'vectorizer'

    predictor = pickle.load(open(openFile, 'rb'))
    vect = pickle.load(open(saveVectorizer, 'rb'))

    readFile = pd.read_csv('predict.csv')
    f1 = csv.writer(open('need.csv','w'))
    f2 = csv.writer(open('avail.csv','w'))
    f1.writerow(["Tweets"])
    f2.writerow(["Tweets"])
    pred = vect.transform(readFile['Tweets']).toarray()
    result = predictor.predict(pred)

    i=0
    for res in result:
    	if(res==1):
    		f2.writerow([readFile['Tweets'][i]])
    	elif(res==2):
    		f1.writerow([readFile['Tweets'][i]])
    	i+=1

@application.route("/")
def main():
    root = Tk()
    root.title("Tweetifire")
    root.geometry('1000x1000')
    c = Canvas(root,width=1000)
    c.pack(side = 'left',expand=1,fill=BOTH)

    c2 = Canvas(c)
    c2.pack(side = 'left',expand=1,fill=BOTH)
    c3 = Canvas(c)
    c3.pack(side = 'left',expand=1,fill=BOTH)

    w1 = Label(c2, text=" UserName ")
    w1.pack()
    e = Entry(c2,width=200)
    e.pack()
    toolbar = Frame(c2)
    toolbar.pack(side=TOP, fill=X)

    l = Label(c2, text=' Need ')
    l.pack()
    l1 = Text(c2, height=15)
    l1.pack()
    l2 = Label(c2, text=' Available ')
    l2.pack()
    l3 = Text(c2, height=15)
    l3.pack()

    b = Button(toolbar, text="Classify", width=9, command=lambda:fn(e,l1,l3))
    b.pack(side=LEFT, padx=2, pady=2)
    root.mainloop()

if __name__ == '__main__':
    main()
