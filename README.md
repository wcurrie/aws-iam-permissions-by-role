Attempting to divine the IAM permissions needed by a given AWS Role.

Idea:

1. grant permissive IAM permissions
2. observe set of services (permissions) consumed by the Role by running main.py
3. reduce privileges
4. try using role again
5. weep or move on to next task

Setup:

Needs CloudTrail enabled and publishing logs to a CloudWatch Logs group named 'CloudTrail/logs'
