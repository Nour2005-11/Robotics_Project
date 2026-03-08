# =========================
# استيراد المكتبات الضرورية
# =========================
import pygame
import time
import heapq
from enum import Enum
import sys
import os

# =========================
# ثوابت الواجهة الرسومية
# =========================
CELL_SIZE = 50
INFO_PANEL_HEIGHT = 50

# الألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# =========================
# الكلاسات الأساسية (البيئة، البحث عن المسار، الروبوت)
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
        if not self.is_within_bounds(x, y): return True
        return self.grid[y][x] == CellType.OBSTACLE

class Node:
    def __init__(self, parent=None, position=None):
        self.parent, self.position = parent, position
        self.g, self.h, self.f = 0, 0, 0
    def __eq__(self, other): return self.position == other.position
    def __lt__(self, other): return self.f < other.f

def heuristic(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_pathfinding(environment, start, end):
    start_node, end_node = Node(None, start), Node(None, end)
    open_list, closed_list = [], set()
    heapq.heappush(open_list, start_node)
    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node.position)
        if current_node == end_node:
            path = []
            current = current_node
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if not environment.is_within_bounds(node_position[0], node_position[1]) or \
               environment.is_obstacle(node_position[0], node_position[1]) or \
               node_position in closed_list:
                continue
            new_node = Node(current_node, node_position)
            new_node.g, new_node.h, new_node.f = current_node.g + 1, heuristic(new_node.position, end_node.position), new_node.g + new_node.h
            if any(open_node for open_node in open_list if new_node == open_node and new_node.g >= open_node.g): continue
            heapq.heappush(open_list, new_node)
    return None

class Direction(Enum):
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270

class RobotState(Enum):
    PLANNING = 0
    EXECUTING_PATH = 1
    FINISHED = 2
    STUCK = 3

class Robot:
    def __init__(self, x, y, direction=Direction.NORTH):
        self.x, self.y, self.direction = x, y, direction
        self.state = RobotState.PLANNING
        self.path, self.path_index = [], 0

    def turn_towards(self, target_pos):
        dx, dy = target_pos[0] - self.x, target_pos[1] - self.y
        if dx == 1: self.direction = Direction.EAST
        elif dx == -1: self.direction = Direction.WEST
        elif dy == 1: self.direction = Direction.SOUTH
        elif dy == -1: self.direction = Direction.NORTH

    def move_forward(self):
        nx, ny = self.next_position()
        self.x, self.y = nx, ny

    def next_position(self):
        if self.direction == Direction.NORTH: return self.x, self.y - 1
        if self.direction == Direction.SOUTH: return self.x, self.y + 1
        if self.direction == Direction.EAST: return self.x + 1, self.y
        if self.direction == Direction.WEST: return self.x - 1, self.y
        return self.x, self.y

    def decide_and_execute(self, environment, goal_pos):
        if self.state == RobotState.PLANNING:
            path = a_star_pathfinding(environment, (self.x, self.y), goal_pos)
            if path:
                self.path, self.path_index = path, 1
                self.state = RobotState.EXECUTING_PATH
            else:
                self.state = RobotState.STUCK
        elif self.state == RobotState.EXECUTING_PATH:
            if self.path_index >= len(self.path):
                self.state = RobotState.FINISHED
                return
            next_pos = self.path[self.path_index]
            if (self.x, self.y) != next_pos:
                self.turn_towards(next_pos)
                self.move_forward()
            if (self.x, self.y) == next_pos:
                self.path_index += 1

# =========================
# كلاس المحاكاة (مع واجهة Pygame)
# =========================
class Simulation:
    def __init__(self, environment, robot, goal_pos, max_steps=100):
        self.environment = environment
        self.robot = robot
        self.goal_pos = goal_pos
        self.max_steps = max_steps
        self.current_step = 0

        pygame.init()
        self.width = self.environment.width * CELL_SIZE
        self.height = self.environment.height * CELL_SIZE + INFO_PANEL_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("محاكاة الروبوت الافتراضي")
        self.font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()

        # __file__ هو متغير خاص في بايثون يحتوي على مسار الملف الحالي
        current_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(current_path, "assets")
        
        try:
            self.assets = {
                'robot': pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "robot.png")).convert_alpha(), (40, 40)),
                'obstacle': pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "obstacle.png")).convert_alpha(), (CELL_SIZE, CELL_SIZE)),
                'goal': pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "goal.png")).convert_alpha(), (CELL_SIZE, CELL_SIZE)),
                'ground': pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "ground.png")).convert(), (CELL_SIZE, CELL_SIZE)),
            }
        except pygame.error as e:
            print(f"Error Loading The Image: {e}")
            print(f"Be Sure that asstes Folder is beside the python file.")
            sys.exit()

    def draw_grid(self):
        for y in range(self.environment.height):
            for x in range(self.environment.width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                self.screen.blit(self.assets['ground'], rect)
                if self.environment.grid[y][x] == CellType.OBSTACLE:
                    self.screen.blit(self.assets['obstacle'], rect)
                elif self.environment.grid[y][x] == CellType.GOAL:
                    self.screen.blit(self.assets['goal'], rect)

    def draw_path(self):
        if self.robot.path:
            for (x, y) in self.robot.path:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(surface, (*YELLOW, 100), (CELL_SIZE // 2, CELL_SIZE // 2), 10)
                self.screen.blit(surface, rect)

    def draw_robot(self):
        rotated_robot = pygame.transform.rotate(self.assets['robot'], -self.robot.direction.value)
        rect = rotated_robot.get_rect(center=(self.robot.x * CELL_SIZE + CELL_SIZE // 2, self.robot.y * CELL_SIZE + CELL_SIZE // 2))
        self.screen.blit(rotated_robot, rect)

    def draw_info_panel(self):
        panel_rect = pygame.Rect(0, self.height - INFO_PANEL_HEIGHT, self.width, INFO_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, BLACK, panel_rect)
        
        state_text = f"State: {self.robot.state.name}"
        text_surface = self.font.render(state_text, True, WHITE)
        text_rect = text_surface.get_rect(center=panel_rect.center)
        self.screen.blit(text_surface, text_rect)

    def step(self):
        if self.robot.state == RobotState.FINISHED or self.robot.state == RobotState.STUCK:
            return
        
        self.robot.decide_and_execute(self.environment, self.goal_pos)
        
        if (self.robot.x, self.robot.y) == self.goal_pos:
            self.robot.state = RobotState.FINISHED
        
        self.current_step += 1
        if self.current_step >= self.max_steps:
            if self.robot.state != RobotState.FINISHED:
                self.robot.state = RobotState.STUCK

    def run(self):
        running = True
        last_step_time = pygame.time.get_ticks()
        step_interval = 500

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_time = pygame.time.get_ticks()
            if current_time - last_step_time > step_interval:
                self.step()
                last_step_time = current_time
                if self.robot.state == RobotState.FINISHED or self.robot.state == RobotState.STUCK:
                    self.draw()
                    pygame.time.wait(3000)
                    running = False

            self.draw()

        pygame.quit()
        sys.exit()

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_path()
        self.draw_robot()
        self.draw_info_panel()
        pygame.display.flip()
        self.clock.tick(30)

# =========================
# الدالة الرئيسية
# =========================
def main():
    env = Environment(width=15, height=12)
    start_pos = (1, 1)
    goal_pos = (13, 10)

    for i in range(8): env.grid[i][4] = CellType.OBSTACLE
    for i in range(4, 12): env.grid[8][i] = CellType.OBSTACLE
    env.grid[3][8] = CellType.OBSTACLE
    env.grid[4][8] = CellType.OBSTACLE
    env.grid[goal_pos[1]][goal_pos[0]] = CellType.GOAL

    robot = Robot(x=start_pos[0], y=start_pos[1], direction=Direction.EAST)

    sim = Simulation(env, robot, goal_pos, max_steps=100)
    sim.run()

if __name__ == "__main__":
    main()
