from mesa import Agent
import random
# Constants
GRID_WIDTH = 20
GRID_HEIGHT = 20
BATTERY_CAPACITY = 100
STORAGE_CAPACITY = 5


class BaseDroneAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.battery = BATTERY_CAPACITY
        self.state = "Exploring"  # Possible states: Exploring, Waiting, Returning

    def step(self):
        if self.battery <= 0:
            self.state = "Returning"

        if self.state == "Waiting":
            self.check_strawberry_status()
        elif self.state == "Exploring":
            self.explore()
        elif self.state == "Returning":
            self.return_to_base()

    def check_strawberry_status(self):
        """
        Check if the strawberry cluster at the current location has been picked.
        If it has, transition back to 'Exploring'.
        """
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        strawberry_present = any(isinstance(obj, BaseStrawberryCluster) for obj in cell_contents)
        if not strawberry_present:
            self.state = "Exploring"  # Resume exploring once the strawberry is gone

    def explore(self):
        """
        Randomly explore the grid and look for strawberry clusters.
        Transition to 'Waiting' if a cluster is found.
        """
        self.move_randomly()
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell_contents:
            if isinstance(obj, BaseStrawberryCluster):
                self.target_location = self.pos
                self.state = "Waiting"  # Switch to waiting when a cluster is found
                return  

        # Decrease battery while exploring
        self.battery -= 1

    def return_to_base(self):
        # Move towards the base station or charging point
        charging_station_pos = (1, 0)
        self.move_towards(charging_station_pos)
        if self.pos == charging_station_pos:
            self.battery = BATTERY_CAPACITY  # Recharge battery
            self.state = "Exploring"

    def move_randomly(self):
        """
        Move to a random adjacent cell.
        """
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def move_towards(self, target):
        """
        Move one step closer to the target position.
        """
        x, y = self.pos
        tx, ty = target
        new_position = (x + (1 if x < tx else -1 if x > tx else 0),
                        y + (1 if y < ty else -1 if y > ty else 0))
        self.model.grid.move_agent(self, new_position)

class BasePickerRobotAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.battery = BATTERY_CAPACITY
        self.storage = 0
        self.state = "Idle"  # Possible states: Idle, Moving, Picking, Returning
        self.target_location = None

    def step(self):
        if self.battery <= 0 or self.storage >= STORAGE_CAPACITY:
            self.state = "Returning"

        if self.state == "Idle":
            self.move_randomly()

        elif self.state == "Moving" and self.target_location:
            self.move_towards(self.target_location)
            if self.pos == self.target_location:
                self.state = "Picking"

        elif self.state == "Picking":
            self.pick_strawberries()

        elif self.state == "Returning":
            self.return_to_base()

    def receive_location(self, location):
        """
        Assign a target location only if the robot is idle.
        """
        if self.state == "Idle":
            self.target_location = location
            self.state = "Moving"

    def move_randomly(self):
        """Move to a random adjacent cell."""
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.battery -= 1

    def pick_strawberries(self):
        """Pick strawberries at the current location."""
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell_contents:
            if isinstance(obj, BaseStrawberryCluster) and obj.is_grown:
                self.storage += 1
                obj.is_grown = False  # Mark as picked
                obj.picked = True  # Update the picked flag
                obj.age = 0  # Reset age if using regrowth

                if self.storage >= STORAGE_CAPACITY:
                    self.state = "Returning"
                else:
                    self.state = "Idle"  # Ready to pick again
                break  # Pick only one strawberry per step

        # Decrease battery for the action
        self.battery -= 1


    def return_to_base(self):
        """Move towards the base station or charging point."""
        charging_station_pos = (0, 0)
        self.move_towards(charging_station_pos)
        if self.pos == charging_station_pos:
            self.battery = BATTERY_CAPACITY
            self.storage = 0
            self.state = "Idle"

    def move_towards(self, target):
        """Move one step closer to the target position."""
        x, y = self.pos
        tx, ty = target
        new_position = (x + (1 if x < tx else -1 if x > tx else 0),
                        y + (1 if y < ty else -1 if y > ty else 0))
        self.model.grid.move_agent(self, new_position)

class BaseStrawberryCluster(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.age = 0
        self.max_age = 10  # Fully grown at 10
        self.is_grown = True
        self.picked = False  # To track if the strawberry has been picked

def step(self):
    pass

def __str__(self):
    return f"StrawberryCluster(unique_id={self.unique_id}, age={self.age}, is_grown={self.is_grown}, picked={self.picked})"
class BasicDroneAgent(BaseDroneAgent):
    def step(self):
        if self.battery <= 0:
            self.state = "Returning"

        if self.state == "Waiting":
            self.check_strawberry_status()
        elif self.state == "Exploring":
            self.explore()
        elif self.state == "Returning":
            self.return_to_base()

    def explore(self):
        """
        Randomly explore the grid and look for strawberry clusters.
        Transition to 'Waiting' if a cluster is found.
        """
        self.move_randomly()
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell_contents:
            if isinstance(obj, BasicStrawberryCluster) and obj.is_grown:
                self.target_location = self.pos
                self.state = "Waiting"  # Switch to waiting when a cluster is found
                return  # Stop further actions in this step

        # Decrease battery while exploring
        self.battery -= 1

    def check_strawberry_status(self):
        """
        Check if the strawberry cluster at the current location has been picked.
        If it has, transition back to 'Exploring'.
        """
        cell_contents = self.model.grid.get_cell_list_contents([self.target_location])
        strawberry_present = any(isinstance(obj, BasicStrawberryCluster) and obj.is_grown for obj in cell_contents)

        if not strawberry_present:
            self.state = "Exploring"  # Resume exploring once the strawberry is gone


class BasicPickerRobotAgent(BasePickerRobotAgent):
    def step(self):
        if self.battery <= 0 or self.storage >= STORAGE_CAPACITY:
            self.state = "Returning"

        if self.state == "Idle":
            self.move_randomly()

        elif self.state == "Returning":
            self.return_to_base()

        # Check for strawberries to pick when idle or after moving
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell_contents:
            if isinstance(obj, BasicStrawberryCluster) and obj.is_grown:
                self.pick_strawberries(obj)
                break  # Pick only one strawberry per step

    def pick_strawberries(self, strawberry):
        """Pick a strawberry at the current location."""
        if strawberry.is_grown:
            self.storage += 1
            strawberry.is_grown = False  # Mark the strawberry as picked
            strawberry.picked = True  # Update picked status
            strawberry.age = 0  # Reset age if regrowth is enabled

            # Check if the robot's storage is full
            if self.storage >= STORAGE_CAPACITY:
                self.state = "Returning"
            else:
                self.state = "Idle"

        # Decrease battery after picking
        self.battery -= 1

class BasicStrawberryCluster(BaseStrawberryCluster):
    def step(self):
        if self.picked:
            self.is_grown = False  # Ensure it doesn't grow in basic mode
class ExtendedDroneAgent(BaseDroneAgent):
        

    def step(self):
        if self.battery <= 0:
            self.state = "Returning"

        if self.state == "Waiting":
            self.check_strawberry_status()
        elif self.state == "Exploring":
            self.explore()
        elif self.state == "Returning":
            self.return_to_base()

    def explore(self):
        """
        Randomly explore the grid and look for strawberry clusters.
        Transition to 'Waiting' if a cluster is found.
        """
        self.move_randomly()
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell_contents:
            if isinstance(obj, ExtendedStrawberryCluster) and obj.is_grown:
                self.model.broadcast_location(self.pos)
                self.target_location = self.pos
                self.state = "Waiting"  # Switch to waiting when a cluster is found
                return  # Stop further actions in this step

        # Decrease battery while exploring
        self.battery -= 1
        
    def check_strawberry_status(self):
        """
        Check if the strawberry cluster at the current location has been picked.
        If it has, transition back to 'Exploring'.
        """
        if not self.target_location:
            self.state = "Exploring"  # No target, go back to exploring
            

        cell_contents = self.model.grid.get_cell_list_contents([self.target_location])
        strawberry_present = any(isinstance(obj, ExtendedStrawberryCluster) and obj.is_grown for obj in cell_contents)

        if not strawberry_present:
            self.state = "Exploring"  # Resume exploring once the strawberry is gone
            return

class ExtendedPickerRobotAgent(BasePickerRobotAgent):
    def step(self):
        if self.battery <= 0 or self.storage >= STORAGE_CAPACITY:
            self.state = "Returning"

        if self.state == "Idle":
            pass  # Wait for a signal from the drone

        elif self.state == "Moving" and self.target_location:
            self.move_towards(self.target_location)
            if self.pos == self.target_location:
                self.state = "Picking"

        elif self.state == "Picking":
            self.pick_strawberries()

        elif self.state == "Returning":
            self.return_to_base()

    def pick_strawberries(self):
        """Pick strawberries at the current location."""
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell_contents:
            if isinstance(obj, ExtendedStrawberryCluster) and obj.is_grown:
                self.storage += 1
                obj.is_grown = False  # Mark as picked
                obj.age = 0  # Reset age
                obj.picked = True  # Mark as picked

                if self.storage >= STORAGE_CAPACITY:
                    self.state = "Returning"
                else:
                    self.move_outside_tree()  # Move away from the tree to wait
                break  # Pick only one cluster per step

        self.battery -= 1

    def move_outside_tree(self):
        """Move to a random adjacent cell away from the tree and wait for the drone signal."""
        # Get all neighboring cells
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        
        # Filter out any cells that contain a tree (assuming Tree is the class for trees)
        valid_steps = [
            step for step in possible_steps
            if not any(isinstance(obj, Tree) for obj in self.model.grid.get_cell_list_contents([step]))
        ]
        
        if valid_steps:  # If there are valid steps, choose one randomly
            new_position = random.choice(valid_steps)
            self.model.grid.move_agent(self, new_position)
            self.state = "Idle"  # Change to idle state after moving





class ExtendedStrawberryCluster(BaseStrawberryCluster):
    def __init__(self, model, pos, max_age=50):
        super().__init__(model, pos)
        self.regrowth_timer = 0  # Timer to track regrowth after being picked
        self.max_age = max_age
    def step(self):
        print(f"Strawberry at {self.pos}: is_grown={self.is_grown}, picked={self.picked}, regrowth_timer={self.regrowth_timer}")
        if not self.is_grown:
            self.age += 1
            if self.age >= self.max_age:
                self.is_grown = True
                self.picked = False  # Reset picked status when regrown
                self.regrowth_timer = 0  # Reset regrowth timer once it regrows
        else:
            # If the strawberry has been picked, increment the regrowth timer
            if self.picked:
                self.regrowth_timer += 1
                if self.regrowth_timer >= 50:  # After 10 steps, it regrows
                    self.is_grown = True  # Regrow the strawberry
                    self.picked = False  # Mark it as not picked
                    self.regrowth_timer = 0  # Reset the timer
            # Ensure the strawberry is marked as ready to be picked again
        if self.is_grown and not self.picked:
            self.picked = False  # Ensure it's marked as not picked

            
class SystematicDroneAgent(BaseDroneAgent):
    def step(self):
        if self.battery <= 0:
            self.state = "Returning"

        if self.state == "Waiting":
            self.check_strawberry_status()
        elif self.state == "Exploring":
            self.explore()
        elif self.state == "Returning":
            self.return_to_base()

    def explore(self):
        """
        Systematically explore the grid and look for strawberry clusters.
        Transition to 'Waiting' if a cluster is found.
        """
        if not hasattr(self, 'exploration_path'):
            self.initialize_exploration_path()

        # Move to the next position in the exploration path
        if self.exploration_path:
            next_position = self.exploration_path.pop(0)
            self.model.grid.move_agent(self, next_position)
            print(f"Drone moving to {next_position}")  # Debug print

        # Check the current cell for strawberry clusters
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        print(f"Drone at {self.pos}, cell contents: {cell_contents}")  # Debug print
        for obj in cell_contents:
            if isinstance(obj, SystematicStrawberryCluster) and obj.is_grown:
                print(f"Strawberry cluster found at {self.pos}")  # Debug print
                self.model.broadcast_location(self.pos)
                self.target_location = self.pos
                self.state = "Waiting"  # Switch to waiting when a cluster is found
                return  # Stop further actions in this step

        # Decrease battery while exploring
        self.battery -= 1

    def initialize_exploration_path(self):
        """
        Initialize a systematic exploration path for the drone.
        Ensure that no column or row is revisited unnecessarily.
        """
        self.exploration_path = []

        grid_width = self.model.grid.width
        grid_height = self.model.grid.height

        if self.unique_id % 2 == 0:  # Alternate drones
            # Row-by-row traversal
            for y in range(grid_height):
                if y % 2 == 0:  # Even rows (left to right)
                    for x in range(grid_width):
                        self.exploration_path.append((x, y))
                else:  # Odd rows (right to left)
                    for x in reversed(range(grid_width)):
                        self.exploration_path.append((x, y))
        else:
            # Column-by-column traversal
            for x in range(grid_width):
                if x % 2 == 0:  # Even columns (top to bottom)
                    for y in range(grid_height):
                        self.exploration_path.append((x, y))
                else:  # Odd columns (bottom to top)
                    for y in reversed(range(grid_height)):
                        self.exploration_path.append((x, y))

        print(f"Exploration path initialized: {self.exploration_path}")  # Debug print
    def check_strawberry_status(self):
        """
        Check if the strawberry cluster at the current location has been picked.
        If it has, transition back to 'Exploring'.
        If it is present, share the location with the nearest picker.
        """
        if not self.target_location:
            self.state = "Exploring"  # No target, go back to exploring
            return

        cell_contents = self.model.grid.get_cell_list_contents([self.target_location])
        strawberry_present = any(isinstance(obj, SystematicStrawberryCluster) and obj.is_grown for obj in cell_contents)

        if not strawberry_present:
            self.state = "Exploring"  # Resume exploring once the strawberry is gone.
        else:
            # Share the location with the nearest picker
            nearest_picker = None
            min_distance = float('inf')

            for agent in self.model.schedule.agents:
                if isinstance(agent, SystematicPickerRobotAgent):  # Assuming PickerAgent class exists
                    distance = self.calculate_distance(self.target_location, agent.pos)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_picker = agent

            if nearest_picker:
                nearest_picker.receive_target_location(self.target_location)  # Share location
                print(f"Shared strawberry location {self.target_location} with Picker {nearest_picker.unique_id}")

    def calculate_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


    

    

class SystematicPickerRobotAgent(BasePickerRobotAgent):
    def step(self):
        """
        Define the behavior of the picker agent at each simulation step.
        """
        # Check battery and storage status
        if self.battery <= 0 or self.storage >= STORAGE_CAPACITY:
            self.state = "Returning"

        if self.state == "Idle":
            # Respond to a drone signal if a target location is provided
            if self.target_location:
                self.state = "Moving"  # Transition to moving state
                print(f"Picker {self.unique_id} received a signal to move to {self.target_location}")

        elif self.state == "Moving" and self.target_location:
            # Move towards the target location
            self.move_towards(self.target_location)
            if self.pos == self.target_location:
                self.state = "Picking"  # Transition to picking state

        elif self.state == "Picking":
            # Perform the strawberry picking operation
            self.pick_strawberries()
            if self.storage >= STORAGE_CAPACITY:
                self.state = "Returning"  # Transition to returning if storage is full
            else:
                self.state = "Idle"  # Ready for the next signal

        elif self.state == "Returning":
            # Return to the base and handle necessary actions (e.g., offloading)
            self.return_to_base()

        # Debug information
        print(f"Picker {self.unique_id} is in state: {self.state}")

    def receive_target_location(self, location):
        self.target_location = location

    def pick_strawberries(self):
        """Pick strawberries at the current location."""
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell_contents:
            if isinstance(obj, SystematicStrawberryCluster) and obj.is_grown:
                self.storage += 1
                obj.is_grown = False  # Mark as picked
                obj.age = 0  # Reset age
                obj.picked = True  # Mark as picked

                if self.storage >= STORAGE_CAPACITY:
                    self.state = "Returning"
                else:
                    self.move_outside_tree()  # Move away from the tree to wait
                break  # Pick only one cluster per step

        self.battery -= 1

    def move_outside_tree(self):
        """Move to a random adjacent cell away from the tree and wait for the drone signal."""
        # Get all neighboring cells
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        
        # Filter out any cells that contain a tree (assuming Tree is the class for trees)
        valid_steps = [
            step for step in possible_steps
            if not any(isinstance(obj, Tree) for obj in self.model.grid.get_cell_list_contents([step]))
        ]
        
        if valid_steps:  # If there are valid steps, choose one randomly
            new_position = random.choice(valid_steps)
            self.model.grid.move_agent(self, new_position)
            self.state = "Idle"  # Change to idle state after moving


class SystematicStrawberryCluster(BaseStrawberryCluster):
    def __init__(self, model, pos, max_age=50):
        super().__init__(model, pos)
        self.regrowth_timer = 0  # Timer to track regrowth after being picked
        self.max_age = max_age
    def step(self):
        print(f"Strawberry at {self.pos}: is_grown={self.is_grown}, picked={self.picked}, regrowth_timer={self.regrowth_timer}")
        if not self.is_grown:
            self.age += 1
            if self.age >= self.max_age:
                self.is_grown = True
                self.picked = False  # Reset picked status when regrown
                self.regrowth_timer = 0  # Reset regrowth timer once it regrows
        else:
            # If the strawberry has been picked, increment the regrowth timer
            if self.picked:
                self.regrowth_timer += 1
                if self.regrowth_timer >= 50:  # After 50 steps, it regrows
                    self.is_grown = True  # Regrow the strawberry
                    self.picked = False  # Mark it as not picked
                    self.regrowth_timer = 0  # Reset the timer
            # Ensure the strawberry is marked as ready to be picked again
        if self.is_grown and not self.picked:
            self.picked = False  # Ensure it's marked as not picked

class Tree(Agent):
    def __init__(self, unique_id, model, picked=False):
        super().__init__(unique_id, model)
        self.picked = picked  # If true, the tree turns green after strawberry is picked

class River(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class ChargingStation(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)