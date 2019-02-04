#!/bin/bash

CWL="cwl/gatk_postprocess.cwl"
YAML="cwl/tests/gatk_postprocess_config.yaml"

mkdir -p cwl/tests/test_results/postprocess
RABIX_ARGS="--basedir cwl/tests/test_results/postprocess"

rabix $RABIX_ARGS $CWL $YAML
