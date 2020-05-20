import boto3
import botocore
import datetime

# logging
dt = datetime.datetime.now()
timestamp = dt.strftime('%Y%m%d%H%M')
logfile = open(f'{timestamp}.log', 'w')

photo = ''
bucket_name = 'bluemonkeyimages'
s3 = boto3.client('s3')
client = boto3.client('rekognition')

def create_tagset(image):
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': image
            },
        },
        MaxLabels=10,
    )
    tag_list = []
    for t in response['Labels']:
        tag_list.append({'Key': t['Name'],
                        'Value': 'True'})
    print(tag_list)
    try:
        s3.put_object_tagging(
            Bucket=bucket_name,
            Key=image,
            Tagging={
                'TagSet': tag_list
            }
        )
        # logfile.write(f'Successfully Processed {photo}')
    except botocore.exceptions.ClientError as error:
        logfile.write(f"could not apply labels to {image}")
        raise error

# pagination through all images
s3response = s3.list_objects_v2(
    Bucket=bucket_name
)

if __name__ == "__main__":

    for key in s3response['Contents']:
        create_tagset(key['Key'])
