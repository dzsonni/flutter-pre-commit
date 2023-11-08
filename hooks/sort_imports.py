import subprocess

def main():
    # Define the command to run
    command = ['dart', 'run', 'import_sorter:main']

    # Run the command using subprocess
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the output and error messages
    print(result.stdout.decode('utf-8'))
    print(result.stderr.decode('utf-8'))

    # Check the return code and exit with an error if it's not 0
    if result.returncode != 0:
        exit(1)
