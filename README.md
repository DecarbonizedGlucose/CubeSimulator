# CubeSimulator

_A simple 3x3 Rubik's Cube simulator with keyboard & GUI controls._

For a detailed Chinese README, see [`README_zh.md`](./README_zh.md).

## Overview

CubeSimulator is a desktop simulator for a standard 3x3 Rubik's Cube. It uses:

- **pygame** for rendering a pseudo-3D view of three faces of the cube
- **Tkinter** for the control panel (buttons, scramble, timer, etc.)
- **kociemba** as the solver backend (two-phase algorithm)

The cube notation follows the commonly used WCA-style notation; single-layer turns use the standard Singmaster notation.

Repository: <https://github.com/DecarbonizedGlucose/CubeSimulator/>

## Features

- One-click reset (restore cube to solved state)
- Control the cube via GUI buttons or keyboard shortcuts
- Generate random scrambles and display the scramble sequence
- Manually input cube state (with validation); apply it to the cube
- Solve the current state using the kociemba algorithm (A* two-phase)
- Step-by-step auto-solve animation (with small delay for visual effect)
- Simple timer for manual solves (not recommended together with auto-solve)

> Note: For the auto-solve feature, the cube could be restored almost instantly.
> A delay of `0.03` seconds between steps is intentionally added just for
> better visual feedback.

## Requirements

### Runtime

- Python **3.8+** (tested with CPython 3.9)
- A desktop environment with support for **Tkinter** and **SDL2** (pygame)

Recommended fonts:

- `Microsoft YaHei` (for Chinese text; optional)
- `Consolas` (for UI labels; if missing, the UI will still work but may look worse)

### Python packages

You need the following third-party packages:

- `kociemba` – cube solver
- `pygame` or `pygame-ce` – rendering and keyboard input

Install via pip:

```sh
pip install kociemba
pip install pygame-ce  # or: pip install pygame
```

On some Linux distros (e.g. Arch Linux), it is recommended to install SDL2
system libraries first, for example:

```sh
# Arch Linux example
sudo pacman -S python tk sdl2 sdl2_image sdl2_mixer sdl2_ttf
```

## How to Run

Clone the repository and run the main script:

```sh
git clone https://github.com/DecarbonizedGlucose/CubeSimulator.git
cd CubeSimulator

python CubeSimulator.py
```

Two windows should appear:

1. A **pygame** window showing the cube
2. A **Tkinter** control window with buttons and menu

If nothing happens or only one window shows up, see the FAQ section below.

## Keyboard Shortcuts

Cube rotations (Singmaster-style):

```text
Q -> z'    W -> x     E -> z
A -> y'    S -> x'    D -> y
6 -> S     7 -> E'    8 -> M'
T -> B'    Y -> U'    U -> U     I -> B
F -> L'    G -> L     J -> R'    K -> R
V -> D     B -> F'    N -> F     M -> D'
Space -> toggle between single-layer / double-layer & middle-layer moves
```

The Tkinter control window also provides buttons for all basic moves,
middle-layer turns, whole-cube rotations, scramble, solve, and timing.

## Known Issues & FAQ

### 1. Program does not start / no window appears

Check the basics first:

- Run from a terminal and see if there is any Python traceback.
- Make sure you are **not** running in a pure Wayland session without XWayland.

On Linux, if you see an error like:

```text
pygame.error: Could not make GL context current: BadAccess
```

This usually means the OpenGL context cannot be created in the current
environment or thread. The current version avoids requesting an explicit
OpenGL context and runs pygame in the main thread, which fixes this on most
Linux desktops. If you still see this error, please open an issue with your
OS, desktop environment, Python and pygame versions.

### 2. `ImportError: No module named tkinter`

This means the Tk runtime is not installed or not linked to your Python
installation.

- On **Arch Linux**:

	```sh
	sudo pacman -S python tk
	```

- On **Ubuntu / Debian**:

	```sh
	sudo apt-get install python3-tk
	```

After installing, re-run:

```sh
python CubeSimulator.py
```

### 3. `ModuleNotFoundError: No module named 'kociemba'` / `pygame`

Install the required packages:

```sh
pip install kociemba
pip install pygame-ce  # or: pip install pygame
```

If you are using a virtual environment, ensure it is activated before
installing and running.

### 4. Exiting does not close all windows

The current version provides a unified `sysQuit()` function that stops the
pygame loop and closes the Tk control window. Use the **"退出程序"** menu
entry or close the Tk window to exit cleanly. If you still see zombie
processes or errors, please report them with your platform details.

## License

This project is released under the MIT License. See the `LICENSE` file if
available, or the repository page for more details.