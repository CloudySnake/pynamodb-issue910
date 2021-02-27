def test_read_from_table(preloaded_table):
    """
    A simple test just to validate we can read/write to the table
    """
    from src.subclassed_code import Stimulus

    table, rows = preloaded_table

    returned_row = Stimulus.get(hash_key="partition_key_1", range_key="sort_key_1")

    assert returned_row.stimulus_id == rows[0].stimulus_id
    assert returned_row.areas_of_interest == rows[0].areas_of_interest


def test_read_from_index(preloaded_table):
    from src.subclassed_code import Stimulus

    gs1_key = "gsi1_pk"

    result = []
    for stimulus in Stimulus.gs1.query(
        gs1_key, Stimulus.gs1_sk.startswith("STIMULUS#")
    ):
        result.append(stimulus.attribute_values)

    assert len(result) == 2

    assert result[0]["areas_of_interest"] == {"Wales": "Millenium Stadium"}
    assert result[1]["areas_of_interest"] == {"Scotland": "Murrayfield"}


def test_query_primary_key(preloaded_table):
    from src.subclassed_code import Stimulus

    result = []
    for stimulus in Stimulus.query(
        "partition_key_2", Stimulus.sk.startswith("sort_key")
    ):
        result.append(stimulus.attribute_values)

    assert len(result) == 1
