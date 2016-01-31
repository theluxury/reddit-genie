from app import app
import urllib2
from elasticsearch import Elasticsearch
import json
from wordcloud import WordCloud
import os

@app.route('/')
@app.route('/query/<searchWord>/<subreddit>/<year_month>')

def query(searchWord, subreddit, year_month):
    os.system("pwd")
    os.system("python quicky.py {0} {1} {2} > meh.txt".format(searchWord, subreddit, year_month))
    os.system("python another-quicky.py")
    return 'plz work'
    
