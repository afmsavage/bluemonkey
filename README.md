# Bluemonkey

Boto3 script which processes images stored in an S3 bucket with [AWS Rekognition](https://aws.amazon.com/rekognition/).  The detected labels are then placed as tags on the image file for searchability.  Utilizes pagination to be able to process any number of images.

[Terraform](https://www.terraform.io/) included for creating S3 bucket too
