
provider "aws" {
  profile = "default"
  region  = "us-west-2"
}

resource "aws_s3_bucket" "bluemonkey_images" {
  bucket = "bluemonkeyimages"
  acl    = "private"
  tags = {
    "Project" = "bluemonkey"
  }
}
