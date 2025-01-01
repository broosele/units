""" giorgi - shared

Some shared code for the giorgi library.

author: Bram Rooseleer
copyright: Bram Rooseleer
"""


SUPERSCRIPTS: dict[str, str] = {
    '-': '⁻',
    '0': '⁰',
    '1': '¹',
    '2': '²',
    '3': '³',
    '4': '⁴',
    '5': '⁵',
    '6': '⁶',
    '7': '⁷',
    '8': '⁸',
    '9': '⁹',
}
"""A mapping of number characters on their superscript version."""


def exponent_superscript(exponent: int) -> str: 
    """Return a string representing the given integer in superscript."""
    if exponent == 1:
        return ''
    return ''.join(SUPERSCRIPTS[c] for c in str(exponent))
