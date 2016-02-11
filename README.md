# reddit genie
Your reddit insights are my command....

#1: Introduction
reddit genie is a tool designed you give users insight about subreddit communities by showing what words members of a subreddits use with a given topic. Beyond just naively searhching in that subreddit, reddie genie actually gets the users of that subreddit, then finds all their comments made in all subreddits. This is because if you want the opinion of the science subreddit on, say, Bernie Sanders, it's helpful to get all their comments everywhere, since they may not talk about Bernie Sanders in science.

#2: Getting started
First thing's first
    
    pip install requirements.txt

Then
    
    python util/nltk-downloader.py
and download stopwords and punkt. Now you're ready to run my code!

#3: What does it actually <i>do?</i>
<h3>Supported Queries</h3>
Can query related words (words used in the same comment) for any word for any users of a subreddit made across all of reddit. This main query can be filtered (by score of comment, date, author) or further analyzed by showing the breakdown of the subreddits where these comments were made. In addition, if the full text for the comments are desired, the full original text can be further queries via cassandra. 

<h3>Data Source</h3>
~900GB of reddit data https://bigquery.cloud.google.com/dataset/fh-bigquery:reddit_comments from Obtober 2007 until June 2015. 

#4: Pipeline and AWS Cluster Breakdown

![alt tag](http://i.imgur.com/WUeI6O6.jpg)

reddit data is read from S3 and preprocessed by a 6 spark node cluster. This cluster then writes to an elasticsearch instance which shares the same cluster and to a cassandra database stored on a seperate 4 node cluster. Finally, the front end is served with a flask app which interacts with the cassandra and elasticsearch clusters. 

#5: Database Design

<h3>Why two databases?</h3>

elasticsearch offer very powerful search capability at the expense of being incredibly ram intensive. This makes it an ideal solution for storing metadata while a cassandra database acts as a more complete datastore if the full information is needed. After prefiltering, the elasticsearch database can accomplish it's goal of being a filtering mechanism while only taking 30% of the original raw JSON disk space.

<h4>Is that really necessary? Can't we just store everything in elasticsearch?</h4>

elasticsearch commits aggregation by first pulling the entire data field into ram. Given the original size of a month's worth of data in ~30GB, this makes elasticsearch unuseable for aggregation counts without the steps of prefiltering and breaking into multiple tables which I have taken.

<h4>Why are the queries slow? Can't we cache the possible queries?</h4>
There are ~100k subreddits and ~1M English words. Assuming it takes 1 second to cache a query, caching 1% of subreddits for 1% of english words would take 1K * 100K = 10M seconds, or ~116 days.

#6: Okay, how well did everything finally work out?

<h3>Performance</h3>

For performance, this setup was acceptable, though not amazing. The first query for an elasticsearch month block took upwards of 30 seconds. However, each additional query from the same month block would be much faster, takin usually around a second. 

The cassandra return time was suboptimal. Given the queries are for arbitrary words on users of abritrary subreddits, there is no natural partitioning pattern for cassandra. Pulling out original comments from cassandra happened at the rate of ~50 a second. 

<h3>Accuracy</h3>

elasticsearch aggregation is actually as estimate, so I tested it's accuracy claims by comparison against the original comments stored in cassandra. Results were surprisingly bad: for a common word aggregation done on "cat" on the "programming" subreddit for the posts in June of 2008, the elasticsearch query returned a result of 482 instance of the word cat, whereas cassandra return 550 instances of the word cat, for an error rate of (550 - 482) / 482 = ~15% margin of error. 

<h4>Methods<h4>

The cassandra count is found by first storing a dictionary of words with their frequency in the comment in each cassandra record. Then, all records who's metadata was queried in elasticsearch are pulled from cassandra and a sum is done over the dictionaries by key. The respective code for each step is stored in the spark/reddit_to_cassandra.py file and the flask-app/cassandra-helper.py files. Time was a limiting factor for this project, so further testing is needed to verify my results.




