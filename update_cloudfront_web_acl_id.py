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

# 更新Cloudfront分发的web acl id
def update_cloudfront_webacl(cloudfront_resource_id, web_acl_id):
    cloudfront_client = boto3.client('cloudfront')

    config_response = cloudfront_client.get_distribution_config(
        Id = cloudfront_resource_id
    )

    eTag = config_response['ETag']
    config = config_response['DistributionConfig']
    config['WebACLId'] = web_acl_id

    print('update info: ', {
        'Id': cloudfront_resource_id,
        'eTag': eTag,
        'WebACLId': web_acl_id
    })

    response = cloudfront_client.update_distribution(
        Id=cloudfront_resource_id,
        DistributionConfig=config,
        IfMatch=eTag
    )

    return response

if __name__ == '__main__':
    # 1. 通过旧的web_acl_id获取关联的cloudfront distribution
    # classic 使用 Id（如：xxxxxxxx-f760-4c29-8fdd-baa0axxxxxxx），wafv2使用ARN(如：arn:aws:wafv2:us-east-1:012321321312:global/webacl/cloudfront/xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx)
    oldWebAclId = 'xxxxxxx-f760-4c29-8fdd-baa0axxxxxxx'
    associated_resources = get_associated_cloudfront_resources(oldWebAclId)

    # 2. 更新cloudfront distribution的web_acl_id
    # classic 使用 xxxxxxx-f760-4c29-8fdd-baa0axxxxxxx），wafv2使用ARN(如：arn:aws:wafv2:us-east-1:012321321312:global/webacl/cloudfront/xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx)
    newWebAclId = 'arn:aws:wafv2:us-east-1:01222333333333:global/webacl/cloudfront/xxxxxxx-f760-4c29-8fdd-baa0axxxxxxx'
    for resource_id in associated_resources:
        res = update_cloudfront_webacl(resource_id, newWebAclId)