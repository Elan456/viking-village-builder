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

> e-pyquadtree is a quadtree datas tructure package written by me, check it out on GitHub: https://github.com/Elan456/pyquadtree

### 3. Running the game 

```sh
python main.py 
```

## Gameplay Instructions 

### Controls

- WASD / Arrow Keys / Middle-Click + Drag = Pan Camera
- Mouse for interacting with and placing buildings

### Building

Click + drag on a building from the far-right panel to an empty space within your walls.

If the construction fails, a message will appear in the center to tell you why.