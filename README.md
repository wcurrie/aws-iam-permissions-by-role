## What?

Attempting to divine the IAM permissions needed by a given AWS Role.

Idea:

1. grant permissive IAM permissions to your new IAM role (eg '*')
2. do something in your AWS account with the role
3. observe set of services (permissions) consumed by the Role by running main.py
4. reduce privileges
5. try using role again
6. weep or move on to next task

## Setup:

Needs CloudTrail enabled and publishing logs to a CloudWatch Logs group named 'CloudTrail/logs'

## Example Output:

From a modified version of [rolemodel](https://github.com/scopely-devops/rolemodel):

    arn:aws:iam::123456789012:role/RoleMaintainer
      cloudformation:DescribeStacks 106
      cloudformation:DescribeStackResources 8
      cloudformation:UpdateStack 3
      cloudformation:ValidateTemplate 7
      iam:GetRole 35
      cloudformation:CreateStack 4
      iam:CreateRole 14
      iam:PutRolePolicy 4
      iam:AttachRolePolicy 1
    arn:aws:iam::123456789012:role/IdentityMaintainer
      iam:GetGroupPolicy 20
      iam:ListGroupPolicies 40
      iam:ListGroups 4
      iam:GetUser 10
      iam:GetGroup 4
      iam:AddUserToGroup 27
      iam:PutGroupPolicy 20
      iam:CreateGroup 10
      iam:CreateUser 2
      iam:CreateLoginProfile 2

From some human:

    arn:aws:iam::123456789012:user/some_developer
      kms:Decrypt 13
      codecommit:GitPush 2