import pytest
from kedro.runner import SequentialRunner
from kedro.io import DataCatalog
from {{cookiecutter.project_slug}}.pipelines.finance_example.pipeline import create_pipeline

@pytest.mark.integration
def test_finance_pipeline_integration(mock_finance_data):
    """Integration test to run the full pipeline locally with mock data."""
    # Setup catalog with memory datasets for integration testing
    catalog = DataCatalog()
    catalog.add("raw_financial_data", mock_finance_data)
    
    pipeline = create_pipeline()
    runner = SequentialRunner()
    
    # Run the pipeline
    result = runner.run(pipeline, catalog)
    
    assert "aggregated_financial_data" in result
    
    # Validate the result DataFrame
    agg_df = result["aggregated_financial_data"]
    assert agg_df.count() > 0
