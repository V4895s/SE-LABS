#!/usr/bin/env bash
# Usage: ./run_analysis.sh before   (or: after)
set -u
tag=${1:-before}
pylint wildlife_sightings.py  > pylint_report_$tag.txt
bandit -r wildlife_sightings.py > bandit_report_$tag.txt
flake8 wildlife_sightings.py  > flake8_report_$tag.txt
tail -n 3 pylint_report_$tag.txt
