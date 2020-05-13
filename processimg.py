#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

# TODO:
# Process the output and find any labels that are 90%+
# Figure out how to apply the labels to the images in s3
# Recursively search through the s3 bucket for image files to process
# Place some sort of tag or label on items that have been processed
# Identify images that have been processed and do not process them again
# Have some sort of logging to identify images that were processed and ones that failed

# INFO:
# https://docs.aws.amazon.com/rekognition/latest/dg/images-s3.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
#
# INFO: tag s3 objects
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_tagging


import boto3

def detect_labels(photo, bucket):

    client=boto3.client('rekognition')

    response = client.detect_labels(
        Image={
            'S3Object':{
                'Bucket':bucket,
                'Name':photo
            },
        },
        MaxLabels=10,
        MinConfidence=90
    )
    # Testing output
    print('Detected labels for ' + photo)
    print()
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']))
        print ("Instances:")
        for instance in label['Instances']:
            print ("  Bounding box")
            # print ("    Top: " + str(instance['BoundingBox']['Top']))
            # print ("    Left: " + str(instance['BoundingBox']['Left']))
            # print ("    Width: " +  str(instance['BoundingBox']['Width']))
            # print ("    Height: " +  str(instance['BoundingBox']['Height']))
            print ("  Confidence: " + str(instance['Confidence']))
            print()

        print ("Parents:")
        for parent in label['Parents']:
            print ("   " + parent['Name'])
        print ("----------")
        print ()
    return len(response['Labels'])


def main():
    photo='sample/bluemonkeycartoon.jpg'
    bucket='bluemonkeyimages'
    label_count=detect_labels(photo, bucket)
    print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    main()
