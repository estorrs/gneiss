class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: gneiss_align
baseCommand:
  - python
  - /gneiss/gneiss/gneiss.py
inputs:
  - id: genome_dir
    type: Directory
    inputBinding:
      position: 0
      prefix: '--genome-dir'
  - id: threads
    type: int?
    inputBinding:
      position: 0
      prefix: '--threads'
  - id: read_1_fastq
    type: File?
    inputBinding:
      position: 98
  - id: read_2_fastq
    type: File?
    inputBinding:
      position: 99
outputs:
  - id: output_bam
    type: File?
    outputBinding:
      glob: gneiss/gneiss/outputs/Aligned.sortedByCoord.out.bam
label: gneiss_align
arguments:
  - position: 0
    prefix: '--output-dir'
    valueFrom: /gneiss/cwl/outputs
requirements:
  - class: DockerRequirement
    dockerPull: estorrs/gneiss
