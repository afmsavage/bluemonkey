
import bluemonkey as bm
import boto3
import botocore

from flask import Flask
app = Flask(__name__)

@app.route('/')
def label():
  bm.tag_iterator()
  return 'Labeling...' # test return