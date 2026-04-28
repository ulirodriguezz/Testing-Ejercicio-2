"""Unit tests for subtotal and discount logic."""

import pytest

from app.descuentos import Item, calcular_subtotal, calcular_total_con_descuento


def test_subtotal_and_total_with_discount_success():
    """Valid items and in-range discount: totals rounded correctly."""
    items = [
        Item("Cuaderno", 1200.0, 2),
        Item("Lápiz", 350.5, 5),
    ]
    subtotal = calcular_subtotal(items)
    assert subtotal == 4152.5
    assert calcular_total_con_descuento(subtotal, 10.0) == 3737.25


def test_empty_item_list_raises_value_error():
    with pytest.raises(ValueError, match="vacía"):
        calcular_subtotal([])


def test_discount_percent_out_of_range_raises_value_error():
    with pytest.raises(ValueError, match="entre 0 y 100"):
        calcular_total_con_descuento(100.0, 101.0)


def test_edge_full_discount_yields_zero_total():
    assert calcular_total_con_descuento(99.99, 100.0) == 0.0


def test_edge_zero_unit_price_yields_zero_subtotal():
    items = [Item("Muestra", 0.0, 1)]
    assert calcular_subtotal(items) == 0.0
    assert calcular_total_con_descuento(0.0, 0.0) == 0.0
