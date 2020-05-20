
# Bluemonkey
# Antonio Savage
# v0.0.1
#
# Processes images stored in AWS S3 buckets with Rekognition.
# Applies the detected labels to each image to make them searchable
#

# TODO:
# Recursively search through the s3 bucket for image files to process
# Add Pagination to the s3 list function so that it can handle the sheer amount of images we have to process
# Identify images that have been processed and do not process them again
# Have some sort of logging to identify images that were processed and ones that failed
# Error handling

# INFO:
# https://docs.aws.amazon.com/rekognition/latest/dg/images-s3.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
#
# INFO: tag s3 objects
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_tagging
# Batch Actions
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/collections.html#guide-collections
# Paginators
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html


import boto3
import botocore
s3 = boto3.client('s3')
photo = ''
bucket_name = 'bluemonkeyimages'
client = boto3.client('rekognition')


def create_tagset(photo):
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': photo
            },
        },
    )
    tag_list = []
    for t in response['Labels']:
        tag_list.append({'Key': t['Name'],
                        'Value': 'True'})
    print(tag_list)
    try:
        s3.put_object_tagging(
            Bucket=bucket_name,
            Key=photo,
            Tagging={
                'Tagset': tag_list
            }
        )
    except botocore.exceptions.ClientError as error:
        print(f"could not apply labels to {photo}")
        raise error

    except botocore.exceptions.ParamValidationError as error:
        raise ValueError(
            'The parameters you provided are incorrect: {}'.format(error))


s3response = s3.list_objects_v2(
    Bucket=bucket_name
)

if __name__ == "__main__":

    for key in s3response['Contents']:
        create_tagset(key['Key'])
