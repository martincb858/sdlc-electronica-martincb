"""Módulo de conversiones de unidades para sensores."""


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convierte grados Celsius a Fahrenheit."""
    if celsius < -273.15:
        raise ValueError("La temperatura no puede estar por debajo del cero absoluto (-273.15 °C)")
    return (celsius * 9.0 / 5.0) + 32.0


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convierte grados Fahrenheit a Celsius."""
    if fahrenheit < -459.67:
        raise ValueError("La temperatura no puede estar por debajo del cero absoluto (-459.67 °F)")
    return (fahrenheit - 32.0) * 5.0 / 9.0


def celsius_to_kelvin(celsius: float) -> float:
    """Convierte grados Celsius a Kelvin."""
    if celsius < -273.15:
        raise ValueError("La temperatura no puede estar por debajo del cero absoluto (-273.15 °C)")
    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    """Convierte Kelvin a grados Celsius."""
    if kelvin < 0.0:
        raise ValueError("La temperatura en Kelvin no puede ser negativa")
    return kelvin - 273.15


def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """Convierte grados Fahrenheit a Kelvin."""
    return celsius_to_kelvin(fahrenheit_to_celsius(fahrenheit))


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convierte Kelvin a grados Fahrenheit."""
    return celsius_to_fahrenheit(kelvin_to_celsius(kelvin))


def hpa_to_pa(hpa: float) -> float:
    """Convierte hectopascales (hPa) a pascales (Pa)."""
    if hpa < 0.0:
        raise ValueError("La presión no puede ser negativa")
    return hpa * 100.0


def pa_to_hpa(pa: float) -> float:
    """Convierte pascales (Pa) a hectopascales (hPa)."""
    if pa < 0.0:
        raise ValueError("La presión no puede ser negativa")
    return pa / 100.0


def hpa_to_psi(hpa: float) -> float:
    """Convierte hectopascales (hPa) a libras por pulgada cuadrada (PSI)."""
    if hpa < 0.0:
        raise ValueError("La presión no puede ser negativa")
    return hpa * 0.014503773773020923


def psi_to_hpa(psi: float) -> float:
    """Convierte libras por pulgada cuadrada (PSI) a hectopascales (hPa)."""
    if psi < 0.0:
        raise ValueError("La presión no puede ser negativa")
    return psi / 0.014503773773020923
