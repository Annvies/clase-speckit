"""Paleta fija de colores para las materias.

Todos los colores tienen un contraste de al menos 4.5:1 con texto blanco (WCAG AA).
"""

PALETA = (
    {"clave": "azul", "nombre": "Azul", "hex": "#1D4ED8"},
    {"clave": "verde", "nombre": "Verde", "hex": "#15803D"},
    {"clave": "rojo", "nombre": "Rojo", "hex": "#B91C1C"},
    {"clave": "naranja", "nombre": "Naranja", "hex": "#C2410C"},
    {"clave": "morado", "nombre": "Morado", "hex": "#7E22CE"},
    {"clave": "rosa", "nombre": "Rosa", "hex": "#BE185D"},
    {"clave": "turquesa", "nombre": "Turquesa", "hex": "#0F766E"},
    {"clave": "gris", "nombre": "Gris", "hex": "#4B5563"},
)

CLAVES_COLOR = frozenset(color["clave"] for color in PALETA)
