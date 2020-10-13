# ====================================================================
# TERRAFORM LAMBDAS
# ====================================================================
#   This module handles lambda functions
#  - Ensure all resources have tags
#  - Ensure everything has a description

resource "aws_lambda_function" "test" {
  function_name = "test_function"
  s3_bucket = var.test_lambda_function_bucket
  s3_key = var.test_lambda_function_key
  runtime = "python3.8"
  handler = "test.test"
  role = var.lambda_execution_role
}