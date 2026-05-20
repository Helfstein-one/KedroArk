"""
This is a simple runner script for AWS Glue to bootstrap a Kedro project.
"""

import sys
from pathlib import Path

from awsglue.context import GlueContext
from awsglue.job import Job
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pyspark.context import SparkContext


def main():
    # Initialize Glue Context
    sc = SparkContext.getOrCreate()
    glueContext = GlueContext(sc)
    job = Job(glueContext)

    # Optional: Get arguments
    from awsglue.utils import getResolvedOptions

    args = getResolvedOptions(sys.argv, ["JOB_NAME"])
    job.init(args["JOB_NAME"], args)

    # Initialize Kedro
    project_path = Path(__file__).resolve().parent.parent
    bootstrap_project(project_path)

    with KedroSession.create(project_path=project_path) as session:
        session.run()

    job.commit()


if __name__ == "__main__":
    main()
