import numpy as np
import time
from tkinter import Tk, Label, StringVar
from copy import  copy

from typing import Union, Type

from display_helper import pretty_matrix, example_window

EMPTY_SYMBOL = 0
ACTOR_SYMBOL = 1
TARGET_SYMBOL = 9

# SHORT TERM
# TODO: GET LOGS OF PASSED ACTIONS

# MID TERM
# TODO: REVIEW NOTES
# TODO: IMPLEMENT BASIC LEARNING STRATEGY

# LONG TERM:
# TODO: BETTER GRAPHICS


class Environment():
    """class to manage which objects are present and render their positions"""
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = np.zeros((width, height))

        self.win = Tk()
        self.win.geometry("750x270")
        self.grid_str = StringVar()
        self.grid_str.set(pretty_matrix(self.grid))
        self.font = ('Helvetica 14 bold')
        self.padding = 20

        self.current_step = "INIT"
        self.label_str = StringVar()
        self.label_str.set(str(self.current_step))

        self.wipe_canvas()
        self.objects = []

        self.label = Label(self.win, textvariable=self.grid_str, font=self.font).pack(pady=self.padding)


        self.label = Label(self.win, textvariable=self.label_str, font=self.font).pack(pady=self.padding)
        self.update_display()
        self.time_step = 0.01
        self.rewards = []


    def update_display(self, str_overide: Union[str, bool] = False) -> None:
        """Update the display with the current value of self.grid"""
        self.grid_str.set(pretty_matrix(self.grid))
        if not str_overide:
            self.label_str.set(str(self.current_step))
        else:
            self.label_str.set(str_overide)
        self.win.update()


    def wipe_canvas(self) -> None:
        """Set self.grid to all 0's"""
        self.grid = np.zeros((self.width, self.height))
        self.update_display()

    def simulate(self, num_steps: int) -> None:
        """Progress the simulation for num_steps"""

        time.sleep(self.time_step)

        current_reward = 0
        time.sleep(3)
        for step in range(num_steps):
            if not current_reward:
                self.current_step = step
                self.wipe_canvas()
                print(f"STEP {step}")
                self.step_objects()
                current_reward = self.get_reward()
                self.rewards += [current_reward]
                self.update_display()
                time.sleep(self.time_step)

            # TODO: make seperate end game signal from the reward signal
            else:
                self.update_display(str_overide="WIN")

        if not current_reward:
            self.update_display(str_overide="LOSE")
        time.sleep(5)


    def step_objects(self) -> None:
        """make each object in the env carry out their step action"""
        for obj in self.objects:
            obj.step(self)
            self.draw_object(obj)


    def draw_object(self, obj: 'Object') -> None:
        """Update the grid with the object's symbol"""
        self.grid[obj.y, obj.x] = obj.symbol
        self.win.update()

    def add_object(self, obj: 'Object') -> None:
        """Add a new object to the env and initialise some of its properties"""
        if obj not in self.objects:
            if not obj.is_target:
                self.objects.append(obj)
            else:
                self.objects.insert(0, obj)
            self.draw_object(obj)
            self.update_display()

    def get_reward(self):
        """get the reward for the actor in the environment"""
        target = [o for o in self.objects if o.is_target]
        if target:
            target = target[0]
            if any([o.x == target.x and o.y == target.y and not o.is_target for o in self.objects]):
                return 1
        return 0


class Object():
    """Parent class for any object in the environment"""
    def __init__(self, x_initial: int, y_initial:int, symbol: int = EMPTY_SYMBOL) -> None:
        self.symbol = symbol
        self.x = x_initial
        self.y = y_initial
        self.last_x = copy(x_initial)
        self.last_y = copy(y_initial)
        self.is_target = False
        self.passable = False

    def occupies_space(self, x: int, y: int) -> bool:
        """determine wether this object blocks access to a specific location on the grid"""
        if x == self.x and y == self.y and not self.passable:
            return True

        return False

class Actor(Object):
    """Object child class that carries out actions in the environment"""
    def __init__(self, x_initial: int, y_initial: int, symbol = ACTOR_SYMBOL):
        Object.__init__(self, x_initial, y_initial, symbol)

    def step_right(self, env: Type[Environment]) -> (int, int):
        """actor moves one unit to the right on loop"""
        if self.x < env.width-1:
            self.x += 1
        return self.x, self.y

    def step(self, env: Type[Environment]) -> (int, int):
        """allow actor to take an action"""
        #self.step_right(env)
        self.random_step(env)

    def random_step(self, env: 'Environment') -> (int, int):
        """move in a random valid direction"""
        all_valid_moves = self.valid_moves(env)
        (self.x, self.y) = all_valid_moves[np.random.choice(range(len(all_valid_moves)))]
        return self.x, self.y


    def valid_moves(self, env: 'Environment') -> [(int, int)]:
        """"""
        valid_next_positions = []
        valid_next_positions.append((self.x, self.y))
        for potential_x in range(self.x-1, self.x+2):
            for potential_y in range(self.y-1, self.y+2):
                if not 0 <= potential_x < env.width:
                    continue
                if not 0 <= potential_y < env.height:
                    continue
                if any([o.occupies_space(potential_x, potential_y) for o in env.objects]):
                    continue

                if abs(potential_x-self.x) + abs(potential_y-self.y) > 1:
                    continue

                valid_next_positions.append((potential_x, potential_y))

        return valid_next_positions


class Target(Object):
    """Class for the location the actor aims to reach"""
    def __init__(self, x_initial: int, y_initial: int) -> None:
        Object.__init__(self,  x_initial, y_initial, symbol = TARGET_SYMBOL)
        self.is_target = True
        self.passable = True

    def step(self, env: 'Environment') -> (int, int):
        """(null) action this Object instance should carry out each step"""
        return self.null_step(env)

    def null_step(self, env: 'Environment') -> (int, int):
        """carry out a null step"""
        return self.x, self.y




if __name__ == '__main__':
    #example_window()

    print("Running")

    env_width = 6
    env_height = 6
    env = Environment(env_width, env_height)

    x_initial = 0
    y_initial = 0
    obj_1 = Actor(x_initial, y_initial)

    env.add_object(obj_1)

    target_x_initial = env_width - 1
    target_y_initial = env_height - 1

    target = Target(target_x_initial, target_y_initial)

    env.add_object(target)

    num_simulation_steps = 1000

    env.simulate(num_simulation_steps)

