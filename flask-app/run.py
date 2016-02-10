from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from es_helper import ESHelper
from cassandra_helper import CassandraHelper
app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def hello_world():
    return render_template('index.html', words=[], subreddits=[])

@app.route('/rub')# , methods=['POST'])
def query_es():
    MAX_USERS = 10000
    MAX_WORDS = 200
    MAX_OTHER_SUBREDDITS = 200
    es_helper = ESHelper()
    topic = 'cat' #request.form['topic']
    subreddit = 'programming' #request.form['subreddit']
    year_month = '2008_06' #es_helper.convert_year_month(request.form['year_month'])
    top_users = es_helper.get_top_users(subreddit, year_month, MAX_USERS)
    top_words = es_helper.get_top_words(topic, year_month, top_users, 200)
    top_other_subreddits = es_helper.get_top_other_subreddits(topic, year_month, top_users, 200)

    return render_template('index.html', words=top_words, subreddits=top_other_subreddits)

@app.route('glean', methods=['POST'])
def quesy_cassandra():
    MAX_USERS = 10000
    MAX_COMMENTS = 100

    topic = request.form['topic']
    subreddit = request.form['subreddit']
    year_month = es_helper.convert_year_month(request.form['year_month'])
    top_users = es_helper.get_top_users(subreddit, year_month, MAX_USERS)
    top_filtered_comments =  es_helper.get_top_comments_by_score(topic, year_month, top_users, MAX_COMMENTS)
    cassandra_helper = CassandraHelper()
    cassandra_helper.get_highest_ranked_comments(top_filtered_comments, year_month,200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
