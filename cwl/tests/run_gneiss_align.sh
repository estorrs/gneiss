#!/bin/bash

CWL="cwl/gneiss_align.cwl"
YAML="cwl/tests/gneiss_align_config.yaml"

mkdir -p cwl/tests/test_results/align
RABIX_ARGS="--basedir cwl/tests/test_results/align"

rabix $RABIX_ARGS $CWL $YAML
