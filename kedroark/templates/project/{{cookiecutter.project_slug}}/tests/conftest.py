import pytest
from pyspark.sql import SparkSession
from faker import Faker
import pandas as pd

@pytest.fixture(scope="session")
def spark():
    """Create a local SparkSession for testing."""
    spark_session = (
        SparkSession.builder.master("local[2]")
        .appName("KedroArkLocalTesting")
        # Iceberg configurations for local testing
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.local.type", "hadoop")
        .config("spark.sql.catalog.local.warehouse", "/tmp/iceberg_warehouse")
        .getOrCreate()
    )
    yield spark_session
    spark_session.stop()

@pytest.fixture
def mock_finance_data(spark):
    """Generate fake financial data using Faker."""
    fake = Faker()
    Faker.seed(42)
    data = []
    for _ in range(100):
        data.append({
            "transaction_id": fake.uuid4(),
            "customer_id": fake.uuid4(),
            "amount": float(fake.pydecimal(left_digits=4, right_digits=2, positive=True)),
            "transaction_date": fake.date_time_this_year().isoformat(),
            "currency": fake.currency_code(),
            "status": fake.random_element(elements=("COMPLETED", "PENDING", "FAILED"))
        })
    
    pdf = pd.DataFrame(data)
    return spark.createDataFrame(pdf)
