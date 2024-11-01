import subprocess

def main():
    # Define the command to run
    command = ['dart', 'analyze']

    # Run the command using subprocess
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the output and error messages
    print(result.stdout)
    print(result.stderr)

    # Check the return code and exit with an error if it's not 0
    if result.returncode != 0:
        exit(1)
