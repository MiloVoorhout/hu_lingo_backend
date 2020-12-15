"""
    Round enum
"""

from enum import Enum


class RoundType(Enum):
    """
        Round enum with 3 value types for the rounds word length
    """
    FiveCharacters = 5
    SixCharacters = 6
    SevenCharacters = 7
