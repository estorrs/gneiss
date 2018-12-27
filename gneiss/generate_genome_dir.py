import argparse
import os
import subprocess

"""
usage: generate_genome_dir.py genome_dir_fp [options]

args:
genome_dir_name: str
    name of genome directory

options:
--threads: int
    how many processes to allow STAR to use
--reference_fasta: str
    reference fasta
--gtf: str
    gtf file
"""

parser = argparse.ArgumentParser()

parser.add_argument('genome_dir_fp', type=str,
        help='what to name output genome dir')

reference_group = parser.add_argument_group('reference_group')
reference_group.add_argument('--reference-fasta', type=str,
        help='location of reference fasta')

parser.add_argument('--threads', type=int,
        default=1, help='how many processes to allow tophat and samtools to use')
parser.add_argument('--gtf', type=str,
        help='location of gtf file')

args = parser.parse_args()

def check_arguments():
    if args.reference_fasta is None:
        raise ValueError('Must specify a bowtie2 compatible reference fasta')

def generate_genome_dir(genome_dir_fp, reference_fp, gtf_fp, tab_fp=None, threads=1):
    # make sure genome_dir exists
    if not os.path.exists(genome_dir_fp):
        os.makedirs(genome_dir_fp)

    tool_args = ['STAR',
            '--runThreadN', str(threads),
            '--runMode', 'genomeGenerate',
            '--genomeDir', genome_dir_fp,
            '--genomeFastaFiles', reference_fp]
    
    if gtf_fp is not None:
        tool_args += ['--sjdbGTFfile', gtf_fp]

    if tab_fp is not None:
        tool_args += ['--sjdbFileChrStartEnd', tab_fp]

    print('creating genome directory')
    print(f'executing the following: {" ".join(tool_args)}')
    print(subprocess.check_output(tool_args).decode('utf-8'))

def main():
    check_arguments()
    
    generate_genome_dir(args.genome_dir_fp, args.reference_fasta, args.gtf, threads=args.threads)


if __name__ == '__main__':
    main()
