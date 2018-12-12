#!/bin/bash
set -e

cd "$(dirname "$0")"
source ./openmdao-0.13.0/bin/activate

exec "$@"
