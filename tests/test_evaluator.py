from tutor.evaluator import evaluate


def make(columns, rows, error=None):
    return {"columns": columns, "rows": rows, "error": error}


EXPECTED = make(["name", "salary"], [("A", 10), ("B", 20)])


def test_correct_unordered_ignores_row_order():
    result = make(["n", "s"], [("B", 20), ("A", 10)])
    assert evaluate(result, EXPECTED, ordered=False)["correct"]


def test_column_aliases_do_not_matter():
    result = make(["x", "y"], [("A", 10), ("B", 20)])
    assert evaluate(result, EXPECTED, ordered=False)["correct"]


def test_wrong_column_count():
    result = make(["name"], [("A",), ("B",)])
    assert evaluate(result, EXPECTED, ordered=False)["kind"] == "wrong_columns"


def test_extra_rows():
    result = make(["name", "salary"], [("A", 10), ("B", 20), ("C", 30)])
    assert evaluate(result, EXPECTED, ordered=False)["kind"] == "wrong_row_count"


def test_missing_rows():
    result = make(["name", "salary"], [("A", 10)])
    assert evaluate(result, EXPECTED, ordered=False)["kind"] == "wrong_row_count"


def test_wrong_values():
    result = make(["name", "salary"], [("A", 10), ("B", 99)])
    assert evaluate(result, EXPECTED, ordered=False)["kind"] == "wrong_values"


def test_ordered_wrong_order():
    result = make(["name", "salary"], [("B", 20), ("A", 10)])
    assert evaluate(result, EXPECTED, ordered=True)["kind"] == "wrong_order"


def test_ordered_correct():
    result = make(["name", "salary"], [("A", 10), ("B", 20)])
    assert evaluate(result, EXPECTED, ordered=True)["correct"]


def test_error_result():
    result = make([], [], error="no such table: x")
    evaluation = evaluate(result, EXPECTED, ordered=False)
    assert evaluation["kind"] == "error"
    assert "no such table" in evaluation["message"]


def test_float_rounding():
    expected = make(["avg"], [(61333.333333,)])
    result = make(["avg"], [(61333.33,)])
    assert evaluate(result, expected, ordered=False)["correct"]


def test_int_and_float_equal():
    expected = make(["n"], [(5,)])
    result = make(["n"], [(5.0,)])
    assert evaluate(result, expected, ordered=False)["correct"]
