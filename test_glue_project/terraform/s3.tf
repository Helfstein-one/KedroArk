# Base S3 Buckets for Data and Artifacts
resource "aws_s3_bucket" "data_bucket" {
  bucket = "${var.project_prefix}-data-bucket-${var.environment}"
}

resource "aws_s3_bucket" "artifacts_bucket" {
  bucket = "${var.project_prefix}-artifacts-${var.environment}"
}
