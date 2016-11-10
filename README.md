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
