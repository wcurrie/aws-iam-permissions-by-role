import boto3
import datetime
import json
import group_by_arn

# boto3.set_stream_logger(name='botocore')
client = boto3.client('cloudtrail')

# depends only on cloudtrail being enabled


def download_events(start_time, end_time):
    """download CloudTrail event published to a CloudWatch logs group"""
    token = None
    while True:
        if token:
            response = client.lookup_events(
                StartTime=start_time,
                EndTime=end_time,
                NextToken=token)
        else:
            response = client.lookup_events(
                StartTime=start_time,
                EndTime=end_time)
        for e in response['Events']:
            yield e
        if 'NextToken' not in response:
            break
        print("Read {0}. More events to read".format(len(response['Events'])))
        token = response['NextToken']


def save_events(events, filename):
    """a generator intended to be chained, save each event in events"""
    with open(filename, 'w') as f:
        for e in events:
            # hack to make cloudtrail response look kinda like cloudwatch logs response
            event = {'message': e['CloudTrailEvent']}
            json.dump(event, f)
            f.write("\n")
            yield event


# Download recent CloudTrail events published to CloudWatch logs

if __name__ == "__main__":
    startTime = datetime.datetime.utcnow() - datetime.timedelta(hours=10)
    endTime = datetime.datetime.utcnow()

    print("Querying {0} to {1}".format(startTime, endTime))
    group_by_arn.process(save_events(download_events(startTime, endTime), 'events.json'))
