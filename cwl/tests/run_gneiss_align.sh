#!/bin/bash

CWL="/diskmnt/Projects/Users/estorrs/gneiss/cwl/gneiss_align.cwl"
YAML="/diskmnt/Projects/Users/estorrs/gneiss/cwl/tests/gneiss_align_config.yaml"

mkdir -p /diskmnt/Projects/Users/estorrs/gneiss/cwl/tests/test_results
RABIX_ARGS="--basedir /diskmnt/Projects/Users/estorrs/gneiss/cwl/tests/test_results"

rabix $RABIX_ARGS $CWL $YAML
