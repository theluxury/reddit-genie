# reddit genie
Getting lots of cool reddit insights because that's how I roll dawg.

#1: Introduction
reddit genie is designed to tell you what subreddits think about things. Beyond just naively searhching in that subreddit, reddie genie actually gets the users of that subreddit, then finds all their posts in all subreddits. This is because if you want the opinion of the science subreddit on say, Bernie Sanders, it's helpful to get all their posts, since they may not talk about Bernie Sanders in that subreddit.

#2: Getting started
First thing's first
    
    pip install requirements.txt

Then
    
    python util/nltk-downloader.py
and download stopwords and punkt. Now you're ready to run my code!

#3: What does it actually <i>do?</i>
<h3>Supported Queries</h3>
Word cloud, membership, filter by time, etc.

<h3>Data Source</h3>
~900GB of reddit data https://bigquery.cloud.google.com/dataset/fh-bigquery:reddit_comments from Obtobe,r 2007 until June, 2015 though since I ran out of HD space. 

#4: AWS Cluster Structure



