"""Project pipelines."""
from typing import Dict

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

{% if cookiecutter.include_finance_example == 'yes' %}
from {{ cookiecutter.project_slug }}.pipelines.finance_example.pipeline import create_pipeline as finance_pipeline
{% endif %}

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    {% if cookiecutter.include_finance_example == 'yes' %}
    pipelines["finance"] = finance_pipeline()
    pipelines["__default__"] = pipelines["finance"]
    {% else %}
    pipelines["__default__"] = Pipeline([])
    {% endif %}
    
    return pipelines
