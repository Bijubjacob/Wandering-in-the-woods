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

🏗 Project Structure
Wandering-in-the-woods
│
├── build
|
├── dist
│   └── main.exe (exetuable file that you can use)
|
├── modes
│   ├── k2_ui.py
│   ├── g35_ui.py
│   └── g68_ui.py
│
├── src
|   ├── assets.py
|   |     └── background.ogg
|   |     └── meet.flac
│   ├── game.py
│   ├── grid.py
│   ├── player.py
│   ├── simulation.py
│   ├── stats.py
│   ├── ui.py
│   └── audio.py
│
├── engine.py
├── main.py
├── main.spec
├── models.py
├── requirements.txt
└── README.md

⚙ Installation

Clone the repository:

git clone https://github.com/bijubjacob/Wandering-in-the-woods.git

Navigate into the folder:

cd Wandering-in-the-woods

Navigate to the "dist" folder

Double click the "main.exe" file

A menu will open for you to select a game mode (K-2, 3-5, 6-8)

Select which game mode you want to play

Maximize each window for the best user experience

🚀 Future Improvements

Possible enhancements include:

Data graphs for meeting times

Experiment mode for grid size comparisons

Character sprites

Forest background graphics

Sound effects and narration

👨‍💻 Authors

Collin Cimaroli
Carlos Fuentes
Alexis Granados
Biju Jacob

Software Engineering Project
Lewis University

📚 Learning Focus

This project demonstrates concepts from:

Software Engineering

Simulation Modeling

Algorithm Design

Educational Game Development