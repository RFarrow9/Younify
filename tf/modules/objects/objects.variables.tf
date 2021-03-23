variable "domain" {
  type = string
  description = "The non-prefixed domain name for the website"
}

variable "full_domain" {
  type = string
  description = "The prefixed domain name for the website"
}

variable "tags" {
  type = map(string)
  description = "map of tags that get applied to all younify objects"
}

## ARTIFACTS
variable "app_lambdas" {
  type = string
  description = "lambda test function for deployment"
}
