"""
One-time surface conversion after the display is created.

pygame convert()/convert_alpha() require an active display mode; many assets are
loaded at import time before set_mode, so we convert them once from Game init.
"""

import pygame


_converted = False


def convert_loaded_surfaces() -> None:
    global _converted
    if _converted:
        return
    _converted = True

    from game import resources
    for name, image in list(resources.resource_to_icon.items()):
        resources.resource_to_icon[name] = image.convert_alpha()

    from buildings.building_info import BldInfo
    for name, image in list(BldInfo.images.items()):
        BldInfo.images[name] = image.convert_alpha()
    for name, image in list(BldInfo.icons.items()):
        BldInfo.icons[name] = image.convert_alpha()

    from world import tree as tree_mod
    for ages in (
        tree_mod.Tree.winter_birch_ages,
        tree_mod.Tree.summer_birch_ages,
        tree_mod.Tree.winter_oak_ages,
        tree_mod.Tree.summer_oak_ages,
    ):
        for i, img in enumerate(ages):
            ages[i] = img.convert_alpha()

    from world.cloud import CloudHandler
    CloudHandler.surfaces = [s.convert_alpha() for s in CloudHandler.surfaces]

    from world.floater import Floater
    for path, image in list(Floater.SCALED_IMAGES.items()):
        Floater.SCALED_IMAGES[path] = image.convert_alpha()

    from villagers.villager import Villager
    Villager.prepare_frames()
