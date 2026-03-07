# Final Project - Full Implementation
# Virtual Robot Simulation with A* Pathfinding and FSM

# =========================
# English: Import necessary libraries
# Arabic: استيراد المكتبات الضرورية
# =========================
from enum import Enum
import time
import heapq

# =========================
# Environment Class
# (No changes from the previous version)
# =========================
class CellType(Enum):
    EMPTY = 0
    OBSTACLE = 1
    GOAL = 2

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[CellType.EMPTY for _ in range(width)] for _ in range(height)]

    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_obstacle(self, x, y):
        if not self.is_within_bounds(x, y):
            return True
        return self.grid[y][x] == CellType.OBSTACLE

    def is_goal(self, x, y):
        return self.grid[y][x] == CellType.GOAL

    def display(self, robot=None, path=None):
        path_coords = set(path) if path else set()
        for y in range(self.height):
            for x in range(self.width):
                if robot and robot.x == x and robot.y == y:
                    if robot.direction == Direction.NORTH: print("^", end=" ")
                    elif robot.direction == Direction.EAST: print(">", end=" ")
                    elif robot.direction == Direction.SOUTH: print("v", end=" ")
                    elif robot.direction == Direction.WEST: print("<", end=" ")
                elif (x, y) in path_coords:
                    print("*", end=" ")
                elif self.grid[y][x] == CellType.OBSTACLE:
                    print("#", end=" ")
                elif self.grid[y][x] == CellType.GOAL:
                    print("G", end=" ")
                else:
                    print(".", end=" ")
            print()
        if robot:
            print(f"Robot State: {robot.state.name}")
        print("-" * (self.width * 2))

# =========================
# Pathfinding (A* Algorithm)
# (No changes from the previous version)
# =========================
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position
    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_pathfinding(environment, start, end):
    start_node = Node(None, start)
    end_node = Node(None, end)
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, start_node)
    while len(open_list) > 0:
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node.position)
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if not environment.is_within_bounds(node_position[0], node_position[1]) or \
               environment.is_obstacle(node_position[0], node_position[1]):
                continue
            if node_position in closed_list:
                continue
            new_node = Node(current_node, node_position)
            new_node.g = current_node.g + 1
            new_node.h = heuristic(new_node.position, end_node.position)
            new_node.f = new_node.g + new_node.h
            if any(open_node for open_node in open_list if new_node == open_node and new_node.g >= open_node.g):
                continue
            heapq.heappush(open_list, new_node)
    return None

# =========================
# Robot Class (with FSM logic)
# =========================
class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class RobotState(Enum):
    """
    English: The states for our Finite State Machine (FSM).
    Arabic: الحالات الخاصة بآلة الحالة المحدودة.
    """
    PLANNING = 0        # English: Robot is calculating the path. / Arabic: الروبوت يقوم بحساب المسار.
    EXECUTING_PATH = 1  # English: Robot is following the calculated path. / Arabic: الروبوت يتبع المسار المحسوب.
    FINISHED = 2        # English: Robot has reached the goal. / Arabic: الروبوت وصل إلى الهدف.
    STUCK = 3           # English: Robot could not find a path. / Arabic: الروبوت لم يتمكن من إيجاد مسار.

class Robot:
    def __init__(self, x, y, direction=Direction.NORTH):
        self.x = x
        self.y = y
        self.direction = direction
        self.state = RobotState.PLANNING # English: Start in PLANNING state. / Arabic: البدء في حالة التخطيط.
        self.path = []
        self.path_index = 0

    def turn_towards(self, target_pos):
        """
        English: Turns the robot to face the target position.
        Arabic: يوجه الروبوت ليواجه الموقع الهدف.
        """
        dx = target_pos[0] - self.x
        dy = target_pos[1] - self.y

        if dx == 1: target_dir = Direction.EAST
        elif dx == -1: target_dir = Direction.WEST
        elif dy == 1: target_dir = Direction.SOUTH
        elif dy == -1: target_dir = Direction.NORTH
        else: return # Already at the target

        # Turn until facing the correct direction
        while self.direction != target_dir:
            # This is a simple turning logic, can be improved
            self.turn_right()

    def move_forward(self):
        """
        English: Moves the robot one step forward. Assumes path is clear.
        Arabic: يحرك الروبوت خطوة واحدة للأمام. يفترض أن المسار خالٍ.
        """
        nx, ny = self.next_position()
        self.x, self.y = nx, ny
        print(f"Action: Moved Forward to ({self.x}, {self.y})")

    def next_position(self):
        dx, dy = 0, 0
        if self.direction == Direction.NORTH: dy = -1
        elif self.direction == Direction.SOUTH: dy = 1
        elif self.direction == Direction.EAST: dx = 1
        elif self.direction == Direction.WEST: dx = -1
        return self.x + dx, self.y + dy
    
    def turn_right(self):
        self.direction = Direction((self.direction.value + 1) % 4)
        print("Action: Turned Right")

    def decide_and_execute(self, environment, goal_pos):
        """
        English: The core FSM logic. Decides what to do based on the current state.
        Arabic: المنطق الرئيسي لآلة الحالة المحدودة. يقرر ما يجب فعله بناءً على الحالة الحالية.
        """
        # === STATE: PLANNING ===
        if self.state == RobotState.PLANNING:
            print("State: PLANNING - Calculating path...")
            path = a_star_pathfinding(environment, (self.x, self.y), goal_pos)
            if path:
                self.path = path
                self.path_index = 1 # Start with the second point in the path
                self.state = RobotState.EXECUTING_PATH
                print(f"Path found: {self.path}")
            else:
                self.state = RobotState.STUCK
                print("No path found!")

        # === STATE: EXECUTING_PATH ===
        elif self.state == RobotState.EXECUTING_PATH:
            print(f"State: EXECUTING_PATH - Following path. Next stop: {self.path[self.path_index]}")
            if self.path_index >= len(self.path):
                # This should not happen if goal check is correct, but as a safeguard
                self.state = RobotState.FINISHED
                return

            next_pos = self.path[self.path_index]
            
            # If not at the next position, move towards it
            if (self.x, self.y) != next_pos:
                self.turn_towards(next_pos)
                self.move_forward()

            # If we arrived at the next position, update index for next step
            if (self.x, self.y) == next_pos:
                self.path_index += 1

        # === STATE: FINISHED or STUCK ===
        # Do nothing in these states
        elif self.state == RobotState.FINISHED:
            print("State: FINISHED - Goal reached.")
        elif self.state == RobotState.STUCK:
            print("State: STUCK - Cannot move.")

# =========================
# Simulation Class (Simplified)
# =========================
class Simulation:
    def __init__(self, environment, robot, goal_pos, max_steps=100):
        self.environment = environment
        self.robot = robot
        self.goal_pos = goal_pos
        self.max_steps = max_steps
        self.current_step = 0

    def step(self):
        """
        English: Executes a single, simplified step of the simulation.
        Arabic: ينفذ خطوة واحدة مبسطة من المحاكاة.
        """
        # 1. Check for terminal states
        if self.robot.state == RobotState.FINISHED or self.robot.state == RobotState.STUCK:
            return False

        # 2. Let the robot decide and act based on its FSM
        self.robot.decide_and_execute(self.environment, self.goal_pos)
        
        # 3. Check if goal is reached after the move
        if (self.robot.x, self.robot.y) == self.goal_pos:
            self.robot.state = RobotState.FINISHED
            return False

        # 4. Check for simulation end conditions
        self.current_step += 1
        if self.current_step >= self.max_steps:
            print("Maximum steps reached.")
            return False

        return True

    def run(self, delay=0.7):
        running = True
        while running:
            # Display the robot and the path it's following
            self.environment.display(self.robot, path=self.robot.path)
            running = self.step()
            time.sleep(delay)
        
        # Final display
        self.environment.display(self.robot, path=self.robot.path)
        print("Simulation finished.")

# =========================
# Main
# =========================
def main():
    env = Environment(width=10, height=10)
    start_pos = (0, 0)
    goal_pos = (7, 7)

    # Add obstacles and goal
    env.grid[2][1] = CellType.OBSTACLE
    env.grid[2][2] = CellType.OBSTACLE
    env.grid[2][3] = CellType.OBSTACLE
    env.grid[2][4] = CellType.OBSTACLE
    env.grid[4][5] = CellType.OBSTACLE
    env.grid[5][5] = CellType.OBSTACLE
    env.grid[6][5] = CellType.OBSTACLE
    env.grid[7][5] = CellType.OBSTACLE
    env.grid[goal_pos[1]][goal_pos[0]] = CellType.GOAL

    # Create the robot
    robot = Robot(x=start_pos[0], y=start_pos[1], direction=Direction.EAST)

    # Create and run the simulation with the FSM-driven robot
    sim = Simulation(env, robot, goal_pos, max_steps=50)
    sim.run()

if __name__ == "__main__":
    main()
