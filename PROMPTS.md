# Prompt Documentation

## 1. Prompts used during development (AI-assisted)

These were given to an AI assistant (Claude) while planning and building the project.

1. Choosing the use case
   "I received an assignment mail from Infinite Computer Solutions with three use cases (SQL Tutor Agent, API Contract Differ, Mock-Data Generator). I want to build the SQL one. Explain the plan, stack and timeline for one day."

2. Building the project
   "Build the SQL Tutor Agent exactly as per the mail requirements: interactive web app, runs the user's SQL on a sample database, compares with expected output, LLM gives hints without revealing the answer, agent loop, tests, README, prompt documentation, AI usage note. Keep it medium level so I can study and explain it. No comments in the code and no env file in the repository."

3. Design decisions asked during development
   - "Which agent loop fits this problem?" -> evaluate, diagnose, hint, retry, with a second loop that regenerates a hint if it leaks the answer.
   - "How do I compare query results fairly?" -> compare column count and normalized values, ignore row order unless the problem needs ORDER BY.
   - "How do I make SQL execution safe?" -> allow only one SELECT or WITH statement, block write keywords, read-only connection, timeout.
   - "Write pytest cases for the evaluator, the safety filter and the leakage check."

## 2. Prompts used at runtime (inside the app)

Defined in `tutor/agent.py`.

### System prompt

```
You are a patient SQL tutor for beginners. A student is solving a SQL problem on a SQLite database.
You will receive the problem, the student's query, a diagnosis of what is wrong, and a hint level.
You also receive a reference solution so that your hint is accurate.
Never reveal the reference solution, never write a complete query, and never put SQL code in code blocks.
Keep the hint under 60 words, friendly and specific to the student's mistake.
Do not repeat earlier hints.
```

### User prompt template

```
Problem: <problem description>
Topic: <topic>
Student's query:
<student SQL>
Diagnosis: <message from the evaluator>
Reference solution (secret, do not reveal): <solution>
Earlier hints already given:
<list of earlier hints or "none">
<level instruction>
```

### Level instructions

- Level 1: gentle, conceptual nudge. Name the SQL concept but not the exact clause or column.
- Level 2: more specific. Mention the relevant clause, table or column and what is wrong in the student's query.
- Level 3: very specific. Describe the structure of the answer step by step in plain English, but do not write the query.

### Regeneration prompt (added when the leakage check fails)

```
Your previous reply revealed too much of the solution. Rewrite it in plain English with no SQL code and no full query.
```

## 3. Why the prompts are designed this way

- The reference solution is given to the model so hints are accurate, and the leakage check protects the answer.
- The diagnosis comes from the evaluator, so the model reacts to the real mistake (wrong columns, wrong row count, SQL error) instead of guessing.
- Earlier hints are included so the model does not repeat itself.
- Hint level is controlled by code, not by the model, so the progression is predictable and testable.
