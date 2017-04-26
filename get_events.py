import boto3
import time
import json

client = boto3.client('logs')

startTime = int(time.time() * 1000) - 4 * 3600 * 1000
endTime = startTime + (10 * 60 * 1000)

# Download recent CloudTrail events published to CloudWatch logs

with open('events.json', 'w') as f:
    token = None
    while True:
        if token:
            response = client.filter_log_events(
                logGroupName='CloudTrail/logs',
                startTime=startTime,
                endTime=endTime,
                nextToken=token)
        else:
            response = client.filter_log_events(
                logGroupName='CloudTrail/logs',
                startTime=startTime,
                endTime=endTime)
        for e in response['events']:
            json.dump(e, f)
            f.write("\n")
        print("Read {0}. More events to read".format(len(response['events'])))
        if 'nextToken' not in response:
            break
        token = response['nextToken']
