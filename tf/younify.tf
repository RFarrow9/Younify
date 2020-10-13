#==================================================#
# YOUNIFY INFRASTRUCTURE                           #
#==================================================#
#
#

terraform {
  backend "s3" {
  }
}

provider "aws" {
  version = "~> 2.0"
  profile = var.profile
  region = "eu-west-1"
}

locals {
  domain = "younify.co.uk"
  full_domain = "www.younify.co.uk"
}

# Modules called in below
module "objects" {
  source = "./modules/objects"
  domain = local.domain
  full_domain = local.full_domain
  tags = var.tags
  lambda_test_function = var.lambda_test_function
}

module "lambda" {
  source = "./modules/lambda"
  test_lambda_function_bucket = module.objects.test_lambda_function_bucket
  test_lambda_function_key = module.objects.test_lambda_function_key
  lambda_execution_role = module.security.lambda_execution_role
}

module "gateway" {
  source = "./modules/gateway"
}

module "website" {
  source = "./modules/website"
  website_endpoints = module.objects.website_endpoints
  domains = module.objects.domains
  tags = var.tags
  domain = local.domain
  full_domain = local.full_domain
}

module "monitoring" {
  source = "./modules/monitoring"
}

module "security" {
  source = "./modules/security"
}