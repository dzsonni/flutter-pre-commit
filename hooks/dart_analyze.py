import subprocess

# Define the command to run dart analyze
command = ["dart", "analyze"]

# Run the command using subprocess
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Print the output of the command
print(result.stdout.decode())
print(result.stderr.decode())

# Check if the command was successful
if result.returncode != 0:
    print("Dart analyze failed. Please fix the errors and try again.")
    exit(1)
