# Variant Calling Pipeline for SE/PE illumina reads

## The pipeline runs sequentially as follows:

>1. Pre-Processing Raw reads using Trimmomatic
>2. Read Alignment using BWA
>3. Post-Alignment steps using SAMTOOLS, GATK, PICARD, Bedtools etc
>4. Variant Calling using SAMTOOLS
>5. Variant Filtering and generating Consensus using GATK, Bedtools, vcftools, in-house scripts etc.


**Usage:**

```
python pipeline.py [-h] -PE1 path-to-forward-PE-read -PE2 path-to-reverse-PE-read -o path-to-OUTPUT_FOLDER -analysis ANALYSIS_NAME -index INDEX_NAME_as_per_config_file -config path-to-config-file
```
**Note:**

- Input file format and extension: Either .fastq or .fastq.gz
- Output Directory: Pipeline creates output folder by output directory name mentioned at the end of the path. e.g: -o /any-path-followed-by/output_directory-name/
- ANALYSIS_NAME: Name by which pipeline saves the results inside output directory. e.g: -analysis first_analysis
- INDEX: Reference Index Name as mentioned under the section 'Reference Genome to be used for pipeline'. 
  e.g: In config file; under the section [KPNIH1], mention the attributes REF_NAME and REF_PATH for reference fasta filename and path to the reference fasta file resp. The section name KPNIH1 is required by the INDEX argument.
- config: Path to your customized config file. Make sure the section names are similar to the default config file.

**Customizing Config file:**

The pipeline implements customisable variant calling configurations using config file. Config file can be customised to use your choice of aligner and variant caller by changing two parameters under the section [pipeline]

```
# Set which tools to use in pipeline:
[pipeline]
# Options for Aligner:bwa / smalt / bowtie
aligner: bwa
# Options for variant_caller:  gatkhaplotypecaller /samtools
variant_caller: samtools
```

Currently, The pipeline supports BWA aligner(mem algorithm) for aligning reads to the reference genome and samtools for variant calling.

Parameters for each tools can be customised under the 'tool_parameter' attribute of each tool in config file.
