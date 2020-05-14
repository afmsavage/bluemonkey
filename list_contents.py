
import boto3

bucket_name = 'bluemonkeyimages'

client = boto3.client('s3')
response = client.list_objects_v2(
  Bucket=bucket_name
)

for key in response['Contents']:
    print(key['Key'])
    print('----')
