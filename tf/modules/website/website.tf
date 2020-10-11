
# ====================================================================
# TERRAFORM WEBSITE
# ====================================================================
#   This module handles cloudfront distribution and certification
#   Based on work done by Gabro: https://github.com/buildo/terraform-aws-website

provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}

resource "aws_cloudfront_distribution" "cdn" {
  count = length(var.domains)
  enabled = true
  default_root_object = element(var.domains, count.index) == var.full_domain ? "index.html" : ""
  aliases = [element(var.domains, count.index)]
  is_ipv6_enabled = true
  origin {
    domain_name = element(var.website_endpoints, count.index)
    origin_id   = "S3-${element(var.domains, count.index)}"
    custom_origin_config {
      http_port                = "80"
      https_port               = "443"
      origin_keepalive_timeout = 5
      origin_protocol_policy   = "http-only"
      origin_ssl_protocols     = ["TLSv1", "TLSv1.1", "TLSv1.2"]
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn = element(data.aws_acm_certificate.ssl.*.arn, count.index)
    minimum_protocol_version = "TLSv1"
    ssl_support_method = "sni-only"
  }

  default_cache_behavior {
    allowed_methods = ["GET", "HEAD"]
    cached_methods = ["GET", "HEAD"]
    target_origin_id = "S3-${element(var.domains, count.index)}"
    compress = true
    viewer_protocol_policy = "redirect-to-https"
    min_ttl = 0
    default_ttl = 86400
    max_ttl = 31536000

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  custom_error_response {
    error_code            = 403
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 300
  }

  custom_error_response {
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 300
  }

  tags = var.tags
}

data "aws_route53_zone" "zone" {
  name = var.domain
}

resource "aws_route53_record" "ip4" {
  count   = length(var.domains)
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = element(var.domains, count.index)
  type    = "A"
  alias {
    name                   = element(aws_cloudfront_distribution.cdn.*.domain_name, count.index)
    zone_id                = element(aws_cloudfront_distribution.cdn.*.hosted_zone_id, count.index)
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "AAAA" {
  count   = length(var.domains)
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = element(var.domains, count.index)
  type    = "AAAA"

  alias {
    name                   = element(aws_cloudfront_distribution.cdn.*.domain_name, count.index)
    zone_id                = element(aws_cloudfront_distribution.cdn.*.hosted_zone_id, count.index)
    evaluate_target_health = false
  }
}

data "aws_acm_certificate" "ssl" {
  count    = length(var.domains)
  provider = aws.us-east-1
  domain   = var.full_domain
  statuses = ["ISSUED"]
}