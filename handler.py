import logging
import requests
from datetime import datetime
import os
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
bucket_resource = s3

endpoints = ['https://api.sleeper.app/v1/players/nfl','https://api.sleeper.app/v1/players/nfl/trending/add','https://api.sleeper.app/v1/players/nfl/trending/drop']

def run(event, context):
    logger.info("Getting SleeperApp data")
    for url in endpoints:
        get_sleeper_data(url)

def get_sleeper_data(url):
    type = url.split('/')[-1]
    date = datetime.today().strftime('%Y%m%d')
    req = requests.get(url)
    file = "nflPlayers_{}_{}.json".format(type, date)
    filepath = '/tmp/'
    key = "{}/{}/{}/{}/{}".format(date[0:4], date[4:6], date[6:8], type, file)

    if req.status_code == 200:
        print('200 OK')
        with open(filepath + file, 'w+') as f:
            f.write(req.text)
        bucket_resource.upload_file(
            Bucket='nfl-players-data',
            Filename= filepath + file,
            Key=key
        )
    else:
        print('error getting players')
