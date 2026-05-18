# Main infrastructure module router


module "compute" {
  source = "./glue"

  project_prefix      = var.project_prefix
  environment         = var.environment
  artifacts_bucket_id = aws_s3_bucket.artifacts_bucket.id
}

