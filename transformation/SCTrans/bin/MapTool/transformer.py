import sys
import warnings
from lxml import etree
from commonroad.common.file_reader import CommonRoadFileReader
from crdesigner.map_conversion.lanelet_lanelet2.cr2lanelet import CR2LaneletConverter

warnings.filterwarnings("ignore")
input_path = sys.argv[1] 
output_name = sys.argv[1].replace('.cr', '',1)
output_name = output_name.replace('.xml','.osm')
proj = ""  # replace empty string


# use Lanelet conversion APIs
try:
    commonroad_reader = CommonRoadFileReader(input_path)
    scenario, _ = commonroad_reader.open()
except etree.XMLSyntaxError as xml_error:
    print(f"SyntaxError: {xml_error}")
    print(
        "There was an error during the loading of the selected CommonRoad file.\n"
    )
    scenario = None

if scenario:
    l2osm = CR2LaneletConverter(proj)
    osm = l2osm(scenario)
    print(l2osm.osm.nodes.get('-1').lat)
    print(l2osm.osm.nodes.get('-1').lon)
    with open(f"{output_name}", "wb") as file_out:
        file_out.write(
            etree.tostring(
                osm, xml_declaration=True, encoding="UTF-8", pretty_print=True
            )
    )
