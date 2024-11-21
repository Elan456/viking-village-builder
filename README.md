# Invasion of London: Forkbeard's Call
https://github.com/Elan456/viking-village-builder

## Setup instructions
Currently, the game is not built into an exe. To play, you must use Python and install the necessary dependencies.

### 1. Downloading the Game (If you don't already have it)
```sh
git clone https://github.com/Elan456/viking-village-builder.git
cd viking-village-builder
```

### 2. Dependency Installation

```sh
python -m pip install -r requirements.txt
```

This should install pygame and e-pyquadtree.

> e-pyquadtree is a quadtree data structure package written by me, check it out on GitHub: https://github.com/Elan456/pyquadtree

### 3. Running the game 

```sh
python main.py 
```

## Gameplay Instructions 

### Controls

- WASD / Arrow Keys / Middle-Click + Drag = Pan Camera
- Mouse for interacting with and placing buildings
- "N" to show the navigation mesh

### Win Condition
- To win, you must generate 250 soldiers and 10 ships within 100 turns.

### Building

Click + drag on a building from the far-right panel to an empty space within your walls.

If the construction fails, a message will appear in the center to tell you why.

### Turn Management

In the bottom-left corner there is a button to advance to the next turn. This will
trigger each building to produce and consume their respective resources.
Construction projects will advance and you might get a random event.

You only get 100 turns till the end of the game to build your army and prepare for the invasion.

### Resource Panel

The panel in the top-left corner shows your current resources and how much you are producing and consuming.
For the warriors and ships, a projection is shown to indicate how many you will have at the end of 100 turns assuming your current production rate stays the same. 
A resource will turn red if buildings are unable to produce because of a lack of that resource. This is a warning that you need to build more of that resource-producing building.

## Milestone 3 (10/31 - 11/20)

### Features Added (with Point Values Adding to 100)
1. Add construction phases to buildings (7)
2. Move the resource panel to the top-left (2)
3. Have the builders walk to construction sites (4)
4. Add a builder assignment manager (7)
5. Show how many turns are needed for a building to be completed to the hover panel (3)
6. Add a button to upgrade the wall and show the cost to do so (3)
7. Indicate buildings that are too expensive with a red rectangle (3)
8. Add an "along river" check for shipyards (3)
9. Improve the contrast of announcements (2)
10. Have the background color change with the seasons (5)
11. Add debris that float down the river and ripples to make the river more lively (5)
12. Add trees that grow over time and the lumberjacks navigate to them (6)
13. Advance the villagers by a few updates each turn to indicate the passage of time (4)
14. Add building demolition, requires turns just like construction (4)
15. Draw all the building assets (10)
16. Fix some resource consumption and production bugs (3)
17. Add a win condition prediction calculation, so the player knows if they are on track (5)
18. Render boats on the river as more are built (3)
19. Make the boats sway in the water (3)
20. Render soldiers in a box as the army grows (4)
21. Add a fire random event that destroys buildings (5)
22. Add plague, caravan, and blight random events (5)
23. Add descriptions to the buildings' hover panel (3)
24. Improve the Linux resolution (2)
25. Add a more stylized button (2)
26. Add a start screen with a button to start the game (3)
27. Add a win/lose screen with stats (2)
28. Navmesh optimizations using an additional quadtree (5)
29. Resource text changes color if it's over demanded (2)
30. Building panel shows icons for the buildings instead of the building itself (2)
31. Change disable, enable, and demolish buttons to be more stylied (2)

## Milestone 2 (9/17 - 10/30)

[Link to the full changelog](https://github.com/Elan456/viking-village-builder/commits/0.1)

### Features Added
- Random event skeleton
- Buttons
- Main panel (turn and resource display)
- Building panel (To drag and place buildings from)
- Building collision and placement
- Fully animated villagers (Idle + Walking)
- Villager pathfinding using A* algorithm, navigation mesh, and quadtree optimizations
- Ability to disable buildings
- Button to demolish buildings
- Placeholder building assets
- Full set of resource assets
- Resource production and consumption per building
- Resource production prediction algorithm
- Arrow key + WASD camera panning
- Middle-click + drag camera panning
- Villager speech bubbles
- Building definition file as a JSON with parsing
- Wall around the village
