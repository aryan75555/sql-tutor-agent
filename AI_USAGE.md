# AI Usage Note

## Tools used

- Claude (Anthropic) as the main AI assistant for planning, code generation, test writing and documentation.
- Claude or Gemini API inside the application itself to generate student hints.

## Where AI helped during development

- Choosing the use case and breaking the work into steps.
- Generating the first version of the modules: database safety layer, evaluator, agent loop, LLM client and Streamlit UI.
- Writing the pytest test cases and the sample database.
- Drafting the README and this documentation.

## Where AI is used in the product

- The tutor agent calls an LLM to turn the evaluator's diagnosis into a short hint at one of three levels.
- The reference solution is shared with the model for accuracy, and a code-based leakage check makes sure it is not repeated in the hint.
- If the model fails or keeps leaking, the app falls back to hand-written hints.

## What was done by me

- Read and understood each module so I can explain the design.
- Ran the full test suite and tried the app manually, including wrong attempts, hint levels and forbidden queries.
- Reviewed the safety rules and the limitations listed in the README.

## Decisions I made rather than the AI

- Keep the project at medium complexity with plain Python, Streamlit and SQLite.
- Use code, not the model, to decide the hint level and to check for leakage.
- Keep API keys in environment variables and out of the repository.

## Risks and how they are handled

- Hallucinated or wrong hints: the diagnosis comes from real query results, and hints stay conceptual.
- Answer leakage: n-gram leakage check, code block rejection, regeneration and fallback.
- Unsafe SQL: single statement only, SELECT only, forbidden keyword filter, read-only connection, timeout.
- Dependence on an external API: the app keeps working with built-in hints.
