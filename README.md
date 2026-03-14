# Wandering in the Woods

Wandering in the Woods is a K-8 educational simulation built with Tkinter + Pygame.
Students choose a grade-band mode, set grid/player options, place animals on a mini-grid, and run simulations until all players meet.

## What the Program Does Today

- Launches a main menu with 3 modes: K-2, Grades 3-5, Grades 6-8.
- Opens the main menu and mode windows in windowed full-screen (maximized).
- Runs automatic movement simulations (not keyboard-controlled player movement).
- Tracks run-time statistics in seconds.
- Plays background audio and meet cues when assets are available.
- Uses narration text (asynchronous voice output) for each mode.

## Mode Breakdown

### K-2 Mode

- Square grid size input (`N x N`, capped at 15).
- 2 players start at opposite corners.
- One-click run simulation flow.
- Reflection question section at the bottom.

### Grades 3-5 Mode

- Rectangular grid (`width`, `height`), each capped at 15.
- Player count from 2 to 4.
- Click-to-place starting positions on a mini-grid.
- Run statistics: runs, shortest, longest, average (seconds).
- Reflection question section.

### Grades 6-8 Mode

- Rectangular grid (`width`, `height`), each capped at 15.
- Player count from 2 to 4.
- Movement algorithm selection:
	- Random
	- Clockwise
	- Zigzag
	- Spiral
- Click-to-place starting positions on a mini-grid.
- Run statistics in seconds.
- Dynamic bar chart (matplotlib): x-axis is grid size (`WxH`), y-axis is average run time.
- Reflection question section with scrolling.

## Core Simulation Behavior

- Players move one cell at a time in cardinal directions.
- Animal speed multipliers differ by animal type.
- When players meet in the same cell, they merge into a group.
- Simulation continues until all players have merged.

## Tech Stack

- Python 3
- Tkinter (UI)
- Pygame (simulation rendering + audio)
- Matplotlib (Grades 6-8 chart)

## Installation

1. Clone repo:

```bash
git clone https://github.com/bijubjacob/Wandering-in-the-woods.git
cd Wandering-in-the-woods
```

2. Create and activate a virtual environment.

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Windows Executable (No Python Required)

If you already have a packaged build, launch:

```text
dist/WanderingInTheWoods.exe
```

This executable starts the same Tkinter main menu and mode windows.

## Build the Executable (Maintainers)

`pyinstaller` is a packaging tool used for distribution builds. It is not required to run the project from source.

Install it when needed:

```bash
pip install pyinstaller
```

Build command used for this project:

```bash
python -m PyInstaller --noconfirm --clean --windowed --onefile --name WanderingInTheWoods --add-data "assets;assets" --hidden-import matplotlib.backends.backend_tkagg --hidden-import matplotlib.backends._tkagg main.py
```

## Project Structure (Current)

```text
Wandering-in-the-woods/
├── assets/
│   ├── audio/
│   │   ├── background.ogg
│   │   └── meet.flac
│   └── images/
├── docs/
├── modes/
│   ├── k2_ui.py
│   ├── g35_ui.py
│   └── g68_ui.py
├── src/
│   ├── audio.py
│   ├── game.py
│   ├── grid.py
│   ├── narrator.py
│   ├── player.py
│   ├── simulation.py
│   └── ui.py
├── main.py
├── requirements.txt
└── README.md
```

## Notes

- Audio is optional at runtime; if audio init or asset loading fails, simulation still runs.
- Narration uses platform speech support when available.
- `requirements.txt` contains runtime dependencies only.
- A quick validation command used in development:

```bash
python -m py_compile main.py modes/*.py src/*.py
```