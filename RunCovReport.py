import subprocess
import sys
import os
# Function to clone the repository from GitHub
def clone_repository(url):
    subprocess.run(['mkdir', 'gitDir'])
    subprocess.run(['git', 'clone', url, 'gitDir'])

# Function to run injectJacoco.py
def run_inject_jacoco():
    subprocess.run(['python', 'injectJacoco.py', './gitDir/pom.xml'])

# Function to run sudo mvn clean test -Dmaven.test.failure.ignore=true
def run_maven_tests():
    os.chdir("gitDir")
    subprocess.run(['sudo', 'mvn', 'clean', 'test', '-Dmaven.test.failure.ignore=true'])
    os.chdir("..")
# Function to run summarizeCoverage.py
def run_summarize_coverage():
    subprocess.run(['python', 'summarizeCoverage.py', './gitDir/'])

# Read X (number of URLs) from command line arguments
if len(sys.argv) != 3:
    print("Usage: python script.py X inputFile")
    sys.exit(1)

try:
    x = int(sys.argv[1])
except ValueError:
    print("Error: X must be an integer")
    sys.exit(1)
    
input_file = sys.argv[2]

# Read URLs from file
with open(input_file, 'r') as file:
    urls = file.read().splitlines()

# Perform actions for each URL up to the first X
for url in urls[:x]:
    clone_repository(url)
    run_inject_jacoco()
    run_maven_tests()
    run_summarize_coverage()
