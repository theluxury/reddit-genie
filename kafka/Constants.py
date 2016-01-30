from os import environ

CONSUMER_KEY = environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = environ.get('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = environ.get('TWITTER_ACCESS_SECRET')

ONE_HUNDRED_MOST_COMMON_WORDS = ["the", "be", "and", "of", "a", "in", "to", "have", "it", "I", "that", "for", "you", "he", "with", "on", "do", "say", "this", "they", "at", "but", "we", "his", "from", "not", "by", "she", "or", "as", "what", "go", "their", "can", "who", "get", "if", "would", "her", "all", "my", "make", "about", "know", "will", "up", "one", "time", "there", "year", "so", "think", "when", "which", "them", "some", "me", "people", "take", "out", "into", "just", "see", "him", "your", "come", "could", "now", "than", "like", "other", "how", "then", "its", "our", "two", "more", "these", "want", "way", "look", "first", "also", "new", "because", "day", "use", "no", "man", "find", "here", "thing", "give", "many", "well", "only", "those", "tell", "very", "even"]

BATCH_SEND_EVERY_N = 100
BATCH_SEND_EVERY_T = 30
ERROR_LOG_FILENAME = "error_log.txt"

SET_OF_WORDS_TO_REMOVE = {"the", "be", "and", "of", "a", "in", "to", "have", "it", "I", "that", "for", "you", "he", "with", "on", "do", "say", "this", "they", "at", "but", "we", "his", "from", "not", "by", "she", "or", "as", "what", "go", "their", "can", "who", "get", "if", "would", "her", "all", "my", "make", "about", "know", "will", "up", "one", "time", "there", "year", "so", "think", "when", "which", "them", "some", "me", "people", "take", "out", "into", "just", "see", "him", "your", "come", "could", "now", "than", "like", "other", "how", "then", "its", "our", "two", "moe", "these", "want", "way", "look", "first", "also", "new", "because", "day", "use", "no", "man", "find", "here", "thing", "give", "many", "well", "only", "those", "tell", "very", "even"}
