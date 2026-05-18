variable "project_prefix" {
  type        = string
  description = "Prefix for project resources"
}

variable "environment" {
  type        = string
  description = "Deployment environment (dev, prod, etc)"
}

variable "artifacts_bucket_id" {
  type        = string
  description = "The S3 bucket ID for uploading Glue scripts and packages"
}
