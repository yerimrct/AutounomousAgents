from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import random

# Constants
GRID_WIDTH = 20
GRID_HEIGHT = 20
BATTERY_CAPACITY = 100
STORAGE_CAPACITY = 5
from .agent import Tree,BasicDroneAgent,BasicPickerRobotAgent, BasicStrawberryCluster, River, BasicStrawberryCluster,ExtendedDroneAgent,ExtendedPickerRobotAgent,ExtendedStrawberryCluster,ChargingStation,SystematicDroneAgent,SystematicPickerRobotAgent,SystematicStrawberryCluster

class FarmModel(Model):
    def __init__(self, num_drones, num_pickers, num_clusters,extended_mode= "Extended"):
        self.grid = MultiGrid(GRID_WIDTH, GRID_HEIGHT, torus=False)
        self.schedule = RandomActivation(self)
        self.systematic_mode = extended_mode == 'Systematic'
        self.extended_mode = extended_mode == 'Extended'
        
        self.drones = []
       
            
        # Base station location
        self.base_station = (0, 0)

        # Create agents
        DroneAgent = ExtendedDroneAgent if self.extended_mode else (SystematicDroneAgent if self.systematic_mode else BasicDroneAgent)
        PickerRobotAgent = ExtendedPickerRobotAgent if self.extended_mode else SystematicPickerRobotAgent if self.systematic_mode else BasicPickerRobotAgent
        StrawberryCluster = ExtendedStrawberryCluster if self.extended_mode else SystematicStrawberryCluster if self.systematic_mode else BasicStrawberryCluster
        print(f"Using DroneAgent: {DroneAgent.__name__}")
        print(f"Using PickerRobotAgent: {PickerRobotAgent.__name__}")
        print(f"Using StrawberryCluster: {StrawberryCluster.__name__}")

        for i in range(num_drones):
            drone = DroneAgent(i, self)
            self.grid.place_agent(drone, self.base_station)
            
            self.schedule.add(drone)

        for i in range(num_drones, num_drones + num_pickers):
            picker = PickerRobotAgent(i, self)
            self.grid.place_agent(picker, self.base_station)
            self.schedule.add(picker)

        # Place the charging station near the base station
        charging_station = ChargingStation(num_drones + num_pickers + num_clusters, self)
        self.grid.place_agent(charging_station, (0, 0))

        # Place trees and strawberries together in rows
        tree_id = num_drones + num_pickers
        river_x2 = tree_id

        bottom_row = GRID_HEIGHT - 1 # Leave space at the top and bottom

        for x in range(2, GRID_WIDTH, 3):  
            for y in range(bottom_row, 1, -1):  # Start from the bottom row and go upwards
                if y == bottom_row or y == 1:  # Add extra space at the top and bottom
                    continue

                tree = Tree(tree_id, self)
                self.grid.place_agent(tree, (x, y))
                tree_id += 1

                if random.random() < 0.5:  # 50% chance to place a strawberry
                    cluster = StrawberryCluster(tree_id, self)
                    self.grid.place_agent(cluster, (x, y))
                    self.schedule.add(cluster)
                    tree_id += 1

            # Adjust the column position for the next set of trees to create a gap between columns
            # Move the x-coordinate for the next set of trees to create the gap between columns
            x += 4

        # Place river in the middle of the grid
        river_id = tree_id
        river_x1 = GRID_WIDTH // 2  # First column of the river
        river_x2 = river_x1 + 1     # Second column of the river
    

        for y in range(GRID_HEIGHT):
            river1 = River(river_id, self)
            self.grid.place_agent(river1, (river_x1, y))
            river_id += 1

            river2 = River(river_id, self)
            self.grid.place_agent(river2, (river_x2, y))
            river_id += 1
            
        


    def broadcast_location(self, location):
        """
        Send location to only one picker robot in extended mode.
        """
        for agent in self.schedule.agents:
            if isinstance(agent, ExtendedPickerRobotAgent) and agent.state == "Idle":
                agent.receive_location(location)
                break  # Only send to one robot
            elif self.systematic_mode and isinstance(agent, SystematicPickerRobotAgent) and agent.state == "Idle":
                agent.receive_location(location)
                break  # Only send to one robot
            
    

    def step(self):
        self.schedule.step()


