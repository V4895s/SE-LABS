# Issues Found (wildlife_sightings.py)

> Line numbers refer to the ORIGINAL file. Tool codes are what Bandit/Pylint/Flake8
> report for these patterns - confirm each against your own `*_before.txt` reports.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (Bandit B608, Medium) | Security | 9 | `str.format()` puts `species`/`zone` straight into the INSERT statement, so input like `x'); DROP TABLE sightings;--` alters the query. | Use a parameterised query: `VALUES (?, ?, ?)` with a tuple of values. |
| Weak hash MD5 (Bandit B324, High) | Security | 15 | `hashlib.md5` is cryptographically broken and flagged for any identifier use. | Switch to `hashlib.sha256`. |
| `assert` used for a check (Bandit B101, Low) | Security / Bug | 36 | Asserts are stripped under `python -O`, so the check silently disappears. | Replace with `if ...: raise ValueError(...)`. |
| Mutable default argument (Pylint W0102) | Bug | 8 | `extras={}` is created once and shared by every call that omits it, so totals leak between unrelated calls. | Default to `None`; create a new dict inside the function. |
| Redefined outer name (Pylint W0621) / global connection (C0103) | Design | 4, 8, 18, 26 | Module-level `conn` is shadowed by every function parameter, and the DB is opened on import. | Create the connection in `create_connection()` and call it from `main()`; close it afterwards. |
| Naming convention (Pylint C0103) | Style | 8, 14, 18 | `logSighting`, `observerId`, `zoneSummary` are camelCase. | Rename to `log_sighting`, `observer_id`, `zone_summary`. |
| Missing docstrings (Pylint C0114 / C0116) | Documentation | 1, 8-32 | Module and all functions lack docstrings. | Add concise docstrings. |
| Unnecessary `else` after `return` (Pylint R1705) | Refactor | 20-23 | `if/else` both return. | Simplify to `return row[0] or 0`. |
| Crash on empty table (logic bug, not tool-reported) | Bug | 28 | `min()` of an empty list raises `ValueError` when no sightings exist. | Return `None` when `rows` is empty. |
| Ambiguous variable `l` (Flake8 E741, Pylint C0103) and missing spaces (E225) | Style | 28 | `l=min(...)` - `l` looks like `1`/`I`, no spaces around `=`. | Return `min(...)[0]` directly. |
| Line too long (Flake8 E501, Pylint C0301) | Style | 5, 9, 19, 27 | Lines exceed 79 characters. | Wrap SQL strings and call arguments across lines. |
| Top-level `main()` call | Design | 40 | Program runs on import. | Guard with `if __name__ == "__main__":`. |

## Commits
1. `fix: resolve bandit findings` - B608, B324, B101 (`commits/01_bandit_fixes.py`)
2. `fix: resolve pylint findings` - naming, docstrings, mutable default, shadowing, else-return, `l`, guard (`commits/02_pylint_fixes.py`)
3. `style: resolve flake8 findings` - line wrapping / PEP 8 (`commits/03_flake8_fixes.py` = final `wildlife_sightings.py`)

Note: after switching MD5 to SHA-256 the observer ID printed for "Arun" changes (it is only a label, not stored anywhere).
