"""Cálculo de subtotales y totales con descuento por porcentaje."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    """Ítem de un pedido con precio unitario y cantidad."""

    nombre: str
    precio_unitario: float
    cantidad: int


def calcular_subtotal(items: list[Item]) -> float:
    """
    Suma precio_unitario * cantidad de cada ítem.

    Lanza ValueError si la lista está vacía, si algún precio es negativo
    o la cantidad no es positiva.
    """
    if not items:
        raise ValueError("La lista de ítems no puede estar vacía")
    total = 0.0
    for item in items:
        if item.precio_unitario < 0:
            raise ValueError("El precio unitario no puede ser negativo")
        if item.cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo")
        total += item.precio_unitario * item.cantidad
    return round(total, 2)


def calcular_total_con_descuento(subtotal: float, porcentaje_descuento: float) -> float:
    """
    Aplica un descuento porcentual al subtotal y devuelve el total a pagar.

    El porcentaje debe estar entre 0 y 100 (ambos inclusive).
    El subtotal no puede ser negativo.
    """
    if subtotal < 0:
        raise ValueError("El subtotal no puede ser negativo")
    if porcentaje_descuento < 0 or porcentaje_descuento > 100:
        raise ValueError("El porcentaje de descuento debe estar entre 0 y 100")
    factor = 1.0 - (porcentaje_descuento / 100.0)
    return round(subtotal * factor, 2)
