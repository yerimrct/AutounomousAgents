

from .agent import Tree,BaseDroneAgent,BasePickerRobotAgent, BaseStrawberryCluster, River,ChargingStation
from .model import FarmModel

GRID_WIDTH = 20
GRID_HEIGHT = 20
BATTERY_CAPACITY = 100
STORAGE_CAPACITY = 5



def agent_portrayal(agent):
    if isinstance(agent, BaseDroneAgent):
        color = "green" if agent.state == "Exploring" else "orange"
        return {"Shape": "circle", "Color": "blue", "Filled": True, "Layer": 1, "r": 0.5}
    elif isinstance(agent, BasePickerRobotAgent):
        color = "yellow" if agent.storage >= STORAGE_CAPACITY else "grey"
        return {"Shape": "circle", "Color": color, "Filled": True, "Layer": 1, "r": 0.5}
    elif isinstance(agent, BaseStrawberryCluster,):
        color = "lightgreen" if agent.picked else "pink"
        return {"Shape": "rect", "Color": color, "Filled": True, "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, Tree):
        color = "lightgreen" if agent.picked else "green"
        return {"Shape": "rect", "Color": color, "Filled": True, "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, River):
        return {"Shape": "rect", "Color": "blue", "Filled": True, "Layer": 0, "w": 1.0, "h": 1.0}
    elif isinstance(agent, ChargingStation):
        return {"Shape": "rect", "Color": "black", "Filled": True, "Layer": 0, "w": 1.0, "h": 1.0}
    




