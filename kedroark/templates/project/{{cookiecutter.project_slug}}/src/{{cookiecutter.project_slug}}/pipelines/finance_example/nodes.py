import pyspark.sql.functions as F
from pyspark.sql import DataFrame


def clean_financial_data(df: DataFrame) -> DataFrame:
    """Clean financial transactions data."""
    return df.filter((F.col("amount") > 0) & (F.col("status") == "COMPLETED")).dropna(
        subset=["transaction_id", "amount"]
    )


def aggregate_by_currency(df: DataFrame) -> DataFrame:
    """Create aggregate metrics by currency."""
    return df.groupBy("currency").agg(
        F.sum("amount").alias("total_amount"),
        F.count("transaction_id").alias("transaction_count"),
    )
