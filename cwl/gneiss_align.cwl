class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: gneiss_align
baseCommand:
  - python
  - /gneiss/gneiss/gneiss.py
inputs:
  - id: threads
    type: int?
    inputBinding:
      position: 0
      prefix: '--threads'
  - id: compressed_input
    type: boolean?
    inputBinding:
      position: 0
      prefix: '--compressed-input'
  - id: gatk_postprocessing
    type: boolean?
    inputBinding:
      position: 0
      prefix: '--gatk-postprocessing'
  - id: read_1_fastq
    type: File?
    inputBinding:
      position: 98
  - id: read_2_fastq
    type: File?
    inputBinding:
      position: 99
  - id: reference_fasta
    type: File
    inputBinding:
      position: 0
      prefix: '--reference-fasta'
  - id: gtf
    type: File?
    inputBinding:
      position: 0
      prefix: '--gtf'
  - id: known_sites
    type: File?
    inputBinding:
      position: 0
      prefix: '--known-sites'
  - id: two_pass
    type: boolean?
    inputBinding:
      position: 0
      prefix: '--two-pass'
outputs:
  - id: output_bam
    type: File?
    outputBinding:
      glob: gneiss_outputs/Aligned.sortedByCoord.out*bam
label: gneiss_align
arguments:
  - position: 0
    prefix: '--output-dir'
    valueFrom: gneiss_outputs
requirements:
  - class: DockerRequirement
    dockerPull: 'estorrs/gneiss:0.0.3'
