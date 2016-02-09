from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from es_helper import ESHelper
app = Flask(__name__)
words = []
subreddits = []
Bootstrap(app)

@app.route('/')
def hello_world():
    print words
    return render_template('index.html', words=words, subreddits=subreddits)

@app.route('/rub', methods=['POST'])
def query_es():
    es_helper = ESHelper()
    topic = request.form['topic']
    subreddit = request.form['subreddit']
    year_month = es_helper.convert_year_month(request.form['year_month'])
    top_users = es_helper.get_top_users(subreddit, year_month, 10000)
    top_words = es_helper.get_top_words(topic, year_month, top_users, 200)
    top_other_subreddits = es_helper.get_top_other_subreddits(topic, year_month, top_users, 200)

    del words[:]
    for word in top_words:
        words.append(word)

    del subreddits[:]
    for subreddit in top_other_subreddits:
        subreddits.append(subreddit)

    return redirect('/')

@app.route('/test')
def show_test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)
