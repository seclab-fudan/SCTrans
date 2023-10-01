# Scenario Runner

This directory is dedicated to the refined versions of the **LGSVL** & **Carla** scenario runners. It contains the complete, modified source code along with comprehensive usage instructions. Recognizing the unique requirements and challenges of diverse driving scenarios, we have meticulously modified the official Scenario Runner to ensure superior compatibility and adaptability with our extensive range of scenarios.

## LGSVL Scenario Runner
Located in `lgvsl-runner/` directory

### Modifications
- Integrated the reading and setting of weather and time configurations into the run_vse script, eliminating the need to set them from the website UI.
- Added a collision check function to print information when a collision occurs.
- Added a bridge connect function for Apollo & LGSVL co-simulation tests.

### Environment Setup
The official LGSVL simulator development has been suspended, and the wise.svlsimulator.com website is also no longer running. We recommend referring to our modified Local version LGSVL simulator: [LGSVL Local Version](https://github.com/emocat/simulator/tree/release-2021.2), which can run a simulation entirely locally. Please follow the usage tutorial. P.S. If you like this repo, do not forget to give this project a star! Thanks a lot.

### Quick Start
For a single scenario simulation, two files are required: 
- **Scenario file**: `YOUR_SCENARIO_FILE_NAME.json`
- **Scenario map**: `environment_xxx`

Before running a scenario, you must add the map asset locally: [add asset](https://github.com/emocat/simulator/tree/release-2021.2#how-to-add-an-asset-locally)

You can use the following command to run a scenario in the LGSVL Simulator:
```
python3 run_vse_test.py YOUR_SCENARIO_FILE_NAME.json
```

## Carla Scenario Setup
Located in `carla-runner/` directory 

### Modifications
- Added a waypoint controller for running waypoint behavior NPC. The controller uses pure pursuit for lateral control and PID for longitudinal control. 

- Updated to use OpenSCENARIOv1.2.xsd instead of OpenSCENARIO.xsd for schema verification.

- Changed the setting of wall height to zero.

### Environment Setup
1) Install Carla-0.9.13

    Download Carla release from https://github.com/carla-simulator/carla/releases/tag/0.9.13

2) Install scenario runner
    
    Download from the `carla-runner/` directory

### Quick Start
For a single scenario simulation, two files are required: 
- **Scenario file**: `YOUR_SCENARIO_FILE_NAME.xosc`
- **Scenario map**: `YOUR_SCENARIO_FILE_NAME.xodr`

Before using the scenario runner, please follow the [Getting Started](https://github.com/seclab-fudan/scenario_runner/blob/a1fe0e5f567abcb4c75420281866116f70d656b9/Docs/getting_scenariorunner.md#b-download-scenariorunner-from-source) Document.

You can use the following command to run a scenario in the LGSVL Simulator. Remember to place the map file in the same location as specified in the scenario file.
```
python3 scenario_runner.py --openscenario YOUR_SCENARIO_FILE_NAME.xosc
```

---
