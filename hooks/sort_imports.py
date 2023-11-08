import sys
import subprocess

def main():
    # Define the command to run
    command = ['dart', 'run', 'import_sorter:main']

    # Run the command using subprocess
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the output and error messages
    print(result.stdout.decode(sys.stdout.encoding, errors='ignore'))
    print(result.stderr.decode(sys.stdout.encoding, errors='ignore'))

    # Check the return code and exit with an error if it's not 0
    if result.returncode != 0:
        exit(1)
