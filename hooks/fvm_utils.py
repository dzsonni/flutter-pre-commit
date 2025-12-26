"""FVM (Flutter Version Manager) detection utilities.

This module provides functions to detect project-specific Flutter/Dart
versions configured via FVM and resolve the correct executable paths.
"""

import json
from pathlib import Path


def find_fvmrc() -> Path | None:
    """Find .fvmrc file by walking up from current directory.

    Returns:
        Path to .fvmrc if found, None otherwise.
    """
    current = Path.cwd()
    for parent in [current, *current.parents]:
        fvmrc = parent / '.fvmrc'
        if fvmrc.exists():
            return fvmrc
    return None


def get_flutter_version() -> str | None:
    """Get Flutter version from FVM configuration.

    Checks for:
    1. .fvmrc file (new FVM format) in current or parent directories
    2. .fvm/fvm_config.json (legacy FVM format) in current directory

    Returns:
        Flutter version string if configured, None otherwise.
    """
    # Check .fvmrc first (new format)
    fvmrc = find_fvmrc()
    if fvmrc:
        try:
            config = json.loads(fvmrc.read_text())
            version = config.get('flutter')
            if version:
                return version
        except (json.JSONDecodeError, IOError):
            pass

    # Check legacy .fvm/fvm_config.json
    current = Path.cwd()
    for parent in [current, *current.parents]:
        fvm_config = parent / '.fvm' / 'fvm_config.json'
        if fvm_config.exists():
            try:
                config = json.loads(fvm_config.read_text())
                version = config.get('flutterSdkVersion')
                if version:
                    return version
            except (json.JSONDecodeError, IOError):
                pass

    return None


def get_dart_executable() -> str:
    """Get path to Dart executable, preferring FVM if configured.

    Resolution order:
    1. Project FVM configuration (.fvmrc or .fvm/fvm_config.json)
    2. System dart from PATH

    Returns:
        Path to dart executable or 'dart' for system fallback.
    """
    version = get_flutter_version()
    if version:
        # Standard FVM installation paths
        fvm_paths = [
            Path.home() / 'fvm' / 'versions' / version / 'bin' / 'dart',
            Path.home() / '.fvm' / 'versions' / version / 'bin' / 'dart',
        ]
        for dart_path in fvm_paths:
            if dart_path.exists():
                return str(dart_path)

    # Fallback to system dart
    return 'dart'
