import pandas as pd
import streamlit as st

from tutor.agent import review_attempt
from tutor.db import create_connection, get_schema, run_query
from tutor.evaluator import evaluate
from tutor.problems import PROBLEMS, get_problem

st.set_page_config(page_title="SQL Tutor Agent", layout="wide")


@st.cache_resource
def get_connection():
    return create_connection()


def get_state(problem_id):
    store = st.session_state.setdefault("progress", {})
    if problem_id not in store:
        store[problem_id] = {"wrong": 0, "solved": False, "history": [], "hints": [], "last": None}
    return store[problem_id]


def go_to(problem_id):
    st.session_state["problem_choice"] = problem_id


def submit(conn, problem, sql, state):
    result = run_query(conn, sql)
    expected = run_query(conn, problem["solution"])
    evaluation = evaluate(result, expected, problem["ordered"])
    state["history"].append({"sql": sql, "kind": evaluation["kind"]})
    hint = None
    if evaluation["correct"]:
        state["solved"] = True
    else:
        state["wrong"] += 1
        previous = [item["hint"] for item in state["hints"]]
        hint = review_attempt(problem, sql, evaluation, state["wrong"], previous)
        state["hints"].append(hint)
    state["last"] = {"result": result, "evaluation": evaluation, "hint": hint}


def render_sidebar(conn):
    st.sidebar.title("SQL Tutor Agent")
    progress = st.session_state.get("progress", {})
    solved = sum(1 for item in progress.values() if item["solved"])
    st.sidebar.metric("Solved", f"{solved} / {len(PROBLEMS)}")
    ids = [problem["id"] for problem in PROBLEMS]
    st.sidebar.selectbox(
        "Problem",
        ids,
        key="problem_choice",
        format_func=lambda pid: f"{pid}. {get_problem(pid)['title']} ({get_problem(pid)['difficulty']})",
    )
    st.sidebar.subheader("Database schema")
    for table, columns in get_schema(conn).items():
        with st.sidebar.expander(table):
            for name, column_type in columns:
                st.write(f"{name} ({column_type})")
    if st.sidebar.button("Reset progress"):
        st.session_state.pop("progress", None)
        st.rerun()


def render_feedback(state):
    last = state["last"]
    if last is None:
        return
    result = last["result"]
    evaluation = last["evaluation"]
    if result["rows"] or result["columns"]:
        st.subheader("Your result")
        st.dataframe(pd.DataFrame(result["rows"], columns=result["columns"]))
    if evaluation["correct"]:
        st.success("Correct! Your result matches the expected output.")
        return
    st.error(evaluation["message"])
    hint = last["hint"]
    if hint:
        label = "AI hint" if hint["source"] == "llm" else "Built-in hint"
        st.info(f"{label} (level {hint['level']}): {hint['hint']}")


def main():
    conn = get_connection()
    st.session_state.setdefault("problem_choice", PROBLEMS[0]["id"])
    render_sidebar(conn)

    problem = get_problem(st.session_state["problem_choice"])
    state = get_state(problem["id"])

    st.title(f"{problem['id']}. {problem['title']}")
    st.caption(f"{problem['difficulty']} | {problem['topic']}")
    st.write(problem["description"])
    if problem["ordered"]:
        st.write("Row order matters for this problem.")

    sql = st.text_area("Your SQL query", key=f"sql_{problem['id']}", height=150)
    if st.button("Run query", type="primary"):
        with st.spinner("Checking your query..."):
            submit(conn, problem, sql, state)
        st.rerun()

    render_feedback(state)

    if state["solved"]:
        next_ids = [item["id"] for item in PROBLEMS if item["id"] > problem["id"]]
        if next_ids:
            st.button("Next problem", on_click=go_to, args=(next_ids[0],))

    if state["history"]:
        with st.expander(f"Attempt history ({len(state['history'])})"):
            for number, item in enumerate(state["history"], start=1):
                st.code(item["sql"], language="sql")
                st.caption(f"Attempt {number}: {item['kind']}")


main()
