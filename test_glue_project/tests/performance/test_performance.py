import pytest

from test_glue_project.pipelines.finance_example.nodes import clean_financial_data


@pytest.mark.performance
def test_performance_clean_data(benchmark, mock_finance_data):
    """Benchmark the clean data node."""

    # We benchmark the Spark query plan execution by calling .collect()
    def run_job():
        clean_financial_data(mock_finance_data).collect()

    benchmark(run_job)
