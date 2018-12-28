import argparse
import os
import shutil
import subprocess

import postprocessing

GENOME_DIR = 'genome_dir'
GENOME_DIR_SECOND_PASS = 'genome_dir_second_pass'
TAB_NAME = 'SJ.out.tab'
ALIGNER_OUTPUT_NAME = 'Aligned.sortedByCoord.out.bam'
POSTPROCESSED_OUTPUT_NAME = 'Aligned.sortedByCoord.out.postprocessed.bam'


parser = argparse.ArgumentParser()

parser.add_argument('fastq_1', type=str,
        help='read 1 fastq')
parser.add_argument('fastq_2', type=str,
        help='read 2 fastq')

reference_fasta_group = parser.add_argument_group('reference_fasta_group')
reference_fasta_group.add_argument('--reference-fasta', type=str,
        help='reference fasta to use for alignment')
gtf_group = parser.add_argument_group('gtf_group')
gtf_group.add_argument('--gtf', type=str,
        help='gtf to use for aligment')

parser.add_argument('--output-dir', type=str,
        help='Directory to store output in')
parser.add_argument('--known-sites', type=str,
        help='A compressed vcf (.vcf.gz) with known sites to be used during base recalibration.  \
used in conjunction with --gatk-postprocessing')
parser.add_argument('--threads', type=int,
        default=1, help='how many processes to allow tools to use')
parser.add_argument('--compressed-input',
        action="store_true", help='how many processes to allow tools to use')
parser.add_argument('--two-pass',
        action="store_true", help='preform a two pass alignment with STAR')
parser.add_argument('--gatk-postprocessing',
        action="store_true", help='Do postprocessing recommended by gatk for rna-seq calling. \
Must provide a compressed vcf.gz file with known polymorphisms for base recalibration using \
the --known-sites flag')

args = parser.parse_args()

def check_arguments():
    if args.reference_fasta is None:
        raise ValueError('Must specify --reference-fasta')

    # if gatk postprocessing then known sites must be present
    if args.gatk_postprocessing and args.known_sites is None:
        raise ValueError('If doing gatk postprocessing, you must supply a .vcf.gz with konwn \
sites using the --known-sites flag')
        
        if args.known_sites[:-3] != '.gz':
            raise ValueError('--known-sites must be compressed with bgzip and have extension .gz')

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

def run_star_aligner(read_1_fp, read_2_fp, genome_dir_fp, output_dir_fp, threads=1,
        compressed=False):
    # add slash if not there
    if output_dir_fp[-1] != '/':
        output_dir_fp += '/'

    # make output directory if it doesn't exist yet
    if not os.path.exists(output_dir_fp):
        os.makedirs(output_dir_fp)

    tool_args = ['STAR',
        '--runThreadN', str(threads),
        '--genomeDir', genome_dir_fp,
        '--outFileNamePrefix', output_dir_fp,
        '--outSAMtype', 'BAM', 'SortedByCoordinate']

    if compressed:
        tool_args += ['--readFilesCommand', 'zcat']

    tool_args += ['--readFilesIn', read_1_fp, read_2_fp]
    print('gneiss starting alignment')
    print(f'executing the following: {" ".join(tool_args)}')
    print(subprocess.check_output(tool_args).decode('utf-8'))

def main():
    check_arguments()

    # generate initial genome dir
    generate_genome_dir(GENOME_DIR, args.reference_fasta, args.gtf, threads=args.threads)
    # run aligner first pass
    run_star_aligner(args.fastq_1, args.fastq_2, GENOME_DIR, args.output_dir,
            threads=args.threads, compressed=args.compressed_input)

    # run second pass if desired
    if args.two_pass:
        # generate genome dir with the output tab file of previous run
        generate_genome_dir(GENOME_DIR_SECOND_PASS, args.reference_fasta, args.gtf,
                threads=args.threads, tab_fp=os.path.join(args.output_dir, TAB_NAME))

        # run aligner second pass
        run_star_aligner(args.fastq_1, args.fastq_2, GENOME_DIR_SECOND_PASS, args.output_dir,
                threads=args.threads, compressed=args.compressed_input)

        # clean up second genome dir
        shutil.rmtree(GENOME_DIR_SECOND_PASS)

    # clean up genome directory
    shutil.rmtree(GENOME_DIR)

    # do gatk postprocessing if necessary
    if args.gatk_postprocessing:
        postprocessing.run_postprocessing(os.path.join(args.output_dir, ALIGNER_OUTPUT_NAME),
                os.path.join(args.output_dir, POSTPROCESSED_OUTPUT_NAME), args.reference_fasta,
                args.known_sites)

        # remove initial bam
        os.remove(os.path.join(args.output_dir, ALIGNER_OUTPUT_NAME))
        

if __name__ == '__main__':
    main()
