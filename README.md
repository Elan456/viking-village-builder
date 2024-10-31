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

### Building

Click + drag on a building from the far-right panel to an empty space within your walls.

If the construction fails, a message will appear in the center to tell you why.

### Turn Management

In the bottom-right corner there is a button to advance to the next turn. This will
trigger each building to produce and consume their respective resources.
Construction projects will advance and you might get a random event.

You only get 100 turns till the end of the game to build your army and prepare for the invasion.

## Milestone 2

[Link to the full changelog](https://github.com/Elan456/viking-village-builder/commits/0.1)

### Features added
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
