from tutor.agent import hint_level, leaks_solution, review_attempt
from tutor.llm import LLMError
from tutor.problems import get_problem

PROBLEM = get_problem(4)
EVALUATION = {"correct": False, "kind": "wrong_row_count", "message": "Your query returns 5 row(s) but 12 are expected."}


def test_hint_level_progression():
    assert [hint_level(n) for n in (1, 2, 3, 4, 9)] == [1, 2, 3, 3, 3]


def test_leak_detected_for_full_solution():
    assert leaks_solution(PROBLEM["solution"], PROBLEM["solution"])


def test_leak_detected_for_lowercase_and_extra_spaces():
    text = "try   " + PROBLEM["solution"].lower().replace(" ", "  ")
    assert leaks_solution(text, PROBLEM["solution"])


def test_leak_detected_for_code_block():
    assert leaks_solution("Use this:\n```sql\nSELECT 1\n```", PROBLEM["solution"])


def test_plain_english_hint_is_safe():
    assert not leaks_solution("Think about which column links the two tables.", PROBLEM["solution"])


def test_clean_llm_hint_is_used():
    def llm(system, user):
        return "Think about which column links employees to departments."

    outcome = review_attempt(PROBLEM, "SELECT name FROM employees", EVALUATION, 1, [], llm=llm)
    assert outcome["source"] == "llm"
    assert outcome["regenerations"] == 0
    assert outcome["level"] == 1


def test_leaky_hint_is_regenerated():
    replies = [PROBLEM["solution"], "Match the department id in employees to the id in departments."]

    def llm(system, user):
        return replies.pop(0)

    outcome = review_attempt(PROBLEM, "SELECT name FROM employees", EVALUATION, 2, [], llm=llm)
    assert outcome["source"] == "llm"
    assert outcome["regenerations"] == 1
    assert not leaks_solution(outcome["hint"], PROBLEM["solution"])


def test_always_leaky_llm_falls_back():
    def llm(system, user):
        return PROBLEM["solution"]

    outcome = review_attempt(PROBLEM, "SELECT name FROM employees", EVALUATION, 3, [], llm=llm)
    assert outcome["source"] == "fallback"
    assert outcome["hint"] == PROBLEM["hints"][2]


def test_llm_failure_falls_back():
    def llm(system, user):
        raise LLMError("no key")

    outcome = review_attempt(PROBLEM, "SELECT name FROM employees", EVALUATION, 1, [], llm=llm)
    assert outcome["source"] == "fallback"
    assert outcome["hint"] == PROBLEM["hints"][0]


def test_prompt_contains_problem_and_student_query():
    captured = {}

    def llm(system, user):
        captured["system"] = system
        captured["user"] = user
        return "Look at the relationship between the tables."

    review_attempt(PROBLEM, "SELECT name FROM employees", EVALUATION, 2, ["earlier hint"], llm=llm)
    assert "SELECT name FROM employees" in captured["user"]
    assert PROBLEM["description"] in captured["user"]
    assert "earlier hint" in captured["user"]
    assert "Level 2" in captured["user"]
    assert "Never reveal" in captured["system"]
