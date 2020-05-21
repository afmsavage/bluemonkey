#!/usr/bin/env python3

import boto3
import botocore
import datetime

# logging
dt = datetime.datetime.now()
timestamp = dt.strftime('%Y%m%d%H%M')

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
    for labels in response['Labels']:
        tag_list.append({'Key': labels['Name'],
                        'Value': 'True'})
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
        logfile = open(f'{timestamp}.log', 'w')
        logfile.write(f'Could not apply labels to {image}.')
        logfile.write(error)
        raise error

def tag_iterator():
    total = 0
    # pagination through all images
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(
        Bucket=bucket_name,
        PaginationConfig={
            'PageSize': 50 # lessen if errors
        }
    )
    for page in page_iterator:
        for key in page['Contents']:
            create_tagset(key['Key'])
            total += 1
    print('Complete!')
    print(f'Processed {total} images!')

if __name__ == '__main__':
    tag_iterator()
