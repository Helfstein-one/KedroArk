"""Project pipelines."""

from typing import Dict

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

from test_glue_project.pipelines.finance_example.pipeline import create_pipeline as finance_pipeline


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()

    pipelines["finance"] = finance_pipeline()
    pipelines["__default__"] = pipelines["finance"]

    return pipelines
