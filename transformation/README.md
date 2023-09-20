# Scenario Transformation 

## Environment Setup

### 1) Java
```
-> & java --version
openjdk version "17.0.5" 2022-11-02
```

### 2) Python
```
-> % python --version
Python 3.8.10
```

### 3) Java-Lib Dependency

Available in the directory: **`transoformation/jarlib/`**
- org.eclipse.emf.common.jar
- org.eclipse.emf.ecore.xmi.jar
- org.eclipse.emf.ecore.jar
- org.eclipse.m2m.atl.common.jar
- org.eclipse.m2m.atl.emftvm.trace.jar
- org.eclipse.m2m.atl.emftvm.jar
- org.objectweb.asm.jar
- org.json.jar
- org.osgeo.proj4j.jar

You can directly refer them in the project.

### 4) Python-lib Dependency

During the transformation, we utilize and modify the crd 
**Install:**
```
pip install -r model_transoformation/SCTrans/src/map/requirements.txt
```

### 5) Build the project


## Input Preparation

### Source Traffic Scenario

In this work, we implement SCTrans on three source traffic scenario datasets:
- [CommonRoad](https://commonroad.in.tum.de/scenarios)
- [inD Dataset](https://www.ind-dataset.com)
- [highD Dataset](https://www.highd-dataset.com)

Please note that according to our policy, we cannot provide access to the source traffic scenarios directly. If you wish to access these source traffic scenarios, kindly refer to the official site below and adhere to the specified requirements.

### Preprocessing Scenario

For **CommonRoad** Scenario, you can directly download scenarios form official site [CommonRoad](https://commonroad.in.tum.de) and move it to the `SCTrans/models` directory.

For **inD** and **highD** Scenario, after downloading the traffic scenario, you need use [Dataset Converter](https://commonroad.in.tum.de/tools/dataset-converters) provided by CommonRoad to extract CommonRoad Scenario and then move it to the `SCTrans/models` directory.


### Scenario Transformation

#### Quick Start
You can use the following command to run a transformation. Remember to modify the path and arguments first.
```
java -classpath /YOUR_PROJECTPATH/SCTrans/bin/:/PROJECTPATH/SCTrans/lib/json-20220924.jar:/PROJECTPATH/SCTrans/lib/org.eclipse.emf.common_2.10.0.v20140514-1158.jar:/PROJECTPATH/SCTrans/lib/org.eclipse.emf.ecore.xmi_2.10.0.v20140514-1158.jar:/PROJECTPATH/SCTrans/lib/org.eclipse.emf.ecore_2.10.0.v20140514-1158.jar:/PROJECTPATH/SCTrans/lib/org.eclipse.m2m.atl.common_3.3.1.v201209061455.jar:/PROJECTPATH/SCTrans/lib/org.eclipse.m2m.atl.emftvm.trace_3.6.0.v201501081942.jar:/PROJECTPATH/SCTrans/lib/org.eclipse.m2m.atl.emftvm_3.6.0.v201501081942.jar:/PROJECTPATH/SCTrans/lib/org.objectweb.asm_3.3.1.v201105211655.jar:/PROJECTPATH/SCTrans/lib/proj4j-0.1.0.jar -XX:+ShowCodeDetailsInExceptionMessages SCTrans.SCTransLauncher TARGET_MODEL YOUR_SCENARIO_FILE_NAME YOUR_PATH_TO_SCENARIO
```
**Arguments**
- TARGET_MODEL: `OpenSCENARIO` or `Lgsvl`
- YOUR_SCENARIO_FILE_NAME: e.g. `ARG_Carcarana-1_1_I-1-1.cr.xml`
- YOUR_ABSOLUTE_PATH_TO_SCENARIO: e.g. `/XXX/YYY/ZZZ/`

If success, there will be four new files generated:
- in_model: `YOUR_SCENARIO_FILE_NAME.xmi`
- out_model: `YOUR_SCENARIO_FILE_NAME_out.xmi`
- out_scenario: `YOUR_SCENARIO_FILE_NAME.json/.xosc`
- out_osm_map: `YOUR_SCENARIO_FILE_NAME.osm`

#### Source Code Build
we also provide all source code for you to build the project yourself. You can import the project from folder, refer all extended jar files and build the project.

### Map Transformation

Use the out_osm_map(YOUR_SCENARIO_FILE_NAME.osm) as input HD map to get Lgsvl Environment Zip and OpenDrive HD map.
Follow the tutorial of [Add new map](https://www.svlsimulator.com/docs/archive/2020.06/add-new-map/)

The output OpenDrive HD map may have some problems. Before using it in carla, you can use the script below to patch the problems. [TODO]

### Dataset
We also provide all simulation-ready scenarios and maps, please see our website to get access.