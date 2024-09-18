"""
Handles common things like text rendering, buttons, etc..
"""
from config.defines import *

def grid_align(x):
    """
    Aligns x to the grid size.

    :param x: The value to align
    :return: The aligned value
    """
    return x - (x % GRID_SIZE)