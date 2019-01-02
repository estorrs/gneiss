import os
import re
import subprocess

TEMP_BAM_NAME = 'temp.bam'
TABLE_NAME = 'output.table'

def prepare_known_sites(known_sites_fp):
    """make sure known sites is indexed"""
    tool_args = ['tabix', '-p', 'vcf', known_sites_fp]
    print('preparing known sites')
    print(f'executing the following command: {" ".join(tool_args)}') 
    print(subprocess.check_output(tool_args))

def prepare_reference(reference_fp):
    """prepares reference for gatk.

    This involves creating a .fai and .dict file
    """
    tool_args = ['samtools', 'faidx', reference_fp]
    print('preparing reference')
    print(f'executing the following command: {" ".join(tool_args)}') 
    print(subprocess.check_output(tool_args))

    tool_args = ['picard', 'CreateSequenceDictionary',
            f'R={reference_fp}',
            'O=' + re.sub(r'.[^.]*$', '.dict', reference_fp)]
    print(f'executing the following command: {" ".join(tool_args)}') 
    print(subprocess.check_output(tool_args))

def sort_and_add_read_groups(input_bam_fp, output_bam_fp):
    """sort and add readgroups"""
    tool_args = ['picard', 'AddOrReplaceReadGroups',
            f'I={input_bam_fp}',
            f'O={output_bam_fp}',
            'SO=coordinate', 'RGID=id', 'RGLB=library',
            'RGPL=platform', 'RGPU=machine', 'RGSM=sample']

    print('sorting and adding read groups')
    print(f'executing the following command: {" ".join(tool_args)}') 
    print(subprocess.check_output(tool_args))

def mark_duplicates(input_bam_fp, output_bam_fp):
    """mark duplicates"""
    tool_args = ['picard', 'MarkDuplicates',
            f'I={input_bam_fp}',
            f'O={output_bam_fp}',
            'CREATE_INDEX=true', 'VALIDATION_STRINGENCY=SILENT', 'M=output.metrics']

    print('marking duplicate reads')
    print(f'executing the following command: {" ".join(tool_args)}') 
    print(subprocess.check_output(tool_args))

def split_and_trim(input_bam_fp, output_bam_fp, reference_fp):
    """split and trim reads.
    
    note: in gatk4 mapping quality is automatically reassigned from 255 to 60
    """
    tool_args = ['gatk', 'SplitNCigarReads',
            '-R', reference_fp,
            '-I', input_bam_fp,
            '-O', output_bam_fp]

    print('spliting, trimming, and reassigning reads from 255 to 60')
    print(f'executing the following command: {" ".join(tool_args)}') 
    print(subprocess.check_output(tool_args))
    
def base_recalibration(input_bam_fp, output_bam_fp, reference_fp, known_sites_fp,
        table_fp='output.table'):
    """do base recalibration"""
    tool_args = ['gatk', 'BaseRecalibrator',
            '-I', input_bam_fp,
            '-R', reference_fp,
            '--known-sites', known_sites_fp,
            '-O', table_fp]

    print('creating base recalibration model')
    print(f'executing the following command: {" ".join(tool_args)}') 
    print(subprocess.check_output(tool_args))

    tool_args = ['gatk', 'ApplyBQSR',
            '-I', input_bam_fp,
            '-R', reference_fp,
            '--bqsr-recal-file', table_fp,
            '-O', output_bam_fp]

    print('running base recalibration')
    print(f'executing the following command: {" ".join(tool_args)}') 
    print(subprocess.check_output(tool_args))

def remove_files(fps):
    for fp in fps:
        os.remove(fp)

def run_postprocessing(input_bam_fp, output_bam_fp, reference_fp, known_sites_fp):
    """run gatk recommended rna-seq bam postprocessing steps"""
    # make sure known sites is indexed
    prepare_known_sites(known_sites_fp)
    # make sure reference has .fai and .dict
    prepare_reference(reference_fp)
    
    # picard sorting, read groups, and deduping
    sort_and_add_read_groups(input_bam_fp, 'temp.bam')
    mark_duplicates('temp.bam', 'temp.2.bam')
    remove_files(['temp.bam'])
    
    # do recommended trimming
    split_and_trim('temp.2.bam', 'temp.3.bam', reference_fp)
    remove_files(('temp.2.bam', 'temp.2.bai'))

    # do base recalibration
    base_recalibration('temp.3.bam', output_bam_fp, reference_fp, known_sites_fp,
            table_fp=TABLE_NAME)

    # clean up temp files
    remove_files(('temp.3.bam', 'temp.3.bai', TABLE_NAME, 'output.metrics'))
