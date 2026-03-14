🌲 Wandering in the Woods

Wandering in the Woods is an educational simulation/game built with Python and Pygame.
The game helps students explore computational thinking, random processes, and grid-based algorithms through an interactive forest wandering scenario.

Players are lost in a forest represented by a grid and must move around until they find each other.

This project is designed for K–8 students and includes multiple complexity levels for different grade groups.

🎮 Game Overview

The forest is represented as a rectangular grid.

Each player occupies a single cell in the grid.

Players cannot see or hear each other until they occupy the same cell.

When both players land on the same cell:

🎉 They find each other and the simulation ends.

🧠 Educational Concepts

This project demonstrates:

Computational thinking

Grid-based environments

Algorithmic movement

Random walks

Data collection

Simulation experiments

Students can explore how movement strategies affect the time it takes for players to meet.

🎮 Controls
Key	Action
W A S D	Move Player 1
Arrow Keys	Move Player 2
R	Reset the game
Close Window	Exit the program

Player 1 starts in the top-left corner
Player 2 starts in the bottom-right corner

🏗 Project Structure
Wandering-in-the-woods
│
├── assets
│   ├── audio
│   │   ├── background.ogg
│   │   └── meet.flac
│   └── images
│
├── docs
├── modes
│   ├── k2_ui.py
│   ├── g35_ui.py
│   └── g68_ui.py
│
├── src
│   ├── audio.py
│   ├── game.py
│   ├── grid.py
│   ├── player.py
│   ├── simulation.py
│   ├── stats.py
│   └── ui.py
│
├── main.py
├── requirements.txt
└── README.md
⚙ Installation

Clone the repository:

git clone https://github.com/bijubjacob/Wandering-in-the-woods.git

Navigate into the folder:

cd Wandering-in-the-woods

Create a virtual environment:

python3 -m venv .venv

Activate it:

Mac / Linux

source .venv/bin/activate

Windows

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
▶ Running the Game

Run the program with:

python3 main.py

A game window will open and players can begin moving around the forest grid.

🧮 Algorithm

Each player moves on the grid according to user input.

Movement is limited to four directions:

UP
DOWN
LEFT
RIGHT

The game checks after each move whether both players occupy the same grid cell.

If they do:

players have met → simulation ends
🚀 Future Improvements

Possible enhancements include:

Main menu with grade level selection

Random wandering simulation mode

Data graphs for meeting times

Experiment mode for grid size comparisons

Character sprites

Forest background graphics

Sound effects and narration

👨‍💻 Authors

Software Engineering Project
Lewis University

📚 Learning Focus

This project demonstrates concepts from:

Software Engineering

Simulation Modeling

Algorithm Design

Educational Game Development