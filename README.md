# KedroArk CLI

KedroArk is a scaffolding tool to generate highly scalable, standardized **Kedro** projects ready for deployment on **AWS (Glue, EMR, or EMR Serverless)**. It enforces advanced Big Data engineering practices such as Terraform IaC, Dev Containers, Data Catalog integration, and Pytest test pyramids.

## Features

- **Modular Kedro Structure**: Strict separation of nodes, pipelines, and config.
- **Compute Targeting**: Scaffolds infrastructure and configurations specifically for AWS Glue, EMR, or EMR Serverless.
- **Dev Containers**: Pre-configured Docker environment (`.devcontainer/`) with Java 11 and Python 3.10 for seamless local PySpark execution.
- **Mock Data Strategy**: Uses `Faker` to generate synthetic data for testing.
- **Testing Pyramid**: Pre-configured `pytest` with `unit`, `integration`, `e2e`, and `performance` markers.
- **CI/CD Workflow**: GitHub Actions workflow that lints, tests, and builds your Kedro wheel package (`.whl`) and simulates an S3 upload.
- **Terraform IaC**: Infrastructure as code to automatically provision buckets, IAM roles, and compute clusters depending on your target.
- **Dynamic Catalog**: Example of configuring `catalog.yml` for Iceberg outputs and AWS Glue Data Catalog integration.
- **Local Infrastructure Testing**: Spin up MinIO to simulate S3 with Docker Compose and test your Spark pipelines locally using `--local-infra` and `kedroark test-local`.
- **Financial Pipeline Example**: Optionally inject a realistic financial transaction pipeline using PySpark and Apache Iceberg.

## 🚀 Step-by-Step Guide

Follow these steps to generate and run your first Kedro pipeline for AWS.

### Step 1: Install KedroArk CLI

Install the KedroArk CLI locally so it becomes available in your terminal:

```bash
# Clone the repository (if you haven't)
cd KedroArk

# Install using pip (or Poetry)
pip install -e .
```

### Step 2: Initialize a New Project

Run the `kedroark init` command to scaffold a new project. You can choose your AWS target engine and optionally inject an example pipeline.

```bash
kedroark init my-awesome-project \
    --compute "AWS EMR Serverless" \
    --example finance \
    --local-infra
```

**Available Flags:**
- `--compute` or `-c`: Target compute engine (`AWS Glue`, `AWS EMR`, or `AWS EMR Serverless`).
- `--example` or `-e`: Pass `finance` to include the financial PySpark + Apache Iceberg pipeline example.
- `--local-infra` or `-l`: Automatically generates a Docker Compose setup with MinIO to simulate AWS S3 interactions.

### Step 3: Run the Local Environment (MinIO + Spark)

If you generated the project with the `--local-infra` flag, you can immediately test the execution of the pipeline using Docker Compose, without spending a dime on AWS:

```bash
cd my-awesome-project

# Spin up MinIO and execute the pipeline on the local Spark engine
kedroark test-local
```
*(This command automatically runs `docker-compose up -d`, triggers `kedro run --env local_infra`, and cleans up the containers afterward.)*

### Step 4: Run Tests

The generated project has an advanced pytest setup out-of-the-box. Run specific layers of the test pyramid:

```bash
# Fast logic tests
pytest -m unit

# Integration with I/O simulation
pytest -m integration

# End-to-End full session test
pytest -m e2e

# Performance / Benchmark tests
pytest -m performance
```

### Step 5: Deploy the Infrastructure (Terraform)

KedroArk separates your infrastructure based on best practices. When you're ready to deploy to AWS, navigate to the terraform folder:

```bash
cd terraform

# Initialize the modular terraform setup
terraform init

# Validate syntax
terraform validate

# Provision your AWS Glue / EMR environments, IAM Roles, and S3 Buckets
terraform plan
terraform apply
```
