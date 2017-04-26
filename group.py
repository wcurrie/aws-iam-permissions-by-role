import json
import re
from collections import defaultdict

# group CloudTrail events by invoking ARN and required iam permission

events_by_arn = defaultdict(list)

with open('events.json') as f:
    while True:
        line = f.readline()
        if not line:
            break

        eventWrapper = json.loads(line)
        event = json.loads(eventWrapper['message'])
        if event['userIdentity']['type'] == 'AWSService':
            arn = event['requestParameters']['roleArn']
        elif event['userIdentity']['type'] == 'AWSAccount':
            arn = event['requestParameters']['roleArn']
        elif event['userIdentity']['type'] == 'IAMUser':
            arn = event['userIdentity']['arn']
        elif event['userIdentity']['type'] == 'AssumedRole':
            arn = event['userIdentity']['sessionContext']['sessionIssuer']['arn']
        else:
            raise "Dunno about {0}".format(line)
        eventName = event['eventName']
        eventSource = re.sub(r'([^.]+).*', '\\1', event['eventSource'])

        events_by_arn[arn].append(eventSource + ":" + eventName)

for arn, events in events_by_arn.items():
    counts_by_event = {}
    for event in events:
        counts_by_event[event] = counts_by_event.get(event, 0) + 1

    print(arn)
    for event, count in counts_by_event.items():
        print("  {0} {1}".format(event, count))
