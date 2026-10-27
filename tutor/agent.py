import re

from tutor.llm import LLMError, call_llm

MAX_REGENERATIONS = 2
NGRAM_SIZE = 6

SYSTEM_PROMPT = (
    "You are a patient SQL tutor for beginners. A student is solving a SQL problem on a SQLite database. "
    "You will receive the problem, the student's query, a diagnosis of what is wrong, and a hint level. "
    "You also receive a reference solution so that your hint is accurate. "
    "Never reveal the reference solution, never write a complete query, and never put SQL code in code blocks. "
    "Keep the hint under 60 words, friendly and specific to the student's mistake. "
    "Do not repeat earlier hints."
)

LEVEL_INSTRUCTIONS = {
    1: "Level 1: give a gentle, conceptual nudge. Name the SQL concept involved but not the exact clause or column.",
    2: "Level 2: be more specific. Mention the relevant clause, table or column, and point at what is wrong in the student's query.",
    3: "Level 3: be very specific. Describe the structure of the answer step by step in plain English, but do not write the query.",
}


def hint_level(wrong_attempts):
    return min(max(wrong_attempts, 1), 3)


def tokenize(text):
    return re.findall(r"[a-z0-9_*.]+|[(),=<>]", text.lower())


def leaks_solution(hint, solution):
    if "```" in hint:
        return True
    solution_tokens = tokenize(solution)
    hint_tokens = tokenize(hint)
    size = min(NGRAM_SIZE, len(solution_tokens))
    solution_ngrams = {
        tuple(solution_tokens[i : i + size]) for i in range(len(solution_tokens) - size + 1)
    }
    for i in range(len(hint_tokens) - size + 1):
        if tuple(hint_tokens[i : i + size]) in solution_ngrams:
            return True
    return False


def build_user_prompt(problem, user_sql, evaluation, level, previous_hints):
    previous = "\n".join(f"- {hint}" for hint in previous_hints) or "none"
    return (
        f"Problem: {problem['description']}\n"
        f"Topic: {problem['topic']}\n"
        f"Student's query:\n{user_sql}\n"
        f"Diagnosis: {evaluation['message']}\n"
        f"Reference solution (secret, do not reveal): {problem['solution']}\n"
        f"Earlier hints already given:\n{previous}\n"
        f"{LEVEL_INSTRUCTIONS[level]}"
    )


def fallback_hint(problem, level):
    return problem["hints"][level - 1]


def review_attempt(problem, user_sql, evaluation, wrong_attempts, previous_hints, llm=call_llm):
    level = hint_level(wrong_attempts)
    prompt = build_user_prompt(problem, user_sql, evaluation, level, previous_hints)
    attempt = 0
    for attempt in range(MAX_REGENERATIONS + 1):
        try:
            text = llm(SYSTEM_PROMPT, prompt).strip()
        except LLMError:
            break
        if text and not leaks_solution(text, problem["solution"]):
            return {"hint": text, "level": level, "source": "llm", "regenerations": attempt}
        prompt += (
            "\n\nYour previous reply revealed too much of the solution. "
            "Rewrite it in plain English with no SQL code and no full query."
        )
    return {
        "hint": fallback_hint(problem, level),
        "level": level,
        "source": "fallback",
        "regenerations": attempt,
    }
