#!/bin/bash

CWL="cwl/gneiss_align.cwl"
YAML="cwl/tests/gneiss_align_config.yaml"

mkdir -p cwl/tests/results
RABIX_ARGS="--basedir cwl/tests/results"

rabix $RABIX_ARGS $CWL $YAML
