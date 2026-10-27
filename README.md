# SQL Tutor Agent

An interactive web app that teaches SQL. It shows a problem, runs the student's query on a sample SQLite database, compares the result with the expected output, and uses an LLM to give progressive hints without revealing the answer.

## Features

- 10 problems (3 easy, 4 medium, 3 hard) covering WHERE, ORDER BY, LIMIT, JOIN, LEFT JOIN, GROUP BY, HAVING, subqueries and self join
- Sample database with 4 tables: departments, employees, customers, orders
- Safe execution: only a single SELECT (or WITH ... SELECT) is allowed, the database is read-only and queries time out after 2 seconds
- Result comparison that ignores row order unless the problem asks for ordering, ignores column aliases, and rounds decimals
- LLM tutor with 3 hint levels that get more specific after every wrong attempt
- Leakage check that rejects hints containing the solution and asks the LLM to rewrite them
- Built-in hints as a fallback when the LLM is unavailable, so the app always works
- Attempt history, score and schema viewer

## Architecture

```
Student query
     |
     v
db.run_query  (validate -> read-only SQLite -> timeout)
     |
     v
evaluator.evaluate  (student result vs expected result)
     |
     +-- correct --> mark solved, show "Next problem"
     |
     +-- wrong --> agent.review_attempt
                      |
                      |  1. pick hint level (1, 2 or 3) from number of wrong attempts
                      |  2. build prompt: problem + student query + diagnosis + earlier hints
                      |  3. call LLM (llm.py)
                      |  4. leakage check on the reply
                      |        leak found  -> ask LLM to rewrite (max 2 times)
                      |        still leaks or LLM fails -> built-in hint from problems.py
                      v
                  hint shown -> student retries -> loop
```

The agent loop is: evaluate, diagnose, hint, retry. The second loop inside it is generate, check for leakage, regenerate.

External service integration: the Anthropic Claude API or the Google Gemini API, called over HTTPS in `tutor/llm.py`.

## Project structure

```
app.py                 Streamlit UI
tutor/db.py            Database setup, query validation, safe execution, schema
tutor/problems.py      Problems, reference solutions, built-in hints
tutor/evaluator.py     Result comparison
tutor/agent.py         Hint levels, prompts, leakage check, agent loop
tutor/llm.py           Claude and Gemini API calls
data/seed.sql          Sample data
tests/                 pytest test cases
PROMPTS.md             Key prompts
AI_USAGE.md            AI usage note
```

## Setup

Requires Python 3.10 or newer.

```
git clone <your-repo-url>
cd sql-tutor-agent
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows cmd: `.venv\Scripts\activate.bat`
- macOS / Linux: `source .venv/bin/activate`

Install dependencies:

```
pip install -r requirements.txt
```

## Configure the LLM

The app reads settings from environment variables. No file with secrets is stored in the repository.

Using Gemini (free tier available, default):

- Windows PowerShell: `$env:GEMINI_API_KEY = "your-key"`
- macOS / Linux: `export GEMINI_API_KEY="your-key"`

Using Claude:

- Windows PowerShell: `$env:LLM_PROVIDER = "claude"; $env:ANTHROPIC_API_KEY = "your-key"`
- macOS / Linux: `export LLM_PROVIDER=claude ANTHROPIC_API_KEY="your-key"`

Optional: set `LLM_MODEL` to use a different model name.

If no key is set, the app still works and shows the built-in hints.

## Run

```
streamlit run app.py
```

Open http://localhost:8501 in the browser.

## Run the tests

```
python -m pytest -v
```

The tests do not call any real API. The LLM is replaced by a stub function.

## Test coverage

- Database: valid queries, forbidden statements (DELETE, DROP, UPDATE, INSERT, PRAGMA, multiple statements), syntax errors, unknown tables
- Evaluator: correct result, different row order, column aliases, wrong columns, extra and missing rows, wrong values, wrong order, SQL error, float rounding
- Problems: every reference solution runs and passes, built-in hints do not leak the solution
- Agent: hint level progression, leakage detection, regeneration after a leak, fallback after repeated leaks, fallback on LLM failure, prompt contents

## Assumptions and limitations

- Results are compared by values and column count. Column names and aliases are not compared.
- Row order is only checked for problems that explicitly ask for sorting.
- The keyword filter blocks words like UPDATE or DELETE even inside text values, which is acceptable for a learning tool.
- The leakage check looks for 6 consecutive matching tokens from the reference solution. It can miss a hint that describes the solution in very different words, and it cannot judge whether a hint is pedagogically good.
- The LLM receives the reference solution so its hints are accurate. The leakage check is the guard that stops it from being repeated.
- Progress is kept in the browser session only and is lost on refresh.
- The sample database is small and in memory. It is recreated every time the app starts.
- Only SQLite syntax is supported.
