from boto.s3.connection import S3Connection
from os import environ
import os

def main():
    conn = S3Connection(environ['AWS_ACCESS_KEY_ID'], environ['AWS_SECRET_ACCESS_KEY'])
    bucket = conn.get_bucket('mark-wang-test')

    for i in range(1,13):
        for key in bucket.list(prefix='reddit-finished/2014_{0}'.format(str(i).zfill(2))):
            filename = key.name.split('/')[-1]
            os.system('aws s3 --region us-west-2 mv s3://mark-wang-test/reddit-finished/2014_{1}/{0} s3://mark-wang-test/reddit-es-comments-json/2014_{1}/{0}'.format(filename, str(i).zfill(2)))

if __name__ == '__main__':
    main()
