# --- AWS EMR Specific Infrastructure ---
resource "aws_emr_cluster" "cluster" {
  name          = "${var.project_prefix}-emr-cluster-${var.environment}"
  release_label = "emr-6.10.0"
  applications  = ["Spark", "Hadoop", "Hive"]

  service_role = aws_iam_role.emr_service_role.arn

  ec2_attributes {
    instance_profile = aws_iam_instance_profile.emr_ec2_profile.arn
  }

  master_instance_group {
    instance_type  = "m5.xlarge"
    instance_count = 1
  }

  core_instance_group {
    instance_type  = "m5.xlarge"
    instance_count = 2
  }
}

resource "aws_iam_role" "emr_service_role" {
  name = "${var.project_prefix}-emr-service-role-${var.environment}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "elasticmapreduce.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role" "emr_ec2_role" {
  name = "${var.project_prefix}-emr-ec2-role-${var.environment}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_instance_profile" "emr_ec2_profile" {
  name = "${var.project_prefix}-emr-ec2-profile-${var.environment}"
  role = aws_iam_role.emr_ec2_role.name
}
