# Reflection
> The handout text I had did not include the four questions, so these answers cover the usual four themes. Adjust headings to match your handout's wording.

**1. Which issues were easiest/hardest to fix, and why?**
Style problems (naming, line length, docstrings) were mechanical. The hardest was the mutable default argument: the fix is small, but understanding why `extras={}` is shared across calls took thought, and changing it alters behaviour for callers that relied on the shared dict.

**2. Did the tools report false positives, or miss real problems?**
Bandit's B101 (`assert`) is low severity and arguably noise in a demo, but the fix is cheap. None of the tools flagged that `rarest()` crashes on an empty table; I found it by reading the code. Static analysis supplements, but does not replace, review and tests.

**3. How would you integrate static analysis into a workflow?**
Run Flake8 and Pylint as pre-commit hooks, and run Bandit plus a minimum Pylint score (e.g. 9.5) in CI so merges fail on regressions. Triage by severity: security (High/Medium) first, then bugs, then style.

**4. What did you learn about code quality and security?**
String-built SQL and weak hashes are easy to write and easy to detect automatically. Small habits (parameterised queries, `None` defaults, small documented functions, no work at import time) remove whole classes of bugs and make code easier to maintain.
