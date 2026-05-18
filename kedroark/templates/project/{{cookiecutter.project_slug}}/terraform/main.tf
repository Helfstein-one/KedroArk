# Main infrastructure module router

{% if cookiecutter.compute_target == 'AWS Glue' %}
module "compute" {
  source = "./glue"

  project_prefix      = var.project_prefix
  environment         = var.environment
  artifacts_bucket_id = aws_s3_bucket.artifacts_bucket.id
}
{% elif cookiecutter.compute_target == 'AWS EMR' %}
module "compute" {
  source = "./emr"

  project_prefix      = var.project_prefix
  environment         = var.environment
}
{% elif cookiecutter.compute_target == 'AWS EMR Serverless' %}
module "compute" {
  source = "./emr_serverless"

  project_prefix      = var.project_prefix
  environment         = var.environment
}
{% endif %}
