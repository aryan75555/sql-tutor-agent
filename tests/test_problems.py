import pytest

from tutor.agent import leaks_solution
from tutor.db import create_connection, run_query
from tutor.evaluator import evaluate
from tutor.problems import PROBLEMS


@pytest.fixture(scope="module")
def conn():
    return create_connection()


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: f"problem_{p['id']}")
def test_solution_passes_its_own_evaluation(conn, problem):
    result = run_query(conn, problem["solution"])
    expected = run_query(conn, problem["solution"])
    assert result["error"] is None
    assert result["rows"]
    assert evaluate(result, expected, problem["ordered"])["correct"]


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: f"problem_{p['id']}")
def test_builtin_hints_do_not_leak_solution(problem):
    assert len(problem["hints"]) == 3
    for hint in problem["hints"]:
        assert not leaks_solution(hint, problem["solution"])


def test_problem_ids_are_unique():
    ids = [problem["id"] for problem in PROBLEMS]
    assert len(ids) == len(set(ids))
