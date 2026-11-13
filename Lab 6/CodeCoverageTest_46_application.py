import pytest
from photo_print_order import (
    extra_print_charge,
    order_valid,
    dispatch_status,
)


# EXTRA PRINT CHARGE TESTS

def test_within_included_prints():
    # 15 copies of 4x6 are inside the 20 included prints, no charge
    assert extra_print_charge("4x6", 15, "matte", False) == 0


def test_member_bonus_included_prints():
    # members get 5 extra included prints on 4x6: 30 - 25 = 5 extra at matte rate 4
    assert extra_print_charge("4x6", 30, "matte", True) == 20


def test_no_member_bonus_on_8x10():
    # the member bonus does not apply to 8x10: 15 - 10 = 5 extra at rate 4
    assert extra_print_charge("8x10", 15, "matte", True) == 20


def test_non_member_glossy_charge():
    # 20 - 15 = 5 extra at the non-matte rate 7
    assert extra_print_charge("5x7", 20, "glossy", False) == 35


def test_large_order_rate_increase():
    # 80 - 20 = 60 extra, over 50 so matte rate 4 + 2 = 6
    assert extra_print_charge("4x6", 80, "matte", False) == 360


def test_unknown_print_size_rejected():
    with pytest.raises(ValueError):
        extra_print_charge("10x12", 10, "matte", False)


def test_negative_copies_rejected():
    with pytest.raises(ValueError):
        extra_print_charge("4x6", -1, "matte", False)


# ORDER VALIDATION TESTS

def test_rush_order_within_limit():
    assert order_valid(10, 50, True) is True


def test_rush_order_over_limit():
    assert order_valid(10, 51, True) is False


def test_large_file_rejected():
    # non-rush orders over 25 MB are not accepted
    assert order_valid(30, 100, False) is False


def test_normal_order_valid():
    assert order_valid(10, 500, False) is True


def test_normal_order_too_many_copies():
    assert order_valid(10, 501, False) is False


# DISPATCH STATUS TESTS

def test_framed_domestic_on_time():
    # framed cutoff is 24 hours, order placed exactly at cutoff
    assert dispatch_status(24, True, False) == "on_time"


def test_unframed_international_tight():
    # unframed international cutoff is 36, tight window starts at 30
    assert dispatch_status(30, False, True) == "tight"


def test_framed_international_missed():
    # framed international cutoff is 48, 30 hours is outside the tight window
    assert dispatch_status(30, True, True) == "missed"
