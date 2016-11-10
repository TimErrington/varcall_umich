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

**Output**:

The pipeline generates various output files from different tools at different steps. The most notable ones are:
- Clean reads: *.fq.gz files from trimmomatic.

- Alignemnet files: analysisname_aln.sam and analysisname_aln.bam from BWA, analysisname_aln_marked.bam from GATK MarkDuplicates, and finally a sorted BAM from marked bam file analysisname_aln_sort.bam. Also including *bai index files.
- Bed file: analysisname_unmapped.bed and analysisname_unmapped.bed_positions with positions that were unmapped. Bedcoverage file analysisname_.bedcov

- VCF file: Various vcf files are generated removing different types of variants at different steps.
>1. analysisname_aln_mpileup_raw.vcf: The raw variant calls without any variant filtering
>2. analysisname_aln_mpileup_raw.vcf_5bp_indel_removed.vcf.gz: variants that proximate to an indel by 5 bp are filtered out
>3. analysisname_filter2_gatk.vcf: variants filtered out using GATK variant filter parameters(parameters can be changed in config file) + variants that are proximate to an indel by 5 bp are filtered out
>4. analysisname_final.vcf_no_proximate_snp.vcf.gz: variants filtered out using GATK variant filter parameters(parameters can be changed in config file) + variants that are proximate to an indel by 5 bp are filtered out + variants that are proximate to each other by 5 bp 

- Statistics Reports:
>1. analysisname_alignment_stats: Alignment stats file generated using SAMTOOLS flagstat.
>2. analysisname_vcf_stats: vcf stats(raw) generated using vcftools
>3. analysisname_depth_of_coverage*: Depth of Coverage generated using GATK Depth of Coverage.
>4. analysisname_markduplicates_metrics: Mark Duplicates metrics generated during Picard Mark Duplicates step.
>5. analysisname_report.pdf and genome_results.txt: generated using Qualimap bamQC.

**Log:**

The pipeline generates a log file following the naming convention: yyyy_mm_dd_hrs_mins_secs_analysisname.log.txt
Each and every step of the pipeline is logged into the log file and the log file sections follows the standard Python log naming conventions: INFO to print STDOUT messages, DEBUG to print commands ran by pipeline, ERROR to print STDERR messages and EXCEPTION to print an exception that occured while the pipeline was running.
