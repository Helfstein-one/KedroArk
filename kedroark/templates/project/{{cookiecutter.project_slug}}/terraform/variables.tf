variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "project_prefix" {
  type    = string
  default = "{{ cookiecutter.project_slug }}"
}
