import unittest
from unittest.mock import MagicMock
from agent import BasicPickerRobotAgent, BasicDroneAgent, BasicStrawberryCluster

STORAGE_CAPACITY = 5  # Define the storage capacity

class TestBasicPickerRobotAgent(unittest.TestCase):
    def setUp(self):
        self.model = MagicMock()
        self.picker = BasicPickerRobotAgent(0, self.model)
        self.picker.battery = 10
        self.picker.storage = 0
        self.picker.state = "Idle"
        self.picker.pos = (0, 0)


    def test_step_idle_to_moving(self):
        self.picker.state = "Idle"
        self.picker.move_randomly = MagicMock()
        self.picker.step()
        self.picker.move_randomly.assert_called_once()

    def test_step_returning_to_base(self):
        self.picker.state = "Returning"
        self.picker.return_to_base = MagicMock()
        self.picker.step()
        self.picker.return_to_base.assert_called_once()

    def test_pick_strawberries(self):
        strawberry = MagicMock()
        strawberry.is_grown = True
        self.picker.pick_strawberries(strawberry)
        self.assertEqual(self.picker.storage, 1)
        self.assertEqual(strawberry.is_grown, False)
        self.assertEqual(strawberry.picked, True)
        self.assertEqual(strawberry.age, 0)
        self.assertEqual(self.picker.battery, 9)

    def test_pick_strawberries_storage_full(self):
        self.picker.storage = STORAGE_CAPACITY - 1
        strawberry = MagicMock()
        strawberry.is_grown = True
        self.picker.pick_strawberries(strawberry)
        self.assertEqual(self.picker.state, "Returning")
        
class TestBasicStrawberryCluster(unittest.TestCase):
    def setUp(self):
        self.model = MagicMock()
        self.strawberry = BasicStrawberryCluster(0, self.model)
        self.strawberry.is_grown = True
        self.strawberry.picked = False

    def test_step_picked(self):
        self.strawberry.picked = True
        self.strawberry.step()
        self.assertEqual(self.strawberry.is_grown, False)

    def test_step_not_picked(self):
        self.strawberry.picked = False
        self.strawberry.step()
        self.assertEqual(self.strawberry.is_grown, True)

class TestBasicDroneAgent(unittest.TestCase):
    def setUp(self):
        self.model = MagicMock()
        self.drone = BasicDroneAgent(0, self.model)
        self.drone.battery = 10
        self.drone.state = "Waiting"
        self.drone.pos = (0, 0)

    def test_step_returning_when_battery_low(self):
        self.drone.battery = 0
        self.drone.step()
        self.assertEqual(self.drone.state, "Returning")

    def test_step_waiting_to_exploring(self):
        self.drone.state = "Waiting"
        self.drone.check_strawberry_status = MagicMock()
        self.drone.step()
        self.drone.check_strawberry_status.assert_called_once()

    def test_step_exploring_to_waiting(self):
        self.drone.state = "Exploring"
        self.drone.explore = MagicMock()
        self.drone.step()
        self.drone.explore.assert_called_once()

    def test_step_returning_to_base(self):
        self.drone.state = "Returning"
        self.drone.return_to_base = MagicMock()
        self.drone.step()
        self.drone.return_to_base.assert_called_once()

    

   
    
    

if __name__ == '__main__':
    unittest.main()