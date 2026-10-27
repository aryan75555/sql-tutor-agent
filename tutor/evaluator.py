def normalize_value(value):
    if isinstance(value, float):
        rounded = round(value, 2)
        return int(rounded) if rounded == int(rounded) else rounded
    if isinstance(value, str):
        return value.strip()
    return value


def normalize_rows(rows):
    return [tuple(normalize_value(value) for value in row) for row in rows]


def sort_key(row):
    return tuple(str(value) for value in row)


def evaluate(result, expected, ordered):
    if result["error"]:
        return {"correct": False, "kind": "error", "message": f"SQL error: {result['error']}"}

    user_cols = len(result["columns"])
    expected_cols = len(expected["columns"])
    if user_cols != expected_cols:
        return {
            "correct": False,
            "kind": "wrong_columns",
            "message": f"Your query returns {user_cols} column(s) but {expected_cols} are expected.",
        }

    user_rows = normalize_rows(result["rows"])
    expected_rows = normalize_rows(expected["rows"])
    if len(user_rows) != len(expected_rows):
        return {
            "correct": False,
            "kind": "wrong_row_count",
            "message": f"Your query returns {len(user_rows)} row(s) but {len(expected_rows)} are expected.",
        }

    same_set = sorted(user_rows, key=sort_key) == sorted(expected_rows, key=sort_key)
    if ordered:
        if user_rows == expected_rows:
            return {"correct": True, "kind": "correct", "message": "Correct."}
        if same_set:
            return {
                "correct": False,
                "kind": "wrong_order",
                "message": "The rows are right but they are in the wrong order.",
            }
    elif same_set:
        return {"correct": True, "kind": "correct", "message": "Correct."}
    return {
        "correct": False,
        "kind": "wrong_values",
        "message": "The returned values do not match the expected result.",
    }
