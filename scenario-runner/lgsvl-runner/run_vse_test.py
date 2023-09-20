#!/usr/bin/env python3
#
# Created by SCTrans
#
# Modified script for running a lgsvl vse test, original script is from LG Electronics, Inc.


import json
import logging
import os
import re
import sys
import lgsvl
from datetime import datetime


FORMAT = '%(asctime)-15s [%(levelname)s][%(module)s] %(message)s'

logging.basicConfig(level=logging.INFO, format=FORMAT)
log = logging.getLogger(__name__)


class VSERunner:
    def __init__(self, json_file, _sensor_conf=None):
        with open(json_file) as f:
            self.VSE_dict = json.load(f)
        self.jsonfile= json_file
        self.isEgoFault = True
        self.isCollision = False
        self.sim = None
        self.ego_agents = []
        self.npc_agents = []
        self.pedestrian_agents = []
        self.sensor_conf = _sensor_conf

    def reset(self):
        log.debug("Reset VSE runner")
        self.ego_agents.clear()
        self.npc_agents.clear()
        self.pedestrian_agents.clear()

    def close(self):
        self.reset()
        self.sim.reset()
        self.sim.close()

    def setup_sim(self, default_host="127.0.0.1", default_port=8181):
        if not self.sim:
            simulator_host = os.getenv('LGSVL__SIMULATOR_HOST', default_host)
            simulator_port = int(os.getenv('LGSVL__SIMULATOR_PORT', default_port))
            log.debug("simulator_host is {}, simulator_port is {}".format(simulator_host, simulator_port))
            self.sim = lgsvl.Simulator(simulator_host, simulator_port)

    def connect_bridge(self, ego_agent, ego_index=0, default_host="127.0.0.1", default_port=9090):
        autopilot_host_env = "LGSVL__AUTOPILOT_{}_HOST".format(ego_index)
        autopilot_port_env = "LGSVL__AUTOPILOT_{}_PORT".format(ego_index)
        bridge_host = os.environ.get(autopilot_host_env, default_host)
        bridge_port = int(os.environ.get(autopilot_port_env, default_port))
        ego_agent.connect_bridge(bridge_host, bridge_port)

        return bridge_host, bridge_port

    def load_scene(self):
        if "map" not in self.VSE_dict.keys():
            log.error("No map specified in the scenario.")
            sys.exit(1)

        scene = self.VSE_dict["map"]["name"]
        log.info("Loading {} map.".format(scene))
        if self.sim.current_scene == scene:
            self.sim.reset()
        else:
            self.sim.load(scene,seed=650387)

    def load_agents(self):
        if "agents" not in self.VSE_dict.keys():
            log.warning("No agents specified in the scenario")
            return

        agents_data = self.VSE_dict["agents"]
        for agent_data in agents_data:
            log.debug("Adding agent {}, type: {}".format(agent_data["variant"], agent_data["type"]))
            agent_type_id = agent_data["type"]
            if agent_type_id == lgsvl.AgentType.EGO.value:
                self.ego_agents.append(agent_data)

            elif agent_type_id == lgsvl.AgentType.NPC.value:
                self.npc_agents.append(agent_data)

            elif agent_type_id == lgsvl.AgentType.PEDESTRIAN.value:
                self.pedestrian_agents.append(agent_data)

            else:
                log.warning("Unsupported agent type {}. Skipping agent.".format(agent_data["type"]))

        log.info("Loaded {} ego agents".format(len(self.ego_agents)))
        log.info("Loaded {} NPC agents".format(len(self.npc_agents)))
        log.info("Loaded {} pedestrian agents".format(len(self.pedestrian_agents)))

    def set_weather(self):
        if "weather" not in self.VSE_dict.keys() or "rain" not in self.VSE_dict["weather"]:
            log.debug("No weather specified in the scenarios")
            return
        weather_data = self.VSE_dict["weather"]
        weather_state = lgsvl.WeatherState(rain=weather_data["rain"],fog=weather_data["fog"],wetness=weather_data["wetness"],cloudiness=weather_data["cloudiness"],damage=weather_data["damage"])
        self.sim.weather = weather_state

    def set_time(self):
        if "time" not in self.VSE_dict.keys() or "year" not in self.VSE_dict["time"]:
            log.debug("No time specified in the scenarios")
            return
        time_data = self.VSE_dict["time"]
        dt = datetime(
            year = time_data["year"],
            month = time_data["month"],
            day = time_data["day"],
            hour = time_data["hour"],
            minute = time_data["minute"],
            second = time_data["second"]
        )
        self.sim.set_date_time(dt,fixed=False)

    def add_controllables(self):
        if "controllables" not in self.VSE_dict.keys():
            log.debug("No controllables specified in the scenarios")
            return

        controllables_data = self.VSE_dict["controllables"]
        for controllable_data in controllables_data:	
            # Name checking for backwards compability
            spawned = "name" in controllable_data or ("spawned" in controllables_data and controllable_data["spawned"])
            if spawned:
                log.debug("Adding controllable {}".format(controllable_data["name"]))
                controllable_state = lgsvl.ObjectState()
                controllable_state.transform = self.read_transform(controllable_data["transform"])
                try:
                    controllable = self.sim.controllable_add(controllable_data["name"], controllable_state)
                    policy = controllable_data["policy"]
                    if len(policy) > 0:
                        controllable.control(policy)
                except Exception as e:
                    msg = "Failed to add controllable {}, please make sure you have the correct simulator".format(controllable_data["name"])
                    log.error(msg)
                    log.error("Original exception: " + str(e))
            else:
                uid = controllable_data["uid"]
                log.debug("Setting policy for controllable {}".format(uid))
                controllable = self.sim.get_controllable_by_uid(uid)
                policy = controllable_data["policy"]
                if len(policy) > 0:
                    controllable.control(policy)
                
    def add_ego(self):
        for i, agent in enumerate(self.ego_agents):
            if "id" in agent:
                agent_name = agent["id"]
            else:
                agent_name = agent["variant"]
            agent_state = lgsvl.AgentState()
            if 'initial_speed' in agent:
                agent_state.velocity = lgsvl.Vector(agent['initial_speed']['x'],agent['initial_speed']['y'],agent['initial_speed']['z'])
            agent_state.transform = self.read_transform(agent["transform"])
            if "destinationPoint" in agent:
                agent_destination = lgsvl.Vector(
                    agent["destinationPoint"]["position"]["x"],
                    agent["destinationPoint"]["position"]["y"],
                    agent["destinationPoint"]["position"]["z"]
                )
                #
                # Set distination rotation once it is supported by DreamView
                #
                agent_destination_rotation = lgsvl.Vector(
                    agent["destinationPoint"]["rotation"]["x"],
                    agent["destinationPoint"]["rotation"]["y"],
                    agent["destinationPoint"]["rotation"]["z"],
                )
            def _on_collision(agent1, agent2, contact):
                self.isCollision = True

                name1 = "STATIC OBSTACLE" if agent1 is None else agent1.name
                name2 = "STATIC OBSTACLE" if agent2 is None else agent2.name
                if name1 == agent["sensorsConfigurationId"]:
                    _ego, _npc = agent1, agent2
                else:
                    _ego, _npc = agent2, agent1

                log.info("{} collided with {} at {}".format(name1, name2, contact))
                ego_speed = _ego.state.speed
                log.info("ego speed {}".format(ego_speed))
                if ego_speed < 0.005:
                    self.isEgoFault = False

                st1 = _ego.state
                st2 = _npc.state if _npc is not None else None

                log.info(st1.rotation)
                log.info(st2.rotation)
                log.info(st1.speed)
                log.info(st2.speed)

                degree = abs(st1.rotation.y - st2.rotation.y)
                degree = degree if degree < 180 else 360 - degree
                if st1.speed < st2.speed and degree <= 90:
                    log.info("NPC rear-end collision")
                elif st1.speed > st2.speed and degree <= 90:
                    log.info("EGO rear-end collision")
                else:
                    log.info("head-on collision")
                
                log.info("Stopping simulation")
                self.sim.stop()

            try:
                if self.sensor_conf:
                    ego = self.sim.add_agent(self.sensor_conf, lgsvl.AgentType.EGO, agent_state)
                elif "sensorsConfigurationId" in agent:
                    ego = self.sim.add_agent(agent["sensorsConfigurationId"], lgsvl.AgentType.EGO, agent_state)
                else:
                    ego = self.sim.add_agent(agent_name, lgsvl.AgentType.EGO, agent_state)
                ego.on_collision(_on_collision)
                self.ego = ego
            except Exception as e:
                msg = "Failed to add agent {}, please make sure you have the correct simulator".format(agent_name)
                log.error(msg)
                log.error("Original exception: " + str(e))
                sys.exit(1)

            try:
                bridge_host = self.connect_bridge(ego, i)[0]

                default_modules = [
                    'Localization',
                    'Transform',
                    'Routing',
                    'Prediction',
                    'Planning',
                    'Control'
                ]
                try:
                    modules = os.environ.get("LGSVL__AUTOPILOT_{}_VEHICLE_MODULES".format(i)).split(",")
                    if len(modules) == 0:
                        modules = default_modules
                except Exception:
                    modules = default_modules
                dv = lgsvl.dreamview.Connection(self.sim, ego, bridge_host)

                hd_map = os.environ.get("LGSVL__AUTOPILOT_HD_MAP")
                if not hd_map:
                    hd_map = self.sim.current_scene                   
                    words = self.split_pascal_case(hd_map)
                    hd_map = ' '.join(words)

                dv.set_hd_map(hd_map)
                dv.set_vehicle(os.environ.get("LGSVL__AUTOPILOT_{}_VEHICLE_CONFIG".format(i), agent["variant"]))
                if "destinationPoint" in agent:
                    dv.setup_apollo(agent_destination.x, agent_destination.z, modules)
                else:
                    log.info("No destination set for EGO {}".format(agent_name))
                    for mod in modules:
                        dv.enable_module(mod)
            except RuntimeWarning as e:
                msg = "Skipping bridge connection for vehicle: {}".format(agent["id"])
                log.warning("Original exception: " + str(e))
                log.warning(msg)
            except Exception as e:
                msg = "Something went wrong with bridge / dreamview connection."
                log.error("Original exception: " + str(e))
                log.error(msg)

    def add_npc(self):
        for agent in self.npc_agents:
            if "id" in agent:
                agent_name = agent["id"]
            else:
                agent_name = agent["variant"]
            agent_state = lgsvl.AgentState()
            agent_state.transform = self.read_transform(agent["transform"])
            agent_color = lgsvl.Vector(agent["color"]["r"], agent["color"]["g"], agent["color"]["b"]) if "color" in agent else None

            try:
                npc = self.sim.add_agent(agent_name, lgsvl.AgentType.NPC, agent_state, agent_color)
            except Exception as e:
                msg = "Failed to add agent {}, please make sure you have the correct simulator".format(agent_name)
                log.error(msg)
                log.error("Original exception: " + str(e))
                sys.exit(1)

            if agent["behaviour"]["name"] == "NPCWaypointBehaviour":
                waypoints = self.read_waypoints(agent["waypoints"])
                if waypoints:
                    npc.follow(waypoints)
            elif agent["behaviour"]["name"] == "NPCLaneFollowBehaviour":
                npc.follow_closest_lane(
                    True,
                    agent["behaviour"]["parameters"]["maxSpeed"],
                    agent["behaviour"]["parameters"]["isLaneChange"]
                )

    def add_pedestrian(self):
        for agent in self.pedestrian_agents:
            if "id" in agent:
                agent_name = agent["id"]
            else:
                agent_name = agent["variant"]
            agent_state = lgsvl.AgentState()
            agent_state.transform = self.read_transform(agent["transform"])

            try:
                pedestrian = self.sim.add_agent(agent_name, lgsvl.AgentType.PEDESTRIAN, agent_state)
            except Exception as e:
                msg = "Failed to add agent {}, please make sure you have the correct simulator".format(agent_name)
                log.error(msg)
                log.error("Original exception: " + str(e))
                sys.exit(1)

            waypoints = self.read_waypoints(agent["waypoints"])
            if waypoints:
                pedestrian.follow(waypoints)

    def read_transform(self, transform_data):
        transform = lgsvl.Transform()
        transform.position = lgsvl.Vector.from_json(transform_data["position"])
        transform.rotation = lgsvl.Vector.from_json(transform_data["rotation"])

        return transform

    def read_waypoints(self, waypoints_data):
        waypoints = []
        for waypoint_data in waypoints_data:
            position = lgsvl.Vector.from_json(waypoint_data["position"])
            speed = waypoint_data["speed"]
            angle = lgsvl.Vector.from_json(waypoint_data["angle"])
            if "wait_time" in waypoint_data:
                wait_time = waypoint_data["wait_time"]
            else:
                wait_time = waypoint_data["waitTime"]
            trigger = self.read_trigger(waypoint_data)

            if 'trigger_distance' in waypoint_data:
                td = waypoint_data['trigger_distance']
                waypoint = lgsvl.DriveWaypoint(position, speed, angle=angle, idle=wait_time, trigger_distance=td, trigger=trigger)
            else:
                waypoint = lgsvl.DriveWaypoint(position, speed, angle=angle, idle=wait_time, trigger=trigger)

            waypoints.append(waypoint)

        return waypoints

    def read_trigger(self, waypoint_data):
        if "trigger" not in waypoint_data:
            return None
        effectors_data = waypoint_data["trigger"]["effectors"]
        if len(effectors_data) == 0:
            return None

        effectors = []
        for effector_data in effectors_data:
            effector = lgsvl.TriggerEffector(effector_data["typeName"], effector_data["parameters"])
            effectors.append(effector)
        trigger = lgsvl.WaypointTrigger(effectors)

        return trigger

    def split_pascal_case(self, s):
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z\d])|(?<=[A-Z\d])(?=[A-Z][a-z])|$)', s)
        return [m.group(0) for m in matches]
   
    def run(self, duration=0.0, force_duration=False, loop=False):
        log.debug("Duration is set to {}.".format(duration))
        self.setup_sim()

        while True:
            self.load_scene()
            self.set_time()
            self.load_agents()
            self.set_weather()
            self.add_ego()  # Must go first since dreamview api may call sim.run()
            self.add_npc()
            self.add_pedestrian() 
            self.add_controllables()

            def _on_agents_traversed_waypoints():
                log.info("All agents traversed their waypoints.")

                if not force_duration:
                    log.info("Stopping simulation")
                    self.sim.stop()

            # self.sim.agents_traversed_waypoints(_on_agents_traversed_waypoints)

            log.info("Starting scenario...")
            self.sim.run(duration)
            log.info("Scenario simulation ended.")
            
            # code for logging the collision result
            '''
            if self.isCollision:
                log.info("Collision happen! IsEgoFault:{}".format(self.isEgoFault))
                if self.isEgoFault:
                    os.system("cp {} {}".format(self.jsonfile,"./true_collision/"))
                else:
                    os.system("cp {} {}".format(self.jsonfile,"./fp_collision"))
            else:
                os.system("cp {} {}".format(self.jsonfile,"./not_collision"))
            '''
            if loop:
                self.reset()
            else:
                break



if __name__ == "__main__":
    if len(sys.argv) < 2:
        log.error("Input file is not specified, please provide the scenario JSON file.")
        sys.exit(1)
    json_file = sys.argv[1]
    if len(sys.argv) > 2:
        vse_runner = VSERunner(json_file, sys.argv[2])
    else:
        vse_runner = VSERunner(json_file)
    vse_runner.run(30)
    vse_runner.close()