import xml.etree.ElementTree as ET
import sys
def get_line_coverage_percentage(jacoco_xml_file):
    tree = ET.parse(jacoco_xml_file)
    root = tree.getroot()

    # Find the counter elements for lines
    counters = root.findall(".//counter[@type='LINE']")

    # Extract covered and missed line counts
    covered_lines = 0
    missed_lines = 0
    for count in counters:
        covered_lines = covered_lines + int(count.get("covered"))
        missed_lines = missed_lines + int(count.get("missed"))
    print(f"Number of covered_lines {covered_lines}")
    print(f"Number of missed_lines {missed_lines}")
    # Calculate line coverage percentage
    total_lines = covered_lines + missed_lines
    line_coverage_percentage = (covered_lines / total_lines) * 100 if total_lines > 0 else 100

    return line_coverage_percentage

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py path/to/root/   githubURL")
        sys.exit(1)
    jacoco_xml_path = sys.argv[1] + "target/site/jacoco/jacoco.xml"# Replace with the actual path to your jacoco.xml
    line_coverage_percentage = get_line_coverage_percentage(jacoco_xml_path)
    with open("CovReport.txt", 'a') as file:
        file.write(f"Line Coverage Percentage: {line_coverage_percentage:.2f}%\n for {sys.argv[2]}")
    print(f"Line Coverage Percentage: {line_coverage_percentage:.2f}%")