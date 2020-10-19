# ====================================================================
# VARIABLE DECLARATION
# ====================================================================

variable "profile" {
  type = string
  description = "name of the AWS profile to pick up from the local machine"
  default = "default"
}
variable "tags" {
  type = map(string)
  description = "map of tags that get applied to all younify objects"
}

## ARTIFACTS
variable "app_lambdas" {
  type = string
  description = "folder containing the lambda deployables"
}