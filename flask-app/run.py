from flask import Flask, render_template, request, redirect, flash
from flask_bootstrap import Bootstrap
from es_helper import ESHelper
from cassandra_helper import CassandraHelper
import json
app = Flask(__name__)
Bootstrap(app)

def year_month_checker(year_month, latest_year, latest_month):
    earliest_year = 2007
    earliest_month  = 10
    year = int(year_month.split('_')[0])
    month = int(year_month.split('_')[1])
    if year > latest_year or (year == latest_year and month > latest_month) or year < earliest_year or (year == earliest_year and month < earliest_month):
        return False
    else:
        return True

@app.route('/')
def hello_world():
    return render_template('index.html', words=[], subreddits=[], link_url="")

@app.route('/rub' , methods=['POST'])
def query_es():
    MAX_USERS = 10000
    MAX_WORDS = 200
    MAX_OTHER_SUBREDDITS = 20
    es_helper = ESHelper()
    topic = request.form['topic']
    subreddit = request.form['subreddit']
    year_month = es_helper.convert_year_month(request.form['year_month'])
    if not year_month_checker(year_month, 2015, 6):
       flash("Ooops, you picked a wrong date range. Please select a month from October 2007 to June 2015", '\
error')
       return render_template('index.html', words=[], subreddits=[])
    top_users = es_helper.get_top_users(subreddit, year_month, MAX_USERS)
    current_try = 0
    total_tries = 4
    while current_try < total_tries:
        current_try += 1
        try:
            top_words = es_helper.get_top_words(topic, year_month, top_users, MAX_WORDS)
            current_try = total_tries
        except:
            if current_try == total_tries:
                flash("Read timed out. Don't worry! Try the same search again and it should work this time.", 'error')
                return redirect('/')
    top_other_subreddits = es_helper.get_top_other_subreddits(topic, year_month, top_users, MAX_OTHER_SUBREDDITS)
    if not top_words:
        flash('Did not get any results for subreddit {0} users for topic {1} during {2}. Are you sure you spelled everything right? Remember that the subreddit entry is case sensitive'.format(subreddit, topic, year_month) ,'error')
    return render_template('index.html', words=top_words, subreddits=top_other_subreddits, topic=topic, link_url="glean/{0}/{1}/{2}".format(topic, subreddit, year_month), show_comments=year_month_checker(year_month, 2014, 5))

@app.route('/glean/<topic>/<subreddit>/<year_month>')
def query_cassandra(topic, subreddit, year_month):
    if not year_month_checker(year_month, 2014,5):
        flash("Ooops, you tried to get comments from an invalid month. Please try something before June 2014.", 'error')
        return redirect('/')
    MAX_USERS = 10000
    MAX_COMMENTS = 20
    es_helper = ESHelper()
    top_users = es_helper.get_top_users(subreddit, year_month, MAX_USERS)
    top_filtered_comments =  es_helper.get_top_comments_by_score(topic, year_month, top_users, MAX_COMMENTS)
    cassandra_helper = CassandraHelper()
    return json.dumps(cassandra_helper.get_highest_ranked_comments(top_filtered_comments, year_month))

if __name__ == '__main__':
    app.secret_key = 'SECRET_KEY'
    app.run(host='0.0.0.0', debug=True)
