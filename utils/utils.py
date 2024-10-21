"""
Handles common things like text rendering, buttons, etc..
"""
from config.defines import *
import pygame 

def grid_align(x):
    """
    Aligns x to the grid size.

    :param x: The value to align
    :return: The aligned value
    """
    return x - (x % GRID_SIZE)

def longTextnewLines(text, maxchars):  # Puts ~ where new line should be

    chars = 0
    newstring = ""
    for c in text:
        chars += 1

        if chars > maxchars and c == " ":
            newstring += "~"
            chars = 0
        else:
            newstring += c

    return newstring

def long_text(surface, coor, newLinedtext, text_color, font, maxchar,
              align="center", rect_color=(0,0,0,0), border_color=(0,0,0,0)):  # Runs slow may need to optimize

    parts = []
    partsrendertext = []
    part = ""

    for c in newLinedtext:
        if c == "~":
            parts.append(part)
            part = ""
        else:
            part += c
    parts.append(part)

    for p in range(len(parts)):
        partsrendertext.append(font.render(parts[p], True, text_color))

    x, y = coor[0], coor[1]
    r = partsrendertext[0].get_rect()
    if align == "center":
        x -= r.width / 2
        y -= r.height / 2

    true_rect = [x, y, r.width, r.height * len(parts)]
    # Update width by finding the longest line
    for p in partsrendertext:
        r = p.get_rect()
        if r.width > true_rect[2]:
            true_rect[2] = r.width

    # Draw the background rectangle
    # Create opcaity surface
    new_surface = pygame.Surface((true_rect[2], true_rect[3]), pygame.SRCALPHA)
    new_surface.fill(rect_color)
    # Draw border
    pygame.draw.rect(new_surface, border_color, (0, 0, true_rect[2], true_rect[3]), 1)
    surface.blit(new_surface, (x, y))



    for p in range(len(parts)):
        surface.blit(partsrendertext[p], (x, y + r.height * p))

    return len(parts) * r.height