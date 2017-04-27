import json
import re
from collections import defaultdict


def events_from_file(filename):
    """read previously downloaded events"""
    with open(filename) as f:
        while True:
            line = f.readline()
            if not line:
                break
            yield json.loads(line)


def process(events):
    """group CloudTrail events by invoking ARN and required iam permission"""
    events_by_arn = defaultdict(list)
    for event_wrapper in events:
        event = json.loads(event_wrapper['message'])
        try:
            arn = invoker_arn(event)
            event_name = event['eventName']
            event_source = re.sub(r'([^.]+).*', '\\1', event['eventSource'])  # drop amazonaws.com suffix
            events_by_arn[arn].append(event_source + ":" + event_name)
        except Exception as e:
            print("Ignoring error")
            print(e)
            pass

    for arn, events in events_by_arn.items():
        counts_by_event = {}
        for event in events:
            counts_by_event[event] = counts_by_event.get(event, 0) + 1

        print(arn)
        for event, count in counts_by_event.items():
            print("  {0} {1}".format(event, count))


def invoker_arn(event):
    if event['userIdentity']['type'] == 'AWSService':
        arn = event['requestParameters']['roleArn']
    elif event['userIdentity']['type'] == 'AWSAccount':
        arn = event['requestParameters']['roleArn']
    elif event['userIdentity']['type'] == 'IAMUser':
        arn = event['userIdentity']['arn']
    elif event['userIdentity']['type'] == 'AssumedRole':
        arn = event['userIdentity']['sessionContext']['sessionIssuer']['arn']
    elif event['userIdentity']['type'] == 'Root':
        arn = event['userIdentity']['arn']
    else:
        raise Exception("Dunno about {0}".format(json.dumps(event)))
    return arn


if __name__ == "__main__":
    process(events_from_file('events.json'))
