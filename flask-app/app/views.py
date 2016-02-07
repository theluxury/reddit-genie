from flask import render_template, flash, redirect
from app import app
import urllib2
from elasticsearch import Elasticsearch
import json
from wordcloud import WordCloud
import os
from .forms import LoginForm, SearchForm
from es_helper import ESHelper
import json



@app.route('/')
@app.route('/bootstrap-index')
def bootstrap():
    return render_template('bootstrap-index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        es_helper = ESHelper()
        top_users = es_helper.get_top_users(form.subreddit.data, form.year_month.data, 10000)
        top_words = es_helper.get_top_words(form.topic.data, form.year_month.data, top_users, 200)
        if not top_words:
            print "nope"
            flash("Didn't get any results.:( Are you sure you put the right things in? Remember subreddit is case sensitive.")
        else:
            return render_template('results.html', title="Reddit Genie", form=form, words=json.dumps(top_words))
    else:
        # TODO: do I want this?
        print "filler"
#       flash("You didn't fill the form right. :(")
    return render_template('search.html',
                           title='Reddit Genie',
                           form=form)
        
@app.route('/bar_results')
def bar_results():
    return render_template('bar_results.html')

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

    
