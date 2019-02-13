import argparse
import os
import shutil
import subprocess

import postprocessing

parser = argparse.ArgumentParser()

parser.add_argument('input_bam', type=str,
        help='input bam to be processed for GATK rna-seq calling pipeline.')

reference_fasta_group = parser.add_argument_group('reference_fasta_group')
reference_fasta_group.add_argument('--reference-fasta', type=str,
        help='reference fasta to use for alignment')
gtf_group = parser.add_argument_group('gtf_group')
gtf_group.add_argument('--gtf', type=str,
        help='gtf to use for aligment')
known_sites_group = parser.add_argument_group('known_sites')
known_sites_group.add_argument('--known-sites', type=str,
        help='A compressed vcf (.vcf.gz) with known sites to be used during base recalibration.  \
used in conjunction with --gatk-postprocessing')

parser.add_argument('--output', type=str,
        default='output.bam', help='name of output bam')
parser.add_argument('--min-jvm-memory', type=str,
        default='64m', help='Minimum memory to give java JVM.')
parser.add_argument('--max-jvm-memory', type=str,
        default='1g', help='Maximum memory to give java JVM.')

args = parser.parse_args()

def check_arguments():
    if args.reference_fasta is None:
        raise ValueError('Must specify --reference-fasta')

    # if gatk postprocessing then known sites must be present
    if args.known_sites is None:
        raise ValueError('You must supply a .vcf.gz with konwn sites using the --known-sites flag')
        
    if args.known_sites[-3:] != '.gz':
        raise ValueError('--known-sites must be compressed with bgzip and have extension .gz')

def main():
    check_arguments()

    # do gatk postprocessing if necessary
    postprocessing.run_postprocessing(args.input_bam, args.output, args.reference_fasta,
            args.known_sites, min_memory=args.min_jvm_memory, max_memory=args.max_jvm_memory)

if __name__ == '__main__':
    main()
