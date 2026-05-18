# --- AWS EMR Serverless Specific Infrastructure ---
resource "aws_emrserverless_application" "spark_app" {
  name          = "${var.project_prefix}-emr-serverless-${var.environment}"
  release_label = "emr-6.10.0"
  type          = "SPARK"

  initial_capacity {
    initial_capacity_type = "Driver"
    initial_capacity_config {
      worker_count = 1
      worker_configuration {
        cpu    = "2 vCPU"
        memory = "4 GB"
      }
    }
  }

  maximum_capacity {
    cpu    = "16 vCPU"
    memory = "64 GB"
  }
}

resource "aws_iam_role" "emr_serverless_role" {
  name = "${var.project_prefix}-emrs-role-${var.environment}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "emr-serverless.amazonaws.com" }
    }]
  })
}
