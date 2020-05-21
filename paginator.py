import boto3

photo = ''
bucket_name = 'bluemonkeyimages'

# paginator to gather s3 objects
s3 = boto3.client('s3')

paginator = s3.get_paginator('list_objects_v2')
page_iterator = paginator.paginate(
                                Bucket=bucket_name,
                                PaginationConfig={
                                    'PageSize': 1
                                }
)

for page in page_iterator:
    print('--page--')
    for key in page['Contents']:
        print(key['Key'])
        print('---next page---')