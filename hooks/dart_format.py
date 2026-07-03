import subprocess
import sys

from hooks.fvm_utils import get_dart_executable


def main():
    # pre-commit passes the staged .dart files as arguments. Format only those —
    # never the whole repo ('.') — so a commit can't sweep unrelated files into a
    # formatter-version reformat, which would surface as spurious cross-file drift.
    files = sys.argv[1:]
    if not files:
        return

    dart = get_dart_executable()
    command = [dart, 'format', '--line-length=140', *files]

    result = subprocess.run(command, text=True, capture_output=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    exit(0)
