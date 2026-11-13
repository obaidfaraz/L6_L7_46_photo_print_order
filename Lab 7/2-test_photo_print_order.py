from hypothesis import given, strategies as st
from photo_print_order import parse_order, file_size_average, payable_amount

@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    try:
        parse_order(s)
    except Exception as e:
        assert False, f"parse_order crashed with: {e!r}"

@given(st.text() | st.none())
def test_file_size_average_no_crash(s):
    try:
        file_size_average(s)
    except Exception as e:
        assert False, f"file_size_average crashed with: {e!r}"

@given(st.text() | st.none())
def test_payable_amount_no_crash(s):
    try:
        payable_amount(s)
    except Exception as e:
        assert False, f"payable_amount crashed with: {e!r}"


# Extra property checks on the results
@given(st.text() | st.none())
def test_parse_order_result_shape(s):
    r = parse_order(s)
    assert r is None or (isinstance(r[0], str) and r[0] and r[1] >= 0)

@given(st.text() | st.none())
def test_file_size_average_result_not_negative(s):
    r = file_size_average(s)
    assert r is None or r >= 0

@given(st.text() | st.none())
def test_payable_amount_result_not_negative(s):
    r = payable_amount(s)
    assert r is None or r >= 0

def test_valid_examples():
    assert parse_order("4x6:25") == ("4X6", 25)
    assert file_size_average("4,8,12") == 8
    assert payable_amount("450|50") == 481.0
