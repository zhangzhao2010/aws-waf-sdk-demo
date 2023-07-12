import boto3

# v2
client = boto3.client('wafv2')

# classic
# client = boto3.client('waf-regional')

response = client.list_resources_for_web_acl(
    WebACLArn='string',
    ResourceType='APPLICATION_LOAD_BALANCER'|'API_GATEWAY'|'APPSYNC'|'COGNITO_USER_POOL'|'APP_RUNNER_SERVICE'|'VERIFIED_ACCESS_INSTANCE'
)

print(response)
