from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from .portraycell import agent_portrayal  
from .model import FarmModel  
from mesa.visualization.UserParam import Choice, Slider
GRID_WIDTH = 20
GRID_HEIGHT = 20

grid = CanvasGrid(agent_portrayal, GRID_WIDTH, GRID_HEIGHT, 500, 500)

mode_selector = Choice(name="choice", value="Basic", choices=["Basic", "Extended","Systematic"])
num_drones_slider = Slider(name="num_drones", value=2, min_value=1, max_value=10, step=1)
num_pickers_slider = Slider(name="num_pickers", value=3, min_value=1, max_value=10, step=1)


server = ModularServer(
    FarmModel,
    [grid],
    "Farm Simulation",
    {
        "num_drones": num_drones_slider,
        "num_pickers": num_pickers_slider,
        "num_clusters": 5,
        "extended_mode": mode_selector
    }
)


server.launch()


