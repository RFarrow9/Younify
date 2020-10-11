output "website_endpoints" {
  value = [
    aws_s3_bucket.website_redirect.website_endpoint,
    aws_s3_bucket.website_main.website_endpoint
  ]
  description = "names of the endpoints from the s3 buckets"
}

output "domains" {
  value = local.domains
  description = "full list of domains being used"
}