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

# Modules called in below

module "objects" {
  source = "./modules/objects"
}