import boto3

photo = ''
bucket_name = 'bluemonkeyimages'

# paginator to gather s3 objects
client = boto3.client('s3')

paginator = client.get_paginator('list_objects')

page_iterator = paginator.paginate(Bucket=bucket_name)

for page in page_iterator:
    print(page['Key'])