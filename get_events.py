import boto3
import time
import json
import group

client = boto3.client('logs')


def download_events(start_time, end_time):
    """download CloudTrail event published to a CloudWatch logs group"""
    token = None
    while True:
        if token:
            response = client.filter_log_events(
                logGroupName='CloudTrail/logs',
                startTime=start_time,
                endTime=end_time,
                nextToken=token)
        else:
            response = client.filter_log_events(
                logGroupName='CloudTrail/logs',
                startTime=start_time,
                endTime=end_time)
        for e in response['events']:
            yield e
        if 'nextToken' not in response:
            break
        print("Read {0}. More events to read".format(len(response['events'])))
        token = response['nextToken']


def save_events(events, filename):
    """a generator intended to be chained, save each event in events"""
    with open(filename, 'w') as f:
        for e in events:
            json.dump(e, f)
            f.write("\n")
            yield e


# Download recent CloudTrail events published to CloudWatch logs

if __name__ == "__main__":
    startTime = int(time.time() * 1000) - 4 * 3600 * 1000
    endTime = startTime + (10 * 60 * 1000)

    group.process(save_events(download_events(startTime, endTime), 'events.json'))
