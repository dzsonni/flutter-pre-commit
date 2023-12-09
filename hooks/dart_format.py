import subprocess

def main():
    # Define the command to run
    command = ['dart', 'format', '.', '--line-length=140']

    # Run the command using subprocess
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the output and error messages
    print(result.stdout)
    print(result.stderr)
    exit(0)
