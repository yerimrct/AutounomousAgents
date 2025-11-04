# AutounomousAgents


# 🍓 Autonomous Agent Multi-Agent System: Farm Simulation

[cite_start]**Project by: YERIM MOHAMED (21052002)** [cite: 2]

[cite_start]This project implements and evaluates a **Multi-Agent System (MAS)** for an automated farm simulation, focusing on the efficient harvesting of crops (strawberries) using **Drones** and **Picker Robots**[cite: 1, 7, 8]. The simulation explores increasing complexity from a basic random movement model to a coordinated, communication-based extended model.

---

## 👨‍💻 Activity 1: Basic Mode Objectives

[cite_start]The initial activity defines the core autonomous behavior and state-based logic for the agents[cite: 3, 4, 5].

### [cite_start]Statecharts of the Agents [cite: 6]

The agents operate based on distinct statecharts to manage their tasks:

#### Picker Agent Statechart
| State | Transition | New State | Condition |
| :--- | :--- | :--- | :--- |
| `Idle` | Move randomly | `Moving` | - |
| `Moving` | Strawberry found | `Picking` | - |
| `Moving` | Battery low | `returning` | - |
| `Picking` | Storage full | `returning` | - |
| `returning` | Go back to move | `Moving` | - |

#### Drone Agent Statechart
| State | Transition | New State | Condition |
| :--- | :--- | :--- | :--- |
| `Waiting` | Start/Strawberry collected | `Exploring` | - |
| `Exploring` | Strawberry found | `Waiting` | - |
| `Exploring` | Battery low | `returning` | - |
| `returning` | battery full | `Exploring` | - |

---

## 🚀 Activity 3: Extended Operation

[cite_start]This activity introduces communication and environmental complexity to improve system efficiency[cite: 21, 22].

### [cite_start]Extended Model Features [cite: 23, 24, 25, 26]
* [cite_start]**Coordinated Movement**: Picker robots only leave the station once the drone sends a signal with coordinates of where the crops need to be collected, avoiding random movement of picker robots[cite: 23].
* [cite_start]**Flexible Communication**: The drone can send messages to individual robots or broadcast the location of the crops to all the robots[cite: 24].
* [cite_start]**Dynamic Environment**: Crops age and grow as the simulation progresses[cite: 25]. [cite_start]Once an area has been fully picked, new seeds are grown, re-starting the ageing cycle[cite: 25]. [cite_start]The Environment handles the ageing and re-growing of strawberries[cite: 26].

### [cite_start]Extended Model KPI Analysis (at ~100 Steps) [cite: 28]

* [cite_start]Total Strawberries Picked: **5.00** [cite: 28]
* [cite_start]Total Energy Consumed: **406.00** [cite: 28]
* [cite_start]Average Strawberries Picked per Agent: **1.6** [cite: 28]

---

## 📈 Activity 4: Comparison of Novel and Extended Mode

[cite_start]This final activity compares the **Extended Model** against a **Systematic Model** (referred to as the "novel mode" in the slides) over 500 steps[cite: 34, 36].

### [cite_start]Key Performance Indicators (KPIs) Defined [cite: 29, 30, 32]
* [cite_start]**Efficiency of Exploration**: Measures the ability to locate strawberries effectively over time[cite: 29].
* [cite_start]**Energy Consumption**: Evaluates the energy usage efficiency of the drones and picker robots[cite: 30].
* [cite_start]**Average Strawberries Picked per Agent**: Measures the average number of strawberries picked by each picker robot[cite: 32].

### [cite_start]Performance Comparison (Extended vs. Systematic) [cite: 36, 37]

| Metric | Extended Model | Systematic Model | Comparison Finding |
| :--- | :--- | :--- | :--- |
| **Total Strawberries Picked** | 9.00 | 8.00 | Extended Model is slightly better. |
| **Total Energy Consumed** | 280.00 | 395.00 | **Extended Model consumes significantly less energy.** |
| **Avg. Strawberries Picked per Agent**| 3.00 | 2.67 | [cite_start]Mostly equal[cite: 37], with a slight edge to Extended. |
| **Efficiency of Exploration** | N/A | N/A | [cite_start]The novel mode is **not more efficient** than the extended mode[cite: 36]. |
| **Average Battery Level** | N/A | N/A | [cite_start]Mostly equal[cite: 37]. |

### Visual Results

[cite_start]The performance plots for the comparison are shown below:  [cite: 35, 37]

---

## ✅ Testing

[cite_start]Unit tests were executed to ensure functionality: [cite: 9]

```bash
Ran 10 tests in 0.004s
OK
