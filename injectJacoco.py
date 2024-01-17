import sys
import xml.etree.ElementTree as ET

def add_jacoco_configuration(pom_file):
    # Load the XML file with namespace awareness
    tree = ET.parse(pom_file)
    root = tree.getroot()

    # Define JaCoCo plugin configuration without a namespace prefix
    ns = {'': 'http://maven.apache.org/POM/4.0.0'}
    jacoco_plugin = ET.Element("plugin", nsmap=ns)
    jacoco_plugin_groupId = ET.SubElement(jacoco_plugin, "groupId")
    jacoco_plugin_groupId.text = "org.jacoco"
    jacoco_plugin_artifactId = ET.SubElement(jacoco_plugin, "artifactId")
    jacoco_plugin_artifactId.text = "jacoco-maven-plugin"
    jacoco_plugin_version = ET.SubElement(jacoco_plugin, "version")
    jacoco_plugin_version.text = "0.8.7"  # Use the latest version

    # Add executions element
    executions = ET.SubElement(jacoco_plugin, "executions")

    # Add prepare-agent goal
    prepare_agent_execution = ET.SubElement(executions, "execution")
    prepare_agent_goals = ET.SubElement(prepare_agent_execution, "goals")
    prepare_agent_goal = ET.SubElement(prepare_agent_goals, "goal")
    prepare_agent_goal.text = "prepare-agent"

    # Add report goal
    report_execution = ET.SubElement(executions, "execution")
    report_execution_id = ET.SubElement(report_execution, "id")
    report_execution_id.text = "report"
    report_execution_phase = ET.SubElement(report_execution, "phase")
    report_execution_phase.text = "test"
    report_goals = ET.SubElement(report_execution, "goals")
    report_goal = ET.SubElement(report_goals, "goal")
    report_goal.text = "report"

    # Find the build section or create one if it doesn't exist
    build = root.find(".//build", ns)

    if build is None:
        build = ET.SubElement(root, "build")

    # Find the plugins section or create one if it doesn't exist
    plugins = build.find(".//plugins", ns)

    if plugins is None:
        plugins = ET.SubElement(build, "plugins")

    # Add JaCoCo plugin configuration to the plugins section
    plugins.append(jacoco_plugin)

    # Save the modified XML back to the file
    tree.write(pom_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/pom.xml")
        sys.exit(1)

    pom_file_path = sys.argv[1]
    add_jacoco_configuration(pom_file_path)
    print(f"JaCoCo configuration added to {pom_file_path}")
