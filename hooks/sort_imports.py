import sys
import subprocess

def main():
    # Define the command to run
    command = ['dart', 'run', 'import_sorter:main']

    # Run the command using subprocess
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    exit(0)
