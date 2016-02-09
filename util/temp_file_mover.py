from boto.s3.connection import S3Connection
from os import environ
import os

def main():
    conn = S3Connection(environ['AWS_ACCESS_KEY_ID'], environ['AWS_SECRET_ACCESS_KEY'])
    bucket = conn.get_bucket('mark-wang-test')


    for key in bucket.list(prefix='reddit-es-comments-json/2015_12/_temporary'):
        if key.name.split('-')[-2][-4:] == 'part':
            filename = key.name.split('/')[-1]
            os.system('aws s3 --region us-west-2 mv s3://mark-wang-test/{0} s3://mark-wang-test/reddit-es-comments-json/2015_12/{1}'.format(key.name, filename))

if __name__ == '__main__':
    main()
