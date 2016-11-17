# Variant Calling Pipeline for SE/PE illumina reads

## The pipeline runs sequentially as follows:
***

>1. Pre-Processing Raw reads using [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic)
>2. Read Alignment using [BWA](http://bio-bwa.sourceforge.net/)
>3. Post-Alignment steps using [SAMTOOLS](http://samtools.sourceforge.net/), [GATK](https://software.broadinstitute.org/gatk/), [PICARD](https://broadinstitute.github.io/picard/), [Bedtools]() etc
>4. Variant Calling using [SAMTOOLS](http://samtools.sourceforge.net/)
>5. Variant Filtering and generating Consensus using [GATK](https://software.broadinstitute.org/gatk/), [Bedtools](http://bedtools.readthedocs.io/en/latest/), [vcftools](http://vcftools.sourceforge.net/), in-house scripts() etc.


**Usage:**
***

```
python pipeline.py [-h] -PE1 path-to-forward-PE-read -PE2 path-to-reverse-PE-read -o path-to-OUTPUT_FOLDER -analysis ANALYSIS_NAME -index INDEX_NAME_as_per_config_file -config path-to-config-file
```
**Note:**
***

- ***Input file format and extension***: Either .fastq or .fastq.gz
- ***Output Directory***: Pipeline creates output folder by output directory name mentioned at the end of the path. e.g: -o /any-path-followed-by/output_directory-name/
- ***ANALYSIS_NAME***: Name by which pipeline saves the results inside output directory. e.g: -analysis first_analysis
- ***INDEX***: Reference Index Name as mentioned under the section 'Reference Genome to be used for pipeline'. 
  e.g: In config file; under the section [KPNIH1], mention the attributes REF_NAME and REF_PATH for reference fasta filename and path to the reference fasta file resp. The section name KPNIH1 is required by the INDEX argument.
- config: Path to your customized config file. Make sure the section names are similar to the default config file.

**Customizing Config file:**
***

The pipeline implements customisable variant calling configurations using config file. Config file can be customised to use your choice of aligner and variant caller by changing two parameters under the section [pipeline]

```
# Set which tools to use in pipeline:
[pipeline]
# Options for Aligner:bwa / smalt / bowtie
aligner: bwa
# Options for variant_caller:  gatkhaplotypecaller /samtools
variant_caller: samtools

# Set bin folder path. 
[bin_path]
#binbase: /scratch/micro612w16_fluxod/shared/bin/
binbase: /home/apirani/bin/
```

Make sure all the executablesdependencies are placed in bin folder supplies with binbase under section [bin_path]. 
NOTE: Add the required perl libraries(such as in the case of vcftools) PERL5LIB environment variable. 


Currently, The pipeline supports BWA aligner(mem algorithm) for aligning reads to the reference genome and samtools for variant calling.

Parameters for each tools can be customised under the 'tool_parameter' attribute of each tool in config file.

**Output**:
***

The pipeline generates various output files from different tools at different steps. The most notable ones are:
- ***Clean reads***: *.fq.gz files from trimmomatic.

- ***Alignment files***: analysisname_aln.sam and analysisname_aln.bam from BWA, analysisname_aln_marked.bam from GATK MarkDuplicates, and finally a sorted BAM from marked bam file analysisname_aln_sort.bam. Also including *bai index files.
- ***Bed file***: analysisname_unmapped.bed and analysisname_unmapped.bed_positions with positions that were unmapped. Bedcoverage file analysisname_.bedcov

- ***VCF file***: Various vcf files are generated removing different types of variants at different steps.
>1. ***analysisname_aln_mpileup_raw.vcf***: The raw variant calls without any variant filtering
>2. ***analysisname_aln_mpileup_raw.vcf_5bp_indel_removed.vcf.gz***: variants that proximate to an indel by 5 bp are filtered out
>3. ***analysisname_filter2_gatk.vcf***: variants that does not pass the GATK variant filter parameters are filtered out(parameters can be changed in config file) + variants that are proximate to an indel by 5 bp are filtered out
>4. ***analysisname_final.vcf_no_proximate_snp.vcf.gz***: variants that does not pass the GATK variant filter parameters are filtered out(parameters can be changed in config file) + variants that are proximate to an indel by 5 bp are filtered out + variants that are proximate to each other by 5 bp 

- ***Statistics Reports***:
***
>1. ***analysisname_alignment_stats***: Alignment stats file generated using SAMTOOLS flagstat.
>2. ***analysisname_vcf_stats***: vcf stats(raw) generated using vcftools
>3. ***analysisname_depth_of_coverage***: Depth of Coverage generated using GATK Depth of Coverage.
>4. ***analysisname_markduplicates_metrics***: Mark Duplicates metrics generated during Picard Mark Duplicates step.
>5. ***analysisname_report.pdf*** and ***genome_results.txt***: generated using [Qualimap bamQC](http://qualimap.bioinfo.cipf.es/).

**Log:**
***

The pipeline generates a log file following the naming convention: yyyy_mm_dd_hrs_mins_secs_analysisname.log.txt and tracks each event/command run by the pipleine. The log file sections follow the standard [Python logging conventions](https://docs.python.org/2/howto/logging.html): 
***INFO*** to print STDOUT messages; ***DEBUG*** to print commands ran by pipeline, ***ERROR*** to print STDERR messages and ***EXCEPTION*** to print an exception that occured while the pipeline was running.
