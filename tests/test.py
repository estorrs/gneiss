import os
import subprocess

import pytest

TEST_DATA_DIR = 'tests/data/'
TEST_FASTA_REFERENCE = TEST_DATA_DIR + 'test_ref.fa'
TEST_GENOME_DIR = TEST_DATA_DIR + 'genome_dir'
TEST_OUTPUT_DIR = TEST_DATA_DIR + 'outputs'

TEST_READ_1 = TEST_DATA_DIR + 'reads_1.fq'
TEST_READ_2 = TEST_DATA_DIR + 'reads_2.fq'

TEST_READ_1_COMPRESSED = TEST_DATA_DIR + 'reads_1.fq.gz'
TEST_READ_2_COMPRESSED = TEST_DATA_DIR + 'reads_2.fq.gz'

def test_build_genome_dir():
    tool_args = ['python', 'gneiss/generate_genome_dir.py',
            '--threads', '2',
            '--reference-fasta', TEST_FASTA_REFERENCE,
            TEST_GENOME_DIR]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    assert 'finished successfully' in results

def test_star_aligner():
    tool_args = ['python', 'gneiss/gneiss.py',
            '--threads', '2',
            '--output-dir', TEST_OUTPUT_DIR,
            '--genome-dir', TEST_GENOME_DIR,
            TEST_READ_1, TEST_READ_2]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    assert 'finished successfully' in results

def test_star_aligner_compressed_input():
    tool_args = ['python', 'gneiss/gneiss.py',
            '--threads', '2',
            '--output-dir', TEST_OUTPUT_DIR,
            '--genome-dir', TEST_GENOME_DIR,
            '--compressed-input',
            TEST_READ_1_COMPRESSED, TEST_READ_2_COMPRESSED]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    assert 'finished successfully' in results
