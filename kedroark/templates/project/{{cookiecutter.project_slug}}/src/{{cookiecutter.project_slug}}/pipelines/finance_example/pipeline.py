from kedro.pipeline import Pipeline, node, pipeline
from .nodes import clean_financial_data, aggregate_by_currency

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=clean_financial_data,
            inputs="raw_financial_data",
            outputs="cleaned_financial_data",
            name="clean_financial_data_node",
        ),
        node(
            func=aggregate_by_currency,
            inputs="cleaned_financial_data",
            outputs="aggregated_financial_data",
            name="aggregate_by_currency_node",
        )
    ])
