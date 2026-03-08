# Virtual Robot Simulation Project

## Project Overview
This project involves the design and implementation of a virtual autonomous robot operating within a simulated 2D environment using Python. The primary focus is on programming and algorithmic thinking, simulating robotic behavior without physical hardware interaction. The robot makes decisions based on virtual sensor inputs and executes actions to achieve a defined goal.

## Implemented Features
This project successfully implements all core requirements and extends functionality through three advanced tracks, exceeding the minimum requirement of two extension tracks.

### Core Requirements:
*   **2D Environment:** A grid-based environment with defined boundaries and obstacles.
*   **Robot Model:** A robot model with position, orientation, and internal states (e.g., PLANNING, EXECUTING_PATH, FINISHED, STUCK).
*   **Movement System:** Defined movement commands and collision prevention logic.
*   **Decision-Making Logic:** Rule-based logic for robot behavior, integrating sensor data and environment state.
*   **Simulation Loop:** Step-by-step execution with clear updates of the robot's state.

### Extension Tracks Implemented:
1.  **Path Planning (A* Algorithm):** The robot autonomously finds an optimal path to a target goal using the A* search algorithm. This involves calculating heuristics and managing open/closed lists to efficiently navigate the environment.
2.  **Finite State Machine (FSM):** The robot's behavior is managed through a clearly defined Finite State Machine, with states such as `PLANNING`, `EXECUTING_PATH`, `FINISHED`, and `STUCK`. Transitions between these states govern the robot's actions.
3.  **User Interface (Pygame GUI):** A graphical user interface (GUI) is implemented using the Pygame library, providing a visual representation of the robot's movement, the environment, obstacles, and the goal. This enhances the simulation's interactivity and clarity.

## Algorithms Explained

### A* Pathfinding Algorithm
The A* algorithm is an informed search algorithm used to find the shortest path between two points in a graph or grid. It combines features of Dijkstra's algorithm and greedy best-first search to efficiently explore the search space. It uses a heuristic function to estimate the cost from the current node to the goal, and a cost function to track the actual cost from the start node to the current node. The sum of these two (`f = g + h`) guides the search towards the most promising paths.

In this project, the A* algorithm is used by the robot to calculate the optimal path from its current position to the designated goal, avoiding obstacles.

### Finite State Machine (FSM)
A Finite State Machine (FSM) is a mathematical model of computation used to design sequential logic and concurrent systems. It consists of a finite number of states, transitions between those states, and actions. The system can only be in one state at any given time; it moves from one state to another when a triggering event or condition is met.

For this robot simulation, the FSM manages the robot's high-level behavior:
*   **PLANNING:** The robot is in this state when it needs to calculate a path to the goal.
*   **EXECUTING_PATH:** Once a path is found, the robot enters this state and follows the calculated path.
*   **FINISHED:** The robot reaches this state when it successfully arrives at the goal.
*   **STUCK:** If the robot cannot find a path or gets trapped, it transitions to the STUCK state.

## How to Run the Program

### Prerequisites
*   Python 3.x installed.
*   `pygame` library: Install using pip:
    ```bash
    pip install pygame
    ```

### Setup
1.  **Save the Code:** Save the provided Python code (e.g., `robot_simulation.py`).
2.  **Create Assets Folder:** Create a folder named `assets` in the same directory as your Python script. This folder must contain the following image files:
    *   `robot.png` (e.g., a 40x40 pixel image for the robot)
    *   `obstacle.png` (e.g., a 50x50 pixel image for obstacles)
    *   `goal.png` (e.g., a 50x50 pixel image for the goal)
    *   `ground.png` (e.g., a 50x50 pixel image for the ground/empty cells)
    
    *(Note: Placeholder images can be simple colored squares if specific graphics are not available.)*

### Execution
Navigate to the directory containing `robot_simulation.py` and the `assets` folder in your terminal, then run the script:

```bash
python robot_simulation.py
```

The Pygame window will open, displaying the robot simulation. The robot will plan its path and move towards the goal, with its state displayed in an info panel.

