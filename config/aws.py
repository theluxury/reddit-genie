from os import environ

REGION = 'us-west-2'
AWS_ACCESS_KEY_ID = environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = environ['AWS_SECRET_ACCESS_KEY']
MY_BUCKET = 'mark-wang-test'
MY_BUCKET_S3_REDDIT_PREFIX = 'reddit-es-comments-json'
MY_BUCKET_S3_FINISHED_PREFIX = 'reddit-finished'
RAW_JSON_REDDIT_BUCKET = 'reddit-comments'
