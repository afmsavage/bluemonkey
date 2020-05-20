
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
s3 = boto3.client('s3')
photo = ''
bucket_name = 'bluemonkeytest'

def detect_labels(photo):

    client = boto3.client('rekognition')

    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': photo
            },
        },
        #    MaxLabels=10,
        #  MinConfidence=90
    )
    # Testing output for labels
    print('Detected labels for ' + photo)
    print()
    for label in response['Labels']:
        print("Label: " + label['Name'])
        print("Confidence: " + str(label['Confidence']))
        print("----------")
        print()
        # apply Rekonition labels to image files

        tagset = []
        dict = {'Key': f"{label['Name']}", 'Value': "True"}
        tagset.append(dict)


    try:
        s3.put_object_tagging(
                    Bucket=bucket_name,
                    Key=photo,
                    Tagging={
                        'Tagset': tagset
                    }
                )
    except:
        print(f"could not apply {label['Name']} to {photo}")
        # TODO: Log error to file
    # TODO: Add a tag to say this image is processed

# TODO: Add pagination to this so that it can handle the amount of images we need to process
s3response = s3.list_objects_v2(
    Bucket=bucket_name
)

if __name__ == "__main__":

    for key in s3response['Contents']:
        detect_labels(key['Key'])

