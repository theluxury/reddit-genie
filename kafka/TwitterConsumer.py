import tweepy 
import yaml
import kafka
import json
import Constants

config = yaml.safe_load(open("tweepy.yaml"))
auth = tweepy.OAuthHandler(config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
auth.set_access_token(config['ACCESS_TOKEN'], config['ACCESS_SECRET'])
api = tweepy.API(auth)
ONE_HUNDRED_MOST_COMMON_WORDS = Constants.ONE_HUNDRED_MOST_COMMON_WORDS
BATCH_SEND_EVERY_N = Constants.BATCH_SEND_EVERY_N
BATCH_SEND_EVERY_T = Constants.BATCH_SEND_EVERY_T
ERROR_LOG_FILENAME = Constants.ERROR_LOG_FILENAME

class KafkaListener(tweepy.StreamListener):
    def __init__(self, topic):
        self.topic = topic
        client = kafka.KafkaClient('localhost:9092')
        self.producer = kafka.SimpleProducer(client, async=True, batch_send_every_n=BATCH_SEND_EVERY_N, batch_send_every_t=BATCH_SEND_EVERY_T)
     
    def on_data(self, data):
        tweetJsonString = data.encode('utf-8')
        tweetJson = json.loads(tweetJsonString)
        #occasionally there are timestamp tweets that are irrelavant. This parses them.
        if 'id' not in tweetJson: 
            return
        self.producer.send_messages(self.topic, data.encode('utf-8'))

    def on_error(self, error):
        print "ERROR: " + error
        if not os.path.isfile(ERROR_LOG_FILENAME):
            f = file(ERROR_LOG_FILENAME, 'w')
            f.close()
        with open(logfilename, 'ab') as f:
            f.write(datetime.now())
            f.write(error)

myStreamListener = KafkaListener("my-topic")
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(languages=['en'], track=ONE_HUNDRED_MOST_COMMON_WORDS)
