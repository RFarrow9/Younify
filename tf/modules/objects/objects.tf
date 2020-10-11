
# ====================================================================
# TERRAFORM OBJECTS
# ====================================================================
#   This module handles objects and buckets
#  - Ensure all objects have etags
#  - Ensure all resources have tags
#  - Ensure everything has a description

locals {
  domains = [
    var.domain,
    var.full_domain
  ]
}

resource "aws_s3_bucket" "website_main" {
  bucket = var.domain
  tags = var.tags
  website {
    index_document = "index.html"
    error_document = "index.html"
  }
}

resource "aws_s3_bucket" "website_redirect" {
  bucket = var.full_domain
  tags = var.tags
  website {
    redirect_all_requests_to = aws_s3_bucket.website_main.id
  }
}

resource "aws_s3_bucket" "engineering" {
  bucket = "younify_engineering"
  acl = "private"
  tags = var.tags
}