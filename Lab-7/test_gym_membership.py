from hypothesis import given, strategies as st
from gym_membership import parse_plan, calculate_bmi, average_workout


# ---------- 1. Robustness: functions must never crash ----------

@given(st.text() | st.none())
def test_parse_plan_no_crash(s):
    try:
        parse_plan(s)
    except Exception as e:
        assert False, f"parse_plan crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_calculate_bmi_no_crash(s):
    try:
        calculate_bmi(s)
    except Exception as e:
        assert False, f"calculate_bmi crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_average_workout_no_crash(s):
    try:
        average_workout(s)
    except Exception as e:
        assert False, f"average_workout crashed with: {e!r} on input {s!r}"


# ---------- 2. Non-string / odd types ----------

@given(st.one_of(st.integers(), st.floats(), st.booleans(), st.lists(st.integers()),
                 st.dictionaries(st.text(), st.integers()), st.binary()))
def test_non_string_inputs_return_none(x):
    assert parse_plan(x) is None
    assert calculate_bmi(x) is None
    assert average_workout(x) is None


# ---------- 3. Valid inputs give correct results ----------

@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1),
       st.integers(min_value=1, max_value=9999))
def test_parse_plan_valid(plan, months):
    assert parse_plan(f"{plan}-{months}") == (plan.upper(), months)


@given(st.floats(min_value=1, max_value=500, allow_nan=False),
       st.floats(min_value=0.5, max_value=3, allow_nan=False))
def test_calculate_bmi_valid(weight, height):
    result = calculate_bmi(f"{weight},{height}")
    assert result == round(weight / (float(str(height)) ** 2), 1)


@given(st.lists(st.integers(min_value=0, max_value=1000), min_size=1, max_size=50))
def test_average_workout_valid(values):
    result = average_workout(" ".join(map(str, values)))
    assert result == sum(values) // len(values)
    assert min(values) <= result <= max(values)


# ---------- 4. Output properties on arbitrary text ----------

@given(st.text())
def test_parse_plan_output_shape(s):
    r = parse_plan(s)
    if r is not None:
        plan, months = r
        assert plan == plan.upper() and plan.isalpha()
        assert isinstance(months, int) and months > 0


@given(st.text())
def test_calculate_bmi_output_shape(s):
    r = calculate_bmi(s)
    if r is not None:
        assert isinstance(r, float) and r > 0 or r == 0.0


@given(st.text())
def test_average_workout_output_shape(s):
    r = average_workout(s)
    if r is not None:
        assert isinstance(r, int) and r >= 0


# ---------- 5. Known edge cases found by fuzzing ----------

def test_known_edge_cases():
    assert parse_plan("") is None
    assert parse_plan("GOLD") is None
    assert parse_plan("GOLD-") is None
    assert parse_plan("-12") is None
    assert parse_plan("GOLD-1-2") is None
    assert parse_plan("GOLD-abc") is None
    assert parse_plan("GOLD-0") is None
    assert parse_plan("gold-12") == ("GOLD", 12)

    assert calculate_bmi("70,0") is None          # ZeroDivisionError
    assert calculate_bmi("70,-1.75") is None
    assert calculate_bmi("70") is None
    assert calculate_bmi("a,b") is None
    assert calculate_bmi("nan,1.7") is None
    assert calculate_bmi("70,1e200") is None      # overflow
    assert calculate_bmi("70,1.75") == 22.9

    assert average_workout("") is None            # ZeroDivisionError
    assert average_workout("   ") is None
    assert average_workout("45 abc") is None
    assert average_workout("-5 10") is None
    assert average_workout("45 60 30") == 45
