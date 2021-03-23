
# ====================================================================
# TERRAFORM SECURITY
# ====================================================================
#   This module handles objects and buckets
#  - Ensure all objects have etags
#  - Ensure all resources have tags
#  - Ensure everything has a description

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.allow_lambda_execution.json
}

data "aws_iam_policy_document" "allow_lambda_execution" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type = "Service"
    }
    effect = "Allow"
  }
}