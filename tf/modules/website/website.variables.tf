variable "website_endpoints" {
  type = list(string)
  description = "names of the endpoints from the s3 buckets"
}

variable "domains" {
  type = list(string)
  description = "full list of domains being used"
}

variable "full_domain" {
  type = string
  description = "The prefixed domain name for the website"
}

variable "tags" {
  type = map(string)
  description = "map of tags that get applied to all younify objects"
}

variable "domain" {
  type = string
  description = "The non-prefixed domain name for the website"
}
