import sys
import xml.etree.ElementTree as ET


def remove_ns0_from_file(file_path):
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Remove all occurrences of 'ns0:'
        modified_content = content.replace('ns0:', '')

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(modified_content)

        print(f'Successfully removed "ns0:" from {file_path}')

    except FileNotFoundError:
        print(f'Error: File not found - {file_path}')

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        
def add_jacoco_configuration(pom_file):
    # Load the XML file with namespace information
    tree = ET.parse(pom_file)
    root = tree.getroot()

    # Extract namespace information
    namespace = root.tag.split('}')[0] + '}'

    # Find or create the build section
    build = root.find(".//{}build".format(namespace))
    if build is None:
        build = ET.Element("{}build".format(namespace))
        root.append(build)

    # Find or create the plugins section within the build section
    plugins = build.find(".//{}plugins".format(namespace))
    if plugins is None:
        plugins = ET.SubElement(build, "{}plugins".format(namespace))

    # Check if JaCoCo plugin already exists
    existing_jacoco = plugins.find(".//{}artifactId[.='jacoco-maven-plugin']".format(namespace))
    if existing_jacoco is not None:
        print("JaCoCo plugin configuration already exists in the pom.xml.")
        sys.exit(0)

    # Define JaCoCo plugin configuration
    jacoco_plugin = ET.Element("{}plugin".format(namespace))
    jacoco_plugin_groupId = ET.SubElement(jacoco_plugin, "{}groupId".format(namespace))
    jacoco_plugin_groupId.text = "org.jacoco"
    jacoco_plugin_artifactId = ET.SubElement(jacoco_plugin, "{}artifactId".format(namespace))
    jacoco_plugin_artifactId.text = "jacoco-maven-plugin"
    jacoco_plugin_version = ET.SubElement(jacoco_plugin, "{}version".format(namespace))
    jacoco_plugin_version.text = "0.8.7"  # Use the latest version

    # Add executions element
    executions = ET.SubElement(jacoco_plugin, "{}executions".format(namespace))

    # Add prepare-agent goal
    prepare_agent_execution = ET.SubElement(executions, "{}execution".format(namespace))
    prepare_agent_goals = ET.SubElement(prepare_agent_execution, "{}goals".format(namespace))
    prepare_agent_goal = ET.SubElement(prepare_agent_goals, "{}goal".format(namespace))
    prepare_agent_goal.text = "prepare-agent"

    # Add report goal
    report_execution = ET.SubElement(executions, "{}execution".format(namespace))
    report_execution_id = ET.SubElement(report_execution, "{}id".format(namespace))
    report_execution_id.text = "report"
    report_execution_phase = ET.SubElement(report_execution, "{}phase".format(namespace))
    report_execution_phase.text = "test"
    report_goals = ET.SubElement(report_execution, "{}goals".format(namespace))
    report_goal = ET.SubElement(report_goals, "{}goal".format(namespace))
    report_goal.text = "report"

    # Add JaCoCo plugin configuration to the plugins section
    plugins.append(jacoco_plugin)

    # Save the modified XML back to the file
    tree.write(pom_file, encoding="utf-8", xml_declaration=True)

def remove_ns0_from_xml(pom_file):
    # Load the XML file
    tree = ET.parse(pom_file)
    root = tree.getroot()

    # Iterate through all elements and attributes and replace ns0
    for elem in root.iter():
        if 'ns0' in elem.tag:
            elem.tag = elem.tag.replace('ns0:', '')

        for key, value in elem.attrib.items():
            if 'ns0' in value:
                elem.attrib[key] = value.replace('ns0:', '')

    # Save the modified XML back to the file
    tree.write(pom_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/pom.xml")
        sys.exit(1)

    pom_file_path = sys.argv[1]
    add_jacoco_configuration(pom_file_path)
    print(f"JaCoCo configuration added to {pom_file_path}")

    remove_ns0_from_file(pom_file_path)
    print(f"Removed 'ns0' occurrences from {pom_file_path}")
