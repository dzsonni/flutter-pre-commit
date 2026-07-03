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


def find_local_fvm_dart() -> Path | None:
    """Find the project-local FVM SDK dart by walking up from the current dir.

    FVM symlinks the pinned SDK at ``<project>/.fvm/flutter_sdk``. This is the
    authoritative SDK for the project and takes priority over any global install,
    because it always matches what ``fvm flutter``/``fvm dart`` use here — even when
    the global versions directory is absent or holds a different set of versions.

    Returns:
        Path to ``.fvm/flutter_sdk/bin/dart`` if found, None otherwise.
    """
    current = Path.cwd()
    for parent in [current, *current.parents]:
        dart_path = parent / '.fvm' / 'flutter_sdk' / 'bin' / 'dart'
        if dart_path.exists():
            return dart_path
    return None


def find_global_fvm_dart() -> Path | None:
    """Find the global FVM SDK dart for the version configured in .fvmrc.

    Returns:
        Path to ``~/fvm/versions/<version>/bin/dart`` (or the legacy
        ``~/.fvm/versions/...`` location) if the configured version is installed
        globally, None otherwise.
    """
    version = get_flutter_version()
    if not version:
        return None
    for base in (Path.home() / 'fvm' / 'versions', Path.home() / '.fvm' / 'versions'):
        dart_path = base / version / 'bin' / 'dart'
        if dart_path.exists():
            return dart_path
    return None


def get_dart_executable() -> str:
    """Get path to the Dart executable, preferring the project's FVM SDK.

    Resolution order (highest priority first):
    1. Project-local FVM SDK — ``<project>/.fvm/flutter_sdk/bin/dart``.
    2. Global FVM SDK for the ``.fvmrc`` version — ``~/fvm/versions/<version>/bin/dart``.
    3. System ``dart`` from PATH (fallback).

    Returns:
        Absolute path to a dart executable, or ``'dart'`` for the system fallback.
    """
    local_dart = find_local_fvm_dart()
    if local_dart:
        return str(local_dart)

    global_dart = find_global_fvm_dart()
    if global_dart:
        return str(global_dart)

    # Fallback to system dart on PATH.
    return 'dart'
