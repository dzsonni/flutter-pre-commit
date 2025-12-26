import subprocess

from hooks.fvm_utils import get_dart_executable


def main():
    dart = get_dart_executable()
    command = [dart, 'analyze']

    result = subprocess.run(command, text=True, capture_output=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        exit(1)
