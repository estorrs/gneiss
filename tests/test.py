import os
import shutil
import subprocess

import pytest

TEST_DATA_DIR = 'tests/data/'
TEST_FASTA_REFERENCE = TEST_DATA_DIR + 'test_ref.fa'
TEST_KNOWN_SITES = TEST_DATA_DIR + 'test_known_sites.vcf.gz'
TEST_GENOME_DIR = TEST_DATA_DIR + 'genome_dir'
TEST_OUTPUT_DIR = TEST_DATA_DIR + 'outputs'

TEST_READ_1 = TEST_DATA_DIR + 'reads_1.fq'
TEST_READ_2 = TEST_DATA_DIR + 'reads_2.fq'

TEST_READ_1_COMPRESSED = TEST_DATA_DIR + 'reads_1.fq.gz'
TEST_READ_2_COMPRESSED = TEST_DATA_DIR + 'reads_2.fq.gz'

TEST_POSTPROCESSING_BAM = TEST_DATA_DIR + 'test.postprocessing.bam'

def test_build_genome_dir():
    tool_args = ['python', 'gneiss/generate_genome_dir.py',
            '--threads', '2',
            '--reference-fasta', TEST_FASTA_REFERENCE,
            TEST_GENOME_DIR]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    # remove genome dir
    shutil.rmtree(TEST_GENOME_DIR)

    assert 'finished successfully' in results

def test_aligner_single_pass():
    tool_args = ['python', 'gneiss/gneiss.py',
            '--threads', '2',
            '--output-dir', TEST_OUTPUT_DIR,
            '--reference-fasta', TEST_FASTA_REFERENCE,
            TEST_READ_1, TEST_READ_2]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    assert 'finished successfully' in results

def test_aligner_two_pass_with_postprocessing():
    tool_args = ['python', 'gneiss/gneiss.py',
            '--threads', '2',
            '--output-dir', TEST_OUTPUT_DIR,
            '--reference-fasta', TEST_FASTA_REFERENCE,
            '--known-sites', TEST_KNOWN_SITES,
            '--two-pass',
            '--gatk-postprocessing',
            TEST_READ_1, TEST_READ_2]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    assert 'finished successfully' in results

def test_star_aligner_compressed_input():
    tool_args = ['python', 'gneiss/gneiss.py',
            '--threads', '2',
            '--output-dir', TEST_OUTPUT_DIR,
            '--reference-fasta', TEST_FASTA_REFERENCE,
            '--compressed-input',
            TEST_READ_1_COMPRESSED, TEST_READ_2_COMPRESSED]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    assert 'finished successfully' in results

def test_gatk_postprocess_only():
    # remove .faidx and .dict file from prev run
    os.remove(TEST_FASTA_REFERENCE.replace('.fa', '.dict'))
    os.remove(TEST_FASTA_REFERENCE + '.fai')
    os.remove(TEST_KNOWN_SITES + '.tbi')
    tool_args = ['python', 'gneiss/gatk_postprocess.py',
            '--output', 'postprocessed_output.bam',
            '--reference-fasta', TEST_FASTA_REFERENCE,
            '--known-sites', TEST_KNOWN_SITES,
            TEST_POSTPROCESSING_BAM]
    
    results = subprocess.check_output(tool_args).decode('utf-8')

    assert True
