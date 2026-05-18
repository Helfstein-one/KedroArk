import pytest

from {{cookiecutter.project_slug}}.pipelines.finance_example.nodes import (
    aggregate_by_currency,
    clean_financial_data,
)


@pytest.mark.unit
def test_clean_financial_data(mock_finance_data):
    """Test the cleaning node logic."""
    cleaned_df = clean_financial_data(mock_finance_data)

    # Assert no missing amounts
    assert cleaned_df.filter(cleaned_df.amount.isNull()).count() == 0

    # Assert correct statuses
    assert cleaned_df.filter(cleaned_df.status != "COMPLETED").count() == 0


@pytest.mark.unit
def test_aggregate_by_currency(mock_finance_data):
    """Test aggregation logic."""
    cleaned_df = clean_financial_data(mock_finance_data)
    agg_df = aggregate_by_currency(cleaned_df)

    # Check that columns are properly aggregated
    expected_cols = ["currency", "total_amount", "transaction_count"]
    for col in expected_cols:
        assert col in agg_df.columns
