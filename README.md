# varcall_umich
Automated analysis of Illumina PE data for Variant Calling.

Usage: python pipeline.py [-h] -PE1 path-to-forward-PE-read -PE2 path-to-reverse-PE-read -o path-to-OUTPUT_FOLDER -analysis ANALYSIS_NAME -index INDEX_NAME_as_per_config_file
       
Note:

Input file format: Either .fastq or .fastq.gz

Output Directory: Pipeline creates output folder by output directory name mentioned at the end of the path. e.g: -o /any-path-followed-by/output_directory-name/

ANALYSIS_NAME: Name by which pipeline saves the results inside output directory. e.g: -analysis first_analysis
 
INDEX: Reference Index Name. Change this argument in config file and mention the reference header name such as KP_NTUH_chr/KPNIH1/KPNIH32. 
        e.g: In config file; under the section KPNIH1, mention the attributes REF_NAME and REF_PATH for reference fasta filename and path to the reference fasta file.
        
################################################################################################################################################################################
The pipeline implements customisable variant calling configurations using config file.
Config file can be customised by changing two parameters under the section [pipeline]

aligner: bwa => Options for Aligner:bwa / smalt / bowtie

variant_caller: samtools Options for variant_caller: samtools/ samtoolswithpostalignbam / gatkhaplotypecaller

Currently, The pipeline supports BWA aligner(mem algorithm) for aligning reads to the reference genome.
Different options can be used to call variants. samtools call variants without indel-realignment step, samtoolswithpostalignbam calls variants with indel realignment as an additional step. 
gatkhaplotypecaller calls variants with GATK best practice variant calling steps and default parameters.

Parameters for each tools can be customised under the parameter attribute of each tool in config file.
# varcall_umich
