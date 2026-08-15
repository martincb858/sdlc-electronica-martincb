def celsius_to_fahrenheit(c: float) -> float:
    """Convierte una temperatura en grados Celsius a Fahrenheit redondeada a 2 decimales."""
    return round((c * 9.0 / 5.0) + 32.0, 2)
