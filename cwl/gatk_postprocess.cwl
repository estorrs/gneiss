class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: gneiss_align
baseCommand:
  - python
  - /gneiss/gneiss/gatk_postprocess.py
inputs:
  - id: input_bam
    type: File?
    inputBinding:
      position: 99
  - id: reference_fasta
    type: File
    inputBinding:
      position: 0
      prefix: '--reference-fasta'
  - id: known_sites
    type: File?
    inputBinding:
      position: 0
      prefix: '--known-sites'
  - id: max_jvm_memory
    type: string?
    inputBinding:
      position: 0
      prefix: '--max-jvm-memory'
  - id: min_jvm_memory
    type: string?
    inputBinding:
      position: 0
      prefix: '--min-jvm-memory'
outputs:
  - id: output_bam
    type: File?
    outputBinding:
      glob: output.bam
label: gneiss_align
arguments:
  - position: 0
    prefix: '--output'
    valueFrom: output.bam
requirements:
  - class: DockerRequirement
    dockerPull: 'estorrs/gneiss:0.0.6'
