import pytest
from photo_print_order import (
    extra_print_charge,
    order_valid,
    dispatch_status,
)


# EXTRA PRINT CHARGE - every decision outcome

def test_unknown_print_size_rejected():
    # if print_size not in INCLUDED_PRINTS -> True
    with pytest.raises(ValueError):
        extra_print_charge("10x12", 10, "matte", False)


def test_known_print_size_accepted():
    # same condition -> False
    assert extra_print_charge("4x6", 15, "matte", False) == 0


def test_negative_copies_rejected():
    # if copies < 0 -> True
    with pytest.raises(ValueError):
        extra_print_charge("4x6", -1, "matte", False)


def test_zero_copies_allowed():
    # copies < 0 -> False, and extra <= 0 -> True
    assert extra_print_charge("4x6", 0, "matte", False) == 0


def test_member_bonus_applied():
    # is_member and print_size != "8x10" -> True
    assert extra_print_charge("4x6", 30, "matte", True) == 20


def test_member_bonus_not_applied_to_8x10():
    # same condition -> False because the size is 8x10
    assert extra_print_charge("8x10", 15, "matte", True) == 20


def test_member_bonus_not_applied_to_non_member():
    # same condition -> False because is_member is False
    assert extra_print_charge("4x6", 25, "matte", False) == 20


def test_extra_prints_charged():
    # extra <= 0 -> False, small extra at matte rate
    assert extra_print_charge("4x6", 40, "matte", False) == 80


def test_matte_rate_selected():
    # finish == "matte" -> True
    assert extra_print_charge("5x7", 20, "matte", False) == 20


def test_non_matte_rate_selected():
    # finish == "matte" -> False, glossy uses rate 7
    assert extra_print_charge("5x7", 20, "glossy", False) == 35


def test_large_order_threshold_crossed():
    # extra > 50 -> True, matte rate 4 + 2
    assert extra_print_charge("4x6", 80, "matte", False) == 360


def test_small_order_threshold_not_crossed():
    # extra > 50 -> False, plain glossy rate
    assert extra_print_charge("5x7", 20, "glossy", False) == 35


def test_large_canvas_order_surcharge():
    # extra > 50 -> True and finish == "canvas" -> True
    assert extra_print_charge("4x6", 80, "canvas", False) == 840


def test_large_non_canvas_order_no_surcharge():
    # extra > 50 -> True and finish == "canvas" -> False
    assert extra_print_charge("4x6", 80, "glossy", False) == 540


# ORDER VALID - every decision outcome

def test_rush_order_within_limit():
    # is_rush -> True, copies <= 50 -> True
    assert order_valid(10, 50, True) is True


def test_rush_order_over_limit():
    # is_rush -> True, copies <= 50 -> False
    assert order_valid(10, 51, True) is False


def test_non_rush_large_file_rejected():
    # is_rush -> False, file_mb > 25 -> True
    assert order_valid(30, 100, False) is False


def test_non_rush_small_file_accepted():
    # file_mb > 25 -> False, copies <= 500 -> True
    assert order_valid(25, 500, False) is True


def test_non_rush_too_many_copies_rejected():
    # copies <= 500 -> False
    assert order_valid(10, 501, False) is False


# DISPATCH STATUS - every decision outcome

def test_framed_cutoff_used():
    # is_framed -> True
    assert dispatch_status(24, True, False) == "on_time"


def test_unframed_cutoff_used():
    # is_framed -> False
    assert dispatch_status(12, False, False) == "on_time"


def test_international_extension_applied():
    # is_international -> True, 30 hours is tight against the 36 hour cutoff
    assert dispatch_status(30, False, True) == "tight"


def test_domestic_no_extension():
    # is_international -> False, 5 hours misses the 12 hour cutoff
    assert dispatch_status(5, False, False) == "missed"


def test_on_time_at_cutoff():
    # hours >= cutoff -> True
    assert dispatch_status(48, True, True) == "on_time"


def test_tight_window_lower_edge():
    # hours >= cutoff -> False, hours >= cutoff - 6 -> True
    assert dispatch_status(42, True, True) == "tight"


def test_missed_below_tight_window():
    # both comparisons -> False
    assert dispatch_status(41, True, True) == "missed"
