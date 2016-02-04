from flask import render_template, flash, redirect
from app import app
import urllib2
from elasticsearch import Elasticsearch
import json
from wordcloud import WordCloud
import os
from .forms import LoginForm, SearchForm
from es_helper import ESHelper

@app.route('/')
@app.route('/bootstrap-index')
def bootstrap():
    return render_template('bootstrap-index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        flash('Search requested for subreddit: {0} and topic: {1} for year_month: {2}'.format(form.subreddit.data, form.topic.data, form.year_month.data))
        es_helper = ESHelper()
        print es_helper.search(form.subreddit.data, form.topic.data, form.year_month.data)
    return render_template('search.html',
                           title='Reddit Genie',
                           form=form)
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        
    return render_template('login.html', 
                           title='Sign In',
                           form=form)


@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/query/<searchWord>/<subreddit>/<year_month>')
def query(searchWord, subreddit, year_month):
    os.system("pwd")
    os.system("python quicky.py {0} {1} {2} > meh.txt".format(searchWord, subreddit, year_month))
    os.system("python another-quicky.py")
    return 'plz work'
    
