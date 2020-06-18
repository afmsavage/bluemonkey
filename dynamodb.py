#!/usr/bin/env python3


# Testing out some DynamoDB calls through boto3
import boto3
dynamodb = boto3.resource('dynamodb')
  table = dynamodb.create_table(
    TableName = 'labels',
    KeySchema=[
      {
        'AttributeName': 'label',
        'KeyType': 'S'
      },
      {
        'AttributeName': ''
      }
    ]
  )