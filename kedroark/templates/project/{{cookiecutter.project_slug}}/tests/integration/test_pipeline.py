import pytest
from kedro.io import DataCatalog, MemoryDataset
from kedro.runner import SequentialRunner

from {{cookiecutter.project_slug}}.pipelines.finance_example.pipeline import create_pipeline


@pytest.mark.integration
def test_finance_pipeline_integration(mock_finance_data):
    """Integration test: run the full pipeline with in-memory datasets."""
    catalog = DataCatalog(
        datasets={
            "raw_financial_data": MemoryDataset(data=mock_finance_data),
            "cleaned_financial_data": MemoryDataset(),
            "aggregated_financial_data": MemoryDataset(),
        }
    )

    pipeline = create_pipeline()
    runner = SequentialRunner()

    runner.run(pipeline, catalog)

    agg_df = catalog.load("aggregated_financial_data")
    assert agg_df.count() > 0

    expected_cols = ["currency", "total_amount", "transaction_count"]
    for col in expected_cols:
        assert col in agg_df.columns
