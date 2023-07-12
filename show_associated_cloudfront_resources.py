import boto3

# 获取web acl id 关联的Cloudfront资源
def get_associated_cloudfront_resources(web_acl_id):
    cloudfront_client = boto3.client('cloudfront')
    distributions_response = cloudfront_client.list_distributions_by_web_acl_id(WebACLId=web_acl_id)

    associated_resources = []

    if distributions_response['DistributionList']['Quantity'] == 0:
        print('no_associated_resources_for', web_acl_id)
        return associated_resources

    for distribution in distributions_response['DistributionList']['Items']:
        associated_resources.append(distribution['Id'])

    print('associated_resources_id:', associated_resources)
    return associated_resources

if __name__ == '__main__':
    # classic 使用 Id（如：xxxxxxxx-f760-4c29-8fdd-baa0axxxxxxx），wafv2使用ARN(如：arn:aws:wafv2:us-east-1:012321321312:global/webacl/cloudfront/xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx)
    web_acl_id = ''
    get_associated_cloudfront_resources(web_acl_id)