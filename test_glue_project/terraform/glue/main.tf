# --- AWS Glue Specific Infrastructure ---
resource "aws_iam_role" "glue_role" {
  name = "${var.project_prefix}-glue-role-${var.environment}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

# Attach AWS managed policies to the Glue role
resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy_attachment" "glue_s3" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# --- AWS Glue Data Catalog ---
resource "aws_glue_catalog_database" "kedro_db" {
  name        = "${var.project_prefix}_db_${var.environment}"
  description = "Glue Catalog Database for Kedro Pipeline ${var.project_prefix}"
}

# --- AWS Glue Artifacts (Managed by Terraform) ---
resource "aws_s3_object" "glue_script" {
  bucket = var.artifacts_bucket_id
  key    = "scripts/main.py"
  source = "${path.root}/../src/main.py"
  etag   = filemd5("${path.root}/../src/main.py")
}

resource "aws_glue_job" "kedro_job" {
  name     = "${var.project_prefix}-etl-job-${var.environment}"
  role_arn = aws_iam_role.glue_role.arn

  command {
    script_location = "s3://${var.artifacts_bucket_id}/${aws_s3_object.glue_script.key}"
    python_version  = "3"
  }

  default_arguments = {
    "--extra-py-files" = "s3://${var.artifacts_bucket_id}/packages/test_glue_project-0.1.0-py3-none-any.whl"
  }
  
  glue_version = "4.0"
  worker_type  = "G.1X"
  number_of_workers = 2
}
