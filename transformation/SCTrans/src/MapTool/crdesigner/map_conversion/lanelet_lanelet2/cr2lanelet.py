"""Module to convert a lanelet UTM representation to OSM."""

__author__ = "Benjamin Orthen"
__copyright__ = "TUM Cyber-Physical Systems Group"
__credits__ = ["Priority Program SPP 1835 Cooperative Interacting Automobiles"]
__version__ = "0.2"
__maintainer__ = "Sebastian Maierhofer"
__email__ = "commonroad@lists.lrz.de"
__status__ = "Released"

from typing import Dict, List, Tuple
from commonroad.common.util import make_valid_orientation

import numpy as np
from pyproj import Proj
from commonroad.scenario.lanelet import Lanelet,LineMarking
from commonroad.scenario.traffic_sign import TrafficLightState,TrafficSignIDUsa,TrafficSignIDGermany,TrafficSignIDZamunda,TrafficSignIDSpain
from crdesigner.map_conversion.lanelet_lanelet2.lanelet2 import OSMLanelet, Node, Way, WayRelation,TrafficWayRelation,TrafficSignWayRelation, DEFAULT_PROJ_STRING, maxspeedRelatation

#ways_are_equal_tolerance = 0.001
ways_are_equal_tolerance = 0.5

class CR2LaneletConverter:
    """Class to convert CommonRoad lanelet to the OSM representation."""

    def __init__(self, proj_string = None):
        if proj_string:
            self.proj = Proj(proj_string)
        else:
            self.proj = Proj(DEFAULT_PROJ_STRING)
        self.osm = None
        self._id_count = -1
        self.first_nodes, self.last_nodes = None, None
        self.left_ways, self.right_ways = None, None
        self.lanelet_network = None
        self.traffic_lights : Dict[int,List()] = None
        self.traffic_light_set = None
        self.update_relation : Dict[int,List()] = None
        self.traffic_light_id : Dict[int,int] = None # traffic_light_id[xml_id]=osm_id

    @property
    def id_count(self) -> int:
        """Internal counter for giving IDs to the members of the OSM.

        Each call returns the count and increases it by one.
        Returns:
          Current id count.
        """
        tmp = self._id_count
        self._id_count -= 1
        return tmp

    def __call__(self, scenario):
        """Convert a scenario to an OSM xml document.

        Args:
          scenario:
        """
        self.osm = OSMLanelet()
        self.lanelet_network = scenario.lanelet_network
        self.first_nodes = dict()  # saves first left and right node
        self.last_nodes = dict()  # saves last left and right node
        self.left_ways = dict()
        self.right_ways = dict()
        self.traffic_lights : Dict[int,List()] = {}
        self.traffic_light_set = []
        self.update_relation : Dict[int,List()] = {}
        self.traffic_light_id : Dict[int,int] = {}

        for traffic_light in scenario.lanelet_network.traffic_lights:
            self.traffic_lights[traffic_light.traffic_light_id] = []
            self.update_relation[traffic_light.traffic_light_id] = []
            self.traffic_light_id[traffic_light.traffic_light_id] = 0
            
        for lanelet in scenario.lanelet_network.lanelets:
            self._convert_lanelet(lanelet)
        self._create_traffic_relation()
        return self.osm.serialize_to_xml()
    '''
    def _create_trffic_sign(self):
        if self.lanelet_network._traffic_signs:
            for sign_id in self.lanelet_network._traffic_signs:
                current_traffic_Sign = self.lanelet_network._traffic_signs[sign_id]._traffic_sign_elements[0]
                if not current_traffic_Sign._additional_values:
                #print(self.lanelet_network._traffic_signs[sign_id]._traffic_sign_id)
                #stopline+position+relation
                    stop_nodes = []
                    #print(self.first_nodes[self.lanelet_network._traffic_signs[sign_id]._first_occurrence][0])
                    y=list(self.lanelet_network._traffic_signs[sign_id]._first_occurrence)
                    y_id = y[0]
                    stop_nodes.append(self.first_nodes[y_id][0])
                    stop_nodes.append(self.first_nodes[y_id][1])
                    stop_line = Way(self.id_count,stop_nodes,tag_dict={"type":"stop_line"})
                    self.osm.add_way(stop_line)
                    #position
                    lon, lat = self.proj(self.lanelet_network._traffic_signs[sign_id].position[0], self.lanelet_network._traffic_signs[sign_id].position[1], inverse=True)
                    node = Node(self.id_count, lat, lon)
                    self.osm.add_node(node)
                    sign_nodes=[]
                    sign_nodes.append(node.id_)
                    node2 = Node(self.id_count, lat, lon)
                    sign_nodes.append(node2.id_)
                    self.osm.add_node(node2)

                # 处理subtype
                # 非speed limit
                current_traffic_Sign = self.lanelet_network._traffic_signs[sign_id]._traffic_sign_elements[0]
                if not current_traffic_Sign._additional_values:
                    #print(self.lanelet_network._traffic_signs[sign_id]._traffic_sign_elements[0]._additional_values)
                    if type(current_traffic_Sign._traffic_sign_element_id) == TrafficSignIDUsa:
                        current_subtype = "us"+str(current_traffic_Sign._traffic_sign_element_id.value)
                    elif type(current_traffic_Sign._traffic_sign_element_id) == TrafficSignIDGermany:
                        current_subtype = "de"+str(current_traffic_Sign._traffic_sign_element_id.value)
                    elif type(current_traffic_Sign._traffic_sign_element_id) ==  TrafficSignIDSpain:
                        current_subtype = "es"+str(current_traffic_Sign._traffic_sign_element_id.value)
                    else:
                        current_subtype = "de"+str(current_traffic_Sign._traffic_sign_element_id.value)    
                        #print(current_subtype)
                    
                    sign_way = Way(self.id_count,sign_nodes,tag_dict={"height":"0","subtype":current_subtype,"type":"traffic_sign"})
                    self.osm.add_way(sign_way)
                    current_refers=[]
                    current_refers.append(sign_way.id_)
                    sign_relation = TrafficSignWayRelation(self.id_count,stop_line.id_,current_refers)
                    self.osm.add_trafficsign_way_relation(sign_relation)
    '''
    def _create_traffic_relation(self):
       #set up relation：stopline+refer+light_bulbs+relation
        for light_set in self.traffic_light_set:
            stop_line_id = None
            refer_list = []
            bulb_list = []
            # set up stopline
            stopline_nodes = set()
            for traffic_light in light_set:
                for refer_line in self.traffic_lights[traffic_light]:
                    stopline_nodes.add(self.last_nodes[refer_line][0])
                    stopline_nodes.add(self.last_nodes[refer_line][1])
            #print(stopline_nodes)
            stop_line = Way(self.id_count,stopline_nodes,tag_dict={"type":"stop_line"})
            self.osm.add_way(stop_line)
            stop_line_id = stop_line.id_
            
            # set up traffic light
            for light_id in light_set:
                # find traffic light in xml
                for traffic_light in self.lanelet_network.traffic_lights:
                    if traffic_light.traffic_light_id == light_id: break
                lon, lat = self.proj(traffic_light.position[0], traffic_light.position[1], inverse=True)
                node = Node(self.id_count, lat, lon)
                self.osm.add_node(node)
                light_nodes=[]
                light_nodes.append(node.id_)
                node2 = Node(self.id_count, lat, lon)
                light_nodes.append(node2.id_)
                self.osm.add_node(node2)

                light_color =set()
                color_nodes = []
                for color in traffic_light.cycle:
                    if color.state == TrafficLightState.RED:
                        dict_tag = {"color":"red"}
                        light_color.add("red")
                    elif color.state == TrafficLightState.YELLOW:
                        dict_tag = {"color":"yellow"}
                        light_color.add("yellow")
                    elif color.state == TrafficLightState.GREEN:
                        dict_tag = {"color":"green"}
                        light_color.add("green")
                    elif color.state == TrafficLightState.INACTIVE:
                        dict_tag = {"color":"black"}
                        light_color.add("inactive")
                    node = Node(self.id_count, lat, lon,dict_tag)
                    color_nodes.append(node.id_)
                    self.osm.add_node(node)

                tag_dict = {"type":"traffic_light","height":"0"}
                if light_color == {"red","yellow","green"} :
                    tag_dict.update({"subtype":"red_yellow_green"})
                elif light_color == {"red","yellow"} or light_color == {"red","yellow","inactive"}:
                    tag_dict.update({"subtype":"red_yellow"})
                elif light_color == {"red","green"} or light_color == {"red","green","inactive"}:   
                    tag_dict.update({"subtype":"red_green"}) 
                elif light_color == {"red"} or light_color == {"red","inactive"}:   
                    tag_dict.update({"subtype":"red"}) 
                elif light_color == {"yellow"} or light_color == {"yellow","inactive"}:   
                    tag_dict.update({"subtype":"yellow"}) 
                elif light_color == {"inactive"}:
                    tag_dict.update({"subtype":"white"})
                trffic_way = Way(self.id_count,light_nodes,tag_dict)
                self.osm.add_way(trffic_way)
                refer_list.append(trffic_way.id_)
                self.traffic_light_id[light_id] = trffic_way.id_
                bulb_tag ={"type":"light_bulbs","traffic_light_id":trffic_way.id_}
                light_bulb_way = Way(self.id_count,color_nodes,bulb_tag)  
                self.osm.add_way(light_bulb_way)
                bulb_list.append(light_bulb_way.id_)
            light_relation= TrafficWayRelation(self.id_count,stop_line_id,refer_list,bulb_list)   
            self.osm.add_trafficlight_way_relation(light_relation)

            for traffic_light in light_set:
                index_list = self.update_relation[traffic_light]
                for index in index_list:
                    self.osm.way_relations[index].regulatory_elements.append(light_relation.id_)


    
    def _convert_lanelet(self, lanelet: Lanelet):
        """Convert a lanelet to a way relation.

        Add the resulting relation and its ways and nodes to the OSM.

        Args:
          lanelet: Lanelet to be converted.
        """

        # check if there are shared ways
        right_way_id = self._get_potential_right_way(lanelet)
        #print(str(lanelet._adj_left)+str(lanelet.lanelet_id)+str(lanelet._adj_right))
        left_way_id = self._get_potential_left_way(lanelet)
        #print("left:"+str(left_way_id)+"right:"+str(right_way_id))

        left_nodes, right_nodes = self._create_nodes(lanelet, left_way_id, right_way_id)

        self.first_nodes[lanelet.lanelet_id] = (left_nodes[0], right_nodes[0])
        self.last_nodes[lanelet.lanelet_id] = (left_nodes[-1], right_nodes[-1])

        left_tag_dict={}
        right_tag_dict={}
        if lanelet.line_marking_left_vertices == LineMarking.UNKNOWN or lanelet.line_marking_left_vertices == LineMarking.DASHED or lanelet.line_marking_left_vertices == LineMarking.BROAD_DASHED:
            left_tag_dict= {"type":"line_thin","subtype":"dashed","color":"white"}
        elif lanelet.line_marking_left_vertices == LineMarking.SOLID or lanelet.line_marking_left_vertices == LineMarking.BROAD_SOLID:
            left_tag_dict= {"type":"line_thin","subtype":"solid","color":"white"}

        if lanelet.line_marking_right_vertices == LineMarking.UNKNOWN or lanelet.line_marking_right_vertices== LineMarking.DASHED or lanelet.line_marking_right_vertices == LineMarking.BROAD_DASHED:
            right_tag_dict= {"type":"line_thin","subtype":"dashed","color":"white"}
        elif lanelet.line_marking_right_vertices == LineMarking.SOLID or lanelet.line_marking_right_vertices == LineMarking.BROAD_SOLID:
            right_tag_dict= {"type":"line_thin","subtype":"solid","color":"white"}

        if not left_way_id:
            left_way = Way(self.id_count, left_nodes,left_tag_dict)
            self.osm.add_way(left_way)
            left_way_id = left_way.id_
        if not right_way_id:
            right_way = Way(self.id_count, right_nodes,right_tag_dict)
            self.osm.add_way(right_way)
            right_way_id = right_way.id_
        

        self.left_ways[lanelet.lanelet_id] = left_way_id
        self.right_ways[lanelet.lanelet_id] = right_way_id
        
        regulatory_elements=[]

        if lanelet._traffic_signs:
        # add speed limit sign
           
            sign_list = list(lanelet._traffic_signs)       
            for sign_id in sign_list:
                current_traffic_Sign = self.lanelet_network._traffic_signs[sign_id]._traffic_sign_elements[0]
                # add speed limit sign
                if current_traffic_Sign._additional_values:
                    max_speed = float(current_traffic_Sign._additional_values[0])
                    maxspeed_relation = maxspeedRelatation(self.id_count,tag_dict={"type":"regulatory_element","subtype":"speed_limit","max_speed":str(max_speed/0.44704),"max_speed_unit":"mph"})
                    self.osm.add_maxspeed_relation(maxspeed_relation)
                    regulatory_elements.append(maxspeed_relation.id_)
                    #self.osm.add_way_relation(WayRelation(self.id_count, left_way_id, right_way_id, tag_dict={"type": "lanelet"},regulatory_elements=[str(maxspeed_relation.id_)]))
                    # add else sign    
                '''
                else:
                    stop_nodes = []
                    #print(self.first_nodes[self.lanelet_network._traffic_signs[sign_id]._first_occurrence][0])
                    y=list(self.lanelet_network._traffic_signs[sign_id]._first_occurrence)
                    y_id = y[0]
                    lon1 = self.osm.nodes[self.first_nodes[y_id][0]].lon
                    lat1 = self.osm.nodes[self.first_nodes[y_id][0]].lat
                    lon2 = self.osm.nodes[self.first_nodes[y_id][1]].lon
                    lat2 = self.osm.nodes[self.first_nodes[y_id][1]].lat
                    lon = (float(lon1)+float(lon2))/2
                    lat = (float(lat1)+float(lat2))/2
                    mid_node = Node(self.id_count,lat,lon)
                    self.osm.add_node(mid_node)

                    stop_nodes.append(self.first_nodes[y_id][0])
                    stop_nodes.append(mid_node.id_)
                    stop_nodes.append(self.first_nodes[y_id][1])
                    stop_line = Way(self.id_count,stop_nodes,tag_dict={"type":"stop_line"})
                    self.osm.add_way(stop_line)
                    #position
                    lon, lat = self.proj(self.lanelet_network._traffic_signs[sign_id].position[0], self.lanelet_network._traffic_signs[sign_id].position[1], inverse=True)
                    node = Node(self.id_count, lat, lon)
                    self.osm.add_node(node)
                    sign_nodes=[]
                    sign_nodes.append(node.id_)
                    node2 = Node(self.id_count, lat, lon)
                    sign_nodes.append(node2.id_)
                    self.osm.add_node(node2)

                    if type(current_traffic_Sign._traffic_sign_element_id) == TrafficSignIDUsa:
                        current_subtype = "us"+str(current_traffic_Sign._traffic_sign_element_id.value)
                    elif type(current_traffic_Sign._traffic_sign_element_id) == TrafficSignIDGermany:
                        current_subtype = "de"+str(current_traffic_Sign._traffic_sign_element_id.value)
                    elif type(current_traffic_Sign._traffic_sign_element_id) ==  TrafficSignIDSpain:
                        current_subtype = "es"+str(current_traffic_Sign._traffic_sign_element_id.value)
                    else:
                        current_subtype = "de"+str(current_traffic_Sign._traffic_sign_element_id.value)
                    
                    sign_way = Way(self.id_count,sign_nodes,tag_dict={"height":"0","subtype":current_subtype,"type":"traffic_sign"})
                    self.osm.add_way(sign_way)
                    current_refers=[]
                    current_refers.append(sign_way.id_)
                    sign_relation = TrafficSignWayRelation(self.id_count,stop_line.id_,current_refers)
                    self.osm.add_trafficsign_way_relation(sign_relation)
                    #regulatory_elements.append(sign_relation.id_)
                    self.osm.add_way_relation(WayRelation(self.id_count, left_way_id, right_way_id, tag_dict={"type": "lanelet"},regulatory_elements=[str(sign_relation.id_)]))
                '''      
            
        current_relation=WayRelation(self.id_count, left_way_id, right_way_id, tag_dict={"type": "lanelet"},regulatory_elements=regulatory_elements)        
        self.osm.add_way_relation(current_relation)     

        # transform traffic light
        if lanelet._traffic_lights:
            
            for light_id in lanelet._traffic_lights:
                self.traffic_lights[light_id].append(lanelet.lanelet_id)
                self.update_relation[light_id].append(current_relation.id_)
            flag = True
            for light_id in lanelet._traffic_lights:
                for set in self.traffic_light_set:
                    if light_id in set:
                        self.traffic_light_set.remove(set)
                        self.traffic_light_set.append(set | lanelet._traffic_lights)
                        flag = False
                        break
                if not flag:
                    break

            if flag:
                self.traffic_light_set.append(lanelet._traffic_lights)
            

    def _create_nodes(
        self, lanelet: Lanelet, left_way_id: str, right_way_id: str
    ) -> Tuple[List[str], List[str]]:
        """Create new nodes for the ways of the lanelet.
        Add them to OSM and return a list of the node ids.

        In case a left or right way already exists, the returned list
        only contains the first and last node of the way.
        Args:
          lanelet: Lanelet of which the right and left vertices should be converted to ways.
          left_way_id: Id of a potential shared left way which was already converted.
            If this is not None, the left vertices of the lanelet do not have to be converted again.
          right_way_id: Id of a potential right way, similar to left_way_id.
        Returns:
          A tuple of lists of node ids for the left and the right way.
        """
        left_nodes, right_nodes = [], []
        start_index = 0
        end_index = len(lanelet.left_vertices)
        pot_first_left_node, pot_first_right_node = self._get_shared_first_nodes_from_other_lanelets(
            lanelet
        )
        pot_last_left_node, pot_last_right_node = self._get_shared_last_nodes_from_other_lanelets(
            lanelet
        )
        if pot_first_left_node:
            start_index = 1
        if pot_last_left_node:
            end_index = -1

        if left_way_id:
            first_left_node, last_left_node = self._get_first_and_last_nodes_from_way(
                left_way_id, lanelet.adj_left_same_direction
            )
        else:
            first_left_node = pot_first_left_node
            last_left_node = pot_last_left_node
            left_nodes = self._create_nodes_from_vertices(
                lanelet.left_vertices[start_index:end_index]
            )
        if right_way_id:
            first_right_node, last_right_node = self._get_first_and_last_nodes_from_way(
                right_way_id, lanelet.adj_right_same_direction
            )
        else:
            first_right_node = pot_first_right_node
            last_right_node = pot_last_right_node
            right_nodes = self._create_nodes_from_vertices(
                lanelet.right_vertices[start_index:end_index]
            )

        if first_left_node:
            left_nodes.insert(0, first_left_node)
        if first_right_node:
            right_nodes.insert(0, first_right_node)

        if last_left_node:
            left_nodes.append(last_left_node)
        if last_right_node:
            right_nodes.append(last_right_node)

        return left_nodes, right_nodes

    def _get_first_and_last_nodes_from_way(
        self, way_id: str, same_dir: bool
    ) -> Tuple[str, str]:
        """Get the first and the last node of a way.

        Reverse order of nodes if way is reversed.
        Args:
          way_id: Id of way.
          same_dir: True if way is in normal direction, False if it is reversed.
        Returns:
          Tuple with first and last node.
        """
        way = self.osm.find_way_by_id(way_id)
        first_idx, last_idx = (0, -1) if same_dir else (-1, 0)
        return (way.nodes[first_idx], way.nodes[last_idx])

    def _create_nodes_from_vertices(self, vertices: List[np.ndarray]) -> List[str]:
        """Create nodes and add them to the OSM.

        Args:
          vertices: List of vertices from a lanelet boundary.
        Returns:
          Ids of nodes which were created.
        """
        nodes = []
        for vertice in vertices:
            lon, lat = self.proj(vertice[0], vertice[1], inverse=True)
            node = Node(self.id_count, lat, lon)
            nodes.append(node.id_)
            self.osm.add_node(node)
        return nodes

    def _get_potential_right_way(self, lanelet):
        """Check if a shared right boundary with another lanelet can be transformed
            to the same way.

        Args:
          lanelet: Lanelet of which right boundary should be converted to a way.
        Returns:
          Id of a way which can be shared, else None if it is not possible.
        """
        if lanelet.adj_right:
            if lanelet.adj_right_same_direction:
                potential_right_way = self.left_ways.get(lanelet.adj_right)
            else:
                potential_right_way = self.right_ways.get(lanelet.adj_right)
            #print(potential_right_way)
            if potential_right_way:
                adj_right = self.lanelet_network.find_lanelet_by_id(lanelet.adj_right)
                vertices = (
                    adj_right.left_vertices
                    if lanelet.adj_right_same_direction
                    else adj_right.right_vertices[::-1]
                )
                if _vertices_are_equal(lanelet.right_vertices, vertices):
                    return potential_right_way

        return None

    def _get_potential_left_way(self, lanelet):
        """Check if a shared left boundary with another lanelet can be transformed
            to the same way.

        Args:
          lanelet: Lanelet of which left boundary should be converted to a way.
        Returns:
          Id of a way which can be shared, else None if it is not possible.
        """
        if lanelet.adj_left:
            if lanelet.adj_left_same_direction:
                potential_left_way = self.right_ways.get(lanelet.adj_left)
            else:
                potential_left_way = self.left_ways.get(lanelet.adj_left)
            #print(potential_left_way)
            if potential_left_way:
                adj_left = self.lanelet_network.find_lanelet_by_id(lanelet.adj_left)
                vertices = (
                    adj_left.right_vertices
                    if lanelet.adj_left_same_direction
                    else adj_left.left_vertices[::-1]
                )
                if _vertices_are_equal(lanelet.left_vertices, vertices):
                    return potential_left_way

        return None

    def _get_shared_first_nodes_from_other_lanelets(
        self, lanelet: Lanelet
    ) -> Tuple[str, str]:
        """Get already created nodes from other lanelets which could also
           be used by this lanelet as first nodes.

        Args:
          lanelet: Lanelet for which shared nodes should be found.
        Returns:
          Id of first left and first right node if they exist.
        """
        if lanelet.predecessor:
            for lanelet_id in lanelet.predecessor:
                first_left_node, first_right_node = self.last_nodes.get(
                    lanelet_id, (None, None)
                )
                if first_left_node:
                    return first_left_node, first_right_node
            for pred_id in lanelet.predecessor:
                pred = self.lanelet_network.find_lanelet_by_id(pred_id)
                for succ_id in pred.successor:
                    first_left_node, first_right_node = self.first_nodes.get(
                        succ_id, (None, None)
                    )
                    if first_left_node:
                        return first_left_node, first_right_node
        return None, None

    def _get_shared_last_nodes_from_other_lanelets(
        self, lanelet: Lanelet
    ) -> Tuple[str, str]:
        """Get already created nodes from other lanelets which could also
           be used by this lanelet as last nodes.

        Args:
          lanelet: Lanelet for which shared nodes should be found.
        Returns:
          Id of last left and last right node if they exist.
        """
        if lanelet.successor:
            for lanelet_id in lanelet.successor:
                last_left_node, last_right_node = self.first_nodes.get(
                    lanelet_id, (None, None)
                )
                if last_left_node:
                    return last_left_node, last_right_node
            for succ_id in lanelet.successor:
                succ = self.lanelet_network.find_lanelet_by_id(succ_id)
                for pred_id in succ.predecessor:
                    last_left_node, last_right_node = self.last_nodes.get(
                        pred_id, (None, None)
                    )
                    if last_left_node:
                        return last_left_node, last_right_node

        return None, None


def _vertices_are_equal(
    vertices1: List[np.ndarray], vertices2: List[np.ndarray]
) -> bool:
    """Checks if two list of vertices are equal up to a tolerance.

    Args:
      vertices1: First vertices to compare.
      vertices2: Second vertices to compare.

    Returns:
      True if every vertice in one list is nearly equal to the
        corresponding vertices at the same position in the other list.
    """

    
    diff1 = vertices1[0] - vertices2[0]
    diff2 = vertices1[-1] - vertices2[-1]
    if np.abs(np.max(diff1)) > ways_are_equal_tolerance or np.abs(np.max(diff2)) > ways_are_equal_tolerance:
        return False
    return True
    '''
    #ways_are_equal_tolerance = 0.001
    if len(vertices1) != len(vertices2):
        return False
    diff = vertices1 - vertices2
    print(diff)
    print(np.max(diff))
    if np.abs(np.max(diff)) < ways_are_equal_tolerance:
        return True
    return False
   '''
