"""Punto de entrada: demostración por consola del carrito con descuentos."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from app.descuentos import Item, calcular_subtotal, calcular_total_con_descuento


def _cargar_items_desde_json(ruta: Path) -> list[Item]:
    data = json.loads(ruta.read_text(encoding="utf-8"))
    return [
        Item(
            nombre=str(entry["nombre"]),
            precio_unitario=float(entry["precio_unitario"]),
            cantidad=int(entry["cantidad"]),
        )
        for entry in data["items"]
    ]


def _pedir_porcentaje_descuento() -> float:
    """Solicita al usuario el porcentaje hasta obtener un valor entre 0 y 100."""
    while True:
        raw = input("Porcentaje de descuento (0-100), Enter para usar 10: ").strip()
        if raw == "":
            return 10.0
        try:
            valor = float(raw.replace(",", "."))
        except ValueError:
            print("  Ingrese un número válido.")
            continue
        if valor < 0 or valor > 100:
            print("  El valor debe estar entre 0 y 100.")
            continue
        return valor


def _pedir_item_opcional() -> Item | None:
    """
    Permite agregar un ítem extra. Si el nombre queda vacío, no se agrega nada.
    """
    nombre = input("Nombre del producto extra (vacío = no agregar): ").strip()
    if not nombre:
        return None
    while True:
        precio_raw = input("  Precio unitario: ").strip().replace(",", ".")
        try:
            precio = float(precio_raw)
            if precio < 0:
                print("  El precio no puede ser negativo.")
                continue
            break
        except ValueError:
            print("  Ingrese un número válido.")
    while True:
        cant_raw = input("  Cantidad (entero positivo): ").strip()
        try:
            cantidad = int(cant_raw)
            if cantidad <= 0:
                print("  La cantidad debe ser mayor que 0.")
                continue
            break
        except ValueError:
            print("  Ingrese un entero válido.")
    return Item(nombre=nombre, precio_unitario=precio, cantidad=cantidad)


def _porcentaje_desde_argv() -> float | None:
    if len(sys.argv) <= 1:
        return None
    try:
        p = float(sys.argv[1].replace(",", "."))
    except ValueError:
        return None
    if p < 0 or p > 100:
        return None
    return p


def main() -> None:
    base = Path(__file__).resolve().parent
    ejemplo = base / "resources" / "items_ejemplo.json"
    interactive = sys.stdin.isatty()

    items = list(_cargar_items_desde_json(ejemplo))
    print("Ítems cargados desde resources/items_ejemplo.json\n")
    for it in items:
        print(f"  - {it.nombre}: {it.cantidad} x ${it.precio_unitario:.2f}")

    print()
    if interactive:
        extra = _pedir_item_opcional()
        if extra is not None:
            items.append(extra)
            print(f"  Sumado: {extra.nombre}\n")

    argv_pct = _porcentaje_desde_argv()
    if interactive:
        if argv_pct is not None:
            porcentaje = argv_pct
            print(f"Descuento desde argumento: {porcentaje:.1f}%\n")
        else:
            porcentaje = _pedir_porcentaje_descuento()
            print()
    else:
        porcentaje = argv_pct if argv_pct is not None else 10.0
        if argv_pct is None:
            print(f"(Sin consola interactiva: descuento por defecto {porcentaje:.1f}%)\n")

    subtotal = calcular_subtotal(items)
    total = calcular_total_con_descuento(subtotal, porcentaje)

    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Descuento aplicado: {porcentaje:.1f}%")
    print(f"Total a pagar: ${total:.2f}")


if __name__ == "__main__":
    main()
