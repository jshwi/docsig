"""
docsig._text
============

Text analysis helpers for comparing docstrings to signatures.
"""

import re as _re
from difflib import SequenceMatcher as _SequenceMatcher

SENTENCE_ABBREVIATIONS = frozenset(
    {
        "al.",
        "approx.",
        "ca.",
        "cf.",
        "dr.",
        "e.g.",
        "eq.",
        "etc.",
        "fig.",
        "figs.",
        "i.e.",
        "incl.",
        "mr.",
        "no.",
        "p.",
        "pp.",
        "resp.",
        "sec.",
        "u.s.",
        "viz.",
        "vol.",
        "vs.",
    },
)


def almost_equal(str1: str, str2: str, mini: float, maxi: float) -> bool:
    """Return True if the strings are equal or ratio in (mini, maxi).

    Uses SequenceMatcher ratio; exact match always returns True.

    :param str1: First string.
    :param str2: Second string.
    :param mini: Lower bound on ratio (exclusive) when not equal.
    :param maxi: Upper bound on ratio (exclusive) when not equal.
    :return: True when equal or mini < ratio < maxi.
    """
    return (str1 == str2) or mini < _SequenceMatcher(
        a=str1,
        b=str2,
    ).ratio() < maxi


def sentence_tokenizer(text: str) -> list[str]:
    """Split text on sentence boundaries, skipping common abbreviations.

    Splits on . ! ? followed by whitespace; treats abbreviations such as
    e.g. and i.e. as non-boundaries.

    :param text: Input string.
    :return: Non-overlapping sentence strings in order.
    """
    abbreviations = SENTENCE_ABBREVIATIONS
    result = []
    start = 0

    for match in _re.finditer(r"(?<!\.)[.!?]\s+", text):
        end = match.end()
        candidate = text[start:end].strip()
        raw_last = candidate.lower().split()[-1]
        # strip leading punctuation so "(e.g." matches "e.g."
        last_word = _re.sub(r"^[^\w.]+", "", raw_last)
        if last_word in abbreviations:
            continue

        result.append(candidate)
        start = end

    if start < len(text):
        result.append(text[start:].strip())

    return result
