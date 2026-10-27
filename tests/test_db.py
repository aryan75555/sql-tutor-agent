import pytest

from tutor.db import create_connection, get_schema, run_query, validate_query


@pytest.fixture
def conn():
    return create_connection()


def test_select_returns_rows(conn):
    result = run_query(conn, "SELECT name FROM employees")
    assert result["error"] is None
    assert len(result["rows"]) == 12
    assert result["columns"] == ["name"]


def test_trailing_semicolon_allowed(conn):
    assert run_query(conn, "SELECT 1;")["error"] is None


def test_with_clause_allowed(conn):
    result = run_query(conn, "WITH t AS (SELECT 1 AS x) SELECT x FROM t")
    assert result["error"] is None


@pytest.mark.parametrize(
    "sql",
    [
        "DELETE FROM employees",
        "DROP TABLE employees",
        "UPDATE employees SET salary = 0",
        "INSERT INTO departments VALUES (9, 'X', 'Y')",
        "SELECT 1; DROP TABLE employees",
        "PRAGMA table_info(employees)",
        "WITH t AS (SELECT 1) DELETE FROM employees",
    ],
)
def test_forbidden_queries_blocked(conn, sql):
    assert run_query(conn, sql)["error"] is not None
    assert len(run_query(conn, "SELECT * FROM employees")["rows"]) == 12


def test_empty_query(conn):
    assert validate_query("   ") == "The query is empty."


def test_syntax_error_reported(conn):
    result = run_query(conn, "SELEC name FROM employees")
    assert result["error"] is not None


def test_unknown_table_reported(conn):
    result = run_query(conn, "SELECT * FROM missing_table")
    assert "no such table" in result["error"]


def test_schema_contains_all_tables(conn):
    assert set(get_schema(conn)) == {"customers", "departments", "employees", "orders"}
