import os

from pynamodb.models import Model, GlobalSecondaryIndex
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    JSONAttribute,
    BooleanAttribute,
    UTCDateTimeAttribute,
    ListAttribute,
)
from pynamodb.indexes import AllProjection


class MainTableMeta:
    table_name = "test-db-local"
    region = os.environ["AWS_DEFAULT_REGION"]
    # host = "http://{}:{}".format(
    #     os.environ["SLS_OFF_HOST"], os.environ["DYNAMODB_PORT"]
    # )


class GlobalIndex1(GlobalSecondaryIndex):
    """
    This class represents the global secondary index
    """

    class Meta:
        index_name = "GS1-Index-local"
        region = os.environ["AWS_DEFAULT_REGION"]
        read_capacity_units = 2
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    gs1_pk = UnicodeAttribute(hash_key=True, attr_name="GS1PK")
    gs1_sk = UnicodeAttribute(range_key=True, attr_name="GS1SK")


class GlobalIndex2(GlobalSecondaryIndex):
    """
    This class represents the global secondary index
    """

    class Meta:
        index_name = "GS1-Index-local"
        region = os.environ["AWS_DEFAULT_REGION"]
        read_capacity_units = 2
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    gs1_pk = UnicodeAttribute(hash_key=True, attr_name="GS1PK")
    gs1_sk = UnicodeAttribute(range_key=True, attr_name="GS1SK")


class Stimulus(Model):
    """
    DynamoDb model for the Stimulus
    """

    Meta = MainTableMeta

    pk = UnicodeAttribute(hash_key=True, attr_name="PK")
    sk = UnicodeAttribute(range_key=True, attr_name="SK")

    gs1 = GlobalIndex1()
    # gs1 = GlobalIndex2()
    gs1_pk = UnicodeAttribute(attr_name="GS1PK")
    gs1_sk = UnicodeAttribute(attr_name="GS1SK")

    stimulus_id = UnicodeAttribute(attr_name="StimulusId")
    index = NumberAttribute(attr_name="Index")
    stimulus_type = UnicodeAttribute(attr_name="StimulusType")
    areas_of_interest = JSONAttribute(attr_name="AreasOfInterest", null=True)
    duration = NumberAttribute(attr_name="Duration")
    open_end_question = BooleanAttribute(attr_name="OpenEndQuestion", null=True)
    questions = JSONAttribute(attr_name="Questions", null=True)
    url = UnicodeAttribute(attr_name="Url")
    date_created = UTCDateTimeAttribute(attr_name="DateCreated")


class Result(Model):
    """
    DynamoDb model for the Result
    """

    Meta = MainTableMeta

    pk = UnicodeAttribute(hash_key=True, attr_name="PK")
    sk = UnicodeAttribute(range_key=True, attr_name="SK")

    gs1 = GlobalIndex1()
    gs1_pk = UnicodeAttribute(attr_name="GS1PK")
    gs1_sk = UnicodeAttribute(attr_name="GS1SK")

    result_id = UnicodeAttribute(attr_name="ResultId")
    stimulus_id = UnicodeAttribute(attr_name="StimulusId")
    respondent_age = UnicodeAttribute(attr_name="RespondentAge")
    respondent_area = UnicodeAttribute(attr_name="RespondentArea")
    respondent_gender = UnicodeAttribute(attr_name="RespondentGender")
    emotions_imgs = ListAttribute(attr_name="EmotionsImgs")
    heatmap_imgs = ListAttribute(attr_name="HeatmapImgs")


# result = []
# for stimulus in Stimulus.gs1.query(gs1_key, Stimulus.gs1_sk.startswith("STIMULUS#")):
#     result.append(stimulus.attribute_values)
