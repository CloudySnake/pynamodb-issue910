import os

from datetime import datetime

import boto3
from freezegun import freeze_time
from moto import mock_dynamodb2
import pytest


@pytest.fixture()
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"


@pytest.fixture()
def mock_dynamo_table(aws_credentials):
    with mock_dynamodb2():
        # AND A MOCKED DYNAMODB TABLE
        table_name = "test-db-local"
        dynamodb = boto3.resource("dynamodb", "eu-west-1")

        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "GS1-Index-local",
                    "KeySchema": [
                        {"AttributeName": "GS1PK", "KeyType": "HASH"},
                        {"AttributeName": "GS1SK", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                },
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
                {"AttributeName": "GS1PK", "AttributeType": "S"},
                {"AttributeName": "GS1SK", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )

        yield table

        table.delete()


@freeze_time("2012-01-01")
@pytest.fixture()
def preloaded_table(mock_dynamo_table):
    # Importing here so the mocking completes before importing (to set default region)
    from src.subclassed_code import Stimulus, Result

    # Row 1
    row1 = Stimulus(
        pk="partition_key_1",
        sk="sort_key_1",
        gs1_pk="gsi1_pk",
        gs1_sk="STIMULUS#row1",
        stimulus_id="stim_id",
        index=1,
        stimulus_type="test",
        areas_of_interest={"Wales": "Millenium Stadium"},
        duration=100,
        open_end_question=True,
        url="https://test_url.co.uk",
        date_created=datetime.now(),
    )
    row1.save()

    # Row 2
    row2 = Stimulus(
        pk="partition_key_2",
        sk="sort_key_2",
        gs1_pk="gsi1_pk",
        gs1_sk="STIMULUS#row2",
        stimulus_id="stim_id2",
        index=2,
        stimulus_type="testing",
        areas_of_interest={"Scotland": "Murrayfield"},
        duration=200,
        open_end_question=False,
        url="https://test_url.co.uk",
        date_created=datetime.now(),
    )
    row2.save()

    # Result Row
    # Row 2
    row3 = Result(
        pk="partition_key_3",
        sk="sort_key_3",
        gs1_pk="gsi1_pk",
        gs1_sk="RESULT#row3",
        result_id="result",
        stimulus_id="stim_id3",
        respondent_age="Forty years",
        respondent_area="Cardiff",
        respondent_gender="Male",
        emotions_imgs=["a", "list"],
        heatmap_imgs=["another", "list"],
    )
    row3.save()

    rows = [row1, row2, row3]

    yield mock_dynamo_table, rows
