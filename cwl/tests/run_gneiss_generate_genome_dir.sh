#!/bin/bash

CWL="/diskmnt/Projects/Users/estorrs/gneiss/cwl/gneiss_generate_genome_dir.cwl"
YAML="/diskmnt/Projects/Users/estorrs/gneiss/cwl/tests/gneiss_generate_genome_dir_config.yaml"

mkdir -p /diskmnt/Projects/Users/estorrs/gneiss/cwl/tests/test_results/generate
RABIX_ARGS="--basedir /diskmnt/Projects/Users/estorrs/gneiss/cwl/tests/test_results/generate"

rabix $RABIX_ARGS $CWL $YAML
