#!/usr/bin/env bash
# Run Dart analyze and check for errors
if ! output=$(dart analyze); then
    echo "COMMIT REJECTED: Dart analyze found the following errors:"
    echo "$output"
    exit 1
fi

exit 0
