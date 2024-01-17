import subprocess
import sys
import os
# Function to clone the repository from GitHub
def clone_repository(url):
    subprocess.run(['mkdir', 'gitDir'])
    subprocess.run(['git', 'clone', url, 'gitDir'])

# Function to run injectJacoco.py
def run_inject_jacoco():
    subprocess.run(['python3', 'injectJacoco.py', './gitDir/pom.xml'])

# Function to run sudo mvn clean test -Dmaven.test.failure.ignore=true
def run_maven_tests(url):
    os.chdir("gitDir")
    try:
        subprocess.run(['sudo', 'mvn', 'clean', 'test', '-Dmaven.test.failure.ignore=true', '-Drat.failOnError=false'], check=True)
    except subprocess.CalledProcessError:
        # Call cleanup function on error
        cleanup_on_fail(url)
        raise
    finally:
        # Change back to the original working directory
        os.chdir('..')
# Function to run summarizeCoverage.py
def run_summarize_coverage():
    subprocess.run(['python3', 'summarizeCoverage.py', './gitDir/'])

def cleanup_on_fail(url):
    with open("ErrorReport.txt", 'a') as file:
        file.write(f"There was an error with {url}\n")
    cleanup()
    
def cleanup():
    subprocess.run(['sudo', 'rm', '-rf', 'gitDir'])
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
    with open("CovLog.txt","a") as file:
        file.write(f"Looking at {url}\n")
    print(f"LOOKING AT {url}\n")
    try:
        clone_repository(url)
        run_inject_jacoco()
        run_maven_tests(url)
        run_summarize_coverage()
        cleanup()
    except Exception as e:
        cleanup_on_fail(url)
