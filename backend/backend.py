
import boto3
import botocore

from flask import Flask
app = Flask(__name__)

@app.route('/')
def label():
  return 'Labeling...' # test return
