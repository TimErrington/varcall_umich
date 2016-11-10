__author__ = 'alipirani'

import sys
import os
import argparse
import errno
from datetime import datetime
import ConfigParser
from config_settings import ConfigSectionMap
#from check_subroutines import *
if sys.version_info < (3, 2):
    import subprocess32 as sp
else:
    import subprocess as sp
from stages import *
from remove_5_bp_snp_indel import *
from bedtools import *
from gatk import gatk_DepthOfCoverage
from logging_subprocess import *
from log_modules import *


# Command Line Argument Parsing
def parser():
    parser = argparse.ArgumentParser(description='Variant Calling pipeline for Illumina PE data.')
    required = parser.add_argument_group('Required arguments')
    optional = parser.add_argument_group('Optional arguments')
    required.add_argument('-type', action='store', dest="type", help='Type of analysis: SE or PE', required=True)
    required.add_argument('-config', action='store', dest="config", help='Path to Config file', required=True)
    required.add_argument('-PE1', action='store', dest="forward_raw", help='Path to Paired End file 1', required=True)
    optional.add_argument('-PE2', action='store', dest="reverse_raw", help='Path to Paired End file 2', required=False)
    required.add_argument('-o', action='store', dest="output_folder", help='Output Path ending with output directory name to save the results', required=True)
    required.add_argument('-analysis', action='store', dest="analysis_name", help='Unique analysis name to save the results', required=True)
    required.add_argument('-index', action='store', dest="index", help='Reference Index Name. Change this argument in config file and mention the reference header name such as KP_NTUH_chr/KPNIH1/KPNIH32.', required=True)
    optional.add_argument('-c', action='store', dest="croplength", help='Crop Length in case needed')
    parser.add_argument('-f', action='store', dest="bam_input", help='Input Bam')
    return parser

# Main Pipeline
def pipeline(args, logger):
    keep_logging('START: Pipeline', 'START: Pipeline', logger, 'info')

    # Check Subroutines and create logger object: Arguments, Input files, Reference Index
    keep_logging('START: Checking Dependencies...', 'Checking Dependencies', logger, 'info')

    if args.output_folder != '':
        args.output_folder += '/'
    make_sure_path_exists(args.output_folder)

    # Reference Genome file name
    reference = ConfigSectionMap(args.index, Config)['ref_path'] + "/" + ConfigSectionMap(args.index, Config)['ref_name']
    keep_logging('Getting Reference Genome name from config file: {}'.format(reference), 'Getting Reference Genome name from config file: {}'.format(reference), logger, 'info')

    # Check FASTQ files
    if args.type != "PE":
        reverse_raw = "None"
        file_exists(args.forward_raw, reverse_raw, reference)
    else:
        file_exists(args.forward_raw, args.reverse_raw, reference)

    # Check Java Version
    java_check()
    keep_logging('END: Checking Dependencies...', 'END: Checking Dependencies', logger, 'info')


    ## 1. Pre-Processing Raw reads using Trimmomatic
    keep_logging('START: Pre-Processing Raw reads using Trimmomatic', 'START: Pre-Processing Raw reads using Trimmomatic', logger, 'info')
    if args.type == "PE":
        trimmomatic(args.forward_raw, args.reverse_raw, args.output_folder, args.croplength, logger, Config)
    else:
        reverse_raw = "None"
        trimmomatic(args.forward_raw, reverse_raw, args.output_folder, args.croplength, logger, Config)
    keep_logging('END: Pre-Processing Raw reads using Trimmomatic', 'END: Pre-Processing Raw reads using Trimmomatic', logger, 'info')


    ## 2. Stages: Alignment using BWA
    keep_logging('START: Mapping Reads using BWA', 'START: Mapping Reads using BWA', logger, 'info')
    split_field = prepare_readgroup(args.forward_raw, logger)
    files_to_delete = []
    out_sam = align(args.bam_input, args.output_folder, args.index, split_field, args.analysis_name, files_to_delete, logger, Config, args.type)
    keep_logging('END: Mapping Reads using BWA', 'END: Mapping Reads using BWA', logger, 'info')


    ## 3. Stages: Post-Alignment using SAMTOOLS, PICARD etc
    keep_logging('START: Post-Alignment using SAMTOOLS, PICARD etc...', 'START: Post-Alignment using SAMTOOLS, PICARD etc...', logger, 'info')
    #out_sorted_bam = prepare_bam(out_sam, args.output_folder, args.analysis_name, files_to_delete, logger, Config)
    keep_logging('END: Post-Alignment using SAMTOOLS, PICARD etc...', 'END: Post-Alignment using SAMTOOLS, PICARD etc...', logger, 'info')
    keep_logging('START: Creating BedGraph Coverage', 'START: Creating BedGraph Coverage', logger, 'info')
    out_sorted_bam = "%s/%s_aln_sort.bam" % (args.output_folder, args.analysis_name)
    #bedgraph_coverage(out_sorted_bam, args.output_folder, args.analysis_name, reference, logger, Config)
    #only_unmapped_positions_file = bedtools(out_sorted_bam, args.output_folder, args.analysis_name, logger, Config)
    keep_logging('END: Creating BedGraph Coverage', 'END: Creating BedGraph Coverage', logger, 'info')


    ## 4. Stages: Variant Calling
    keep_logging('START: Variant Calling', 'START: Variant Calling', logger, 'info')
    caller = ConfigSectionMap("pipeline", Config)['variant_caller']
    if caller == "samtoolswithpostalignbam":
        keep_logging('START: Variant Calling using Samtools and post-align bam input files', 'START: Variant Calling using Samtools and post-align bam input files', logger, 'info')
        out_finalbam = post_align_bam(out_sorted_bam, args.output_folder, args.index, args.analysis_name)
        final_raw_vcf = variant_calling(out_finalbam, args.output_folder, args.index, args.analysis_name)
        keep_logging('The final raw VCF file: {}'.format(final_raw_vcf), 'The final raw VCF file: {}'.format(final_raw_vcf), logger, 'debug')
        keep_logging('END: Variant Calling using Samtools and post-align bam input files', 'END: Variant Calling using Samtools and post-align bam input files', logger, 'info')
    elif caller == "gatkhaplotypecaller":
        keep_logging('START: Variant Calling using GATK haplotyper and post-align bam input files', 'START: Variant Calling using GATK haplotyper and post-align bam input files', logger, 'info')
        out_finalbam = post_align_bam(out_sorted_bam, args.output_folder, args.index, args.analysis_name)
        final_raw_vcf = variant_calling(out_finalbam, args.output_folder, args.index, args.analysis_name)
        keep_logging('The final raw VCF file: {}'.format(final_raw_vcf), 'The final raw VCF file: {}'.format(final_raw_vcf), logger, 'debug')
        keep_logging('END: Variant Calling using GATK haplotyper and post-align bam input files', 'END: Variant Calling using GATK haplotyper and post-align bam input files', logger, 'info')
    elif caller == "samtools":
        keep_logging('START: Variant Calling using Samtools without post-align bam input files.', 'START: Variant Calling using Samtools without post-align bam input files.', logger, 'info')
        #final_raw_vcf_mpileup = variant_calling(out_sorted_bam, args.output_folder, args.index, args.analysis_name, logger, Config)
        #final_raw_vcf_mpileup = "%s/%s_aln_mpileup_raw.vcf" % (args.output_folder, args.analysis_name)
        #final_raw_vcf = remove_5_bp_snp_indel(final_raw_vcf_mpileup, args.output_folder, args.analysis_name, reference, logger, Config)
        final_raw_vcf = "%s/%s_aln_mpileup_raw.vcf_5bp_indel_removed.vcf" % (args.output_folder, args.analysis_name)
        keep_logging('The final raw VCF file: {}'.format(final_raw_vcf), 'The final raw VCF file: {}'.format(final_raw_vcf), logger, 'debug')
        keep_logging('END: Variant Calling using Samtools without post-align bam input files.', 'END: Variant Calling using Samtools without post-align bam input files.', logger, 'info')
    else:
        keep_logging('Please provide Variant Caller name in config file under the section [pipeline]. Options for Variant caller: 1. samtools 2. samtoolswithpostalignbam 3. gatkhaplotypecaller', 'Please provide Variant Caller name in config file under the section [pipeline]. Options for Variant caller: 1. samtools 2. samtoolswithpostalignbam 3. gatkhaplotypecaller', logger, 'info')
        exit()
    keep_logging('END: Variant Calling', 'END: Variant Calling', logger, 'info')


    ## 5. Stages: Variant Filteration
    keep_logging('START: Variant Filteration', 'START: Variant Filteration', logger, 'info')
    #filter2_variants(final_raw_vcf, args.output_folder, args.analysis_name, args.index, logger, Config)
    keep_logging('END: Variant Filteration', 'END: Variant Filteration', logger, 'info')


    ## 6. Stages: Statistics
    keep_logging('START: Generating Statistics Reports', 'START: Generating Statistics Reports', logger, 'info')
    alignment_stats_file = alignment_stats(out_sorted_bam, args.output_folder, args.analysis_name, logger, Config)
    gatk_DepthOfCoverage(out_sorted_bam, args.output_folder, args.analysis_name, reference, logger, Config)
    vcf_stats_file = vcf_stats(final_raw_vcf, args.output_folder, args.analysis_name, logger, Config)
    qualimap_report = qualimap(out_sorted_bam, args.output_folder, args.analysis_name, logger, Config)
    keep_logging('END: Generating Statistics Reports', 'END: Generating Statistics Reports', logger, 'info')

    # ################################################### Stages: Remove Unwanted Intermediate files ######################################
    # # print "Removing Imtermediate Files...\n%s" % files_to_delete
    # # for files in files_to_delete:
    # #     os.remove(files)
    # # print "Removing Imtermediate Files...\n%s" % files_to_delete
    # # for files in files_to_delete:
    # #     os.remove(files)
    # ############################################################################ End ####################################################




## Check Subroutines
def usage():
    print "Usage: python pipeline.py [-h] -PE1 path-to-forward-PE-read -PE2 path-to-reverse-PE-read -o path-to-OUTPUT_FOLDER -analysis ANALYSIS_NAME -index INDEX_NAME_as_per_config_file \n"

# Validate Filenames for any unsupported characters
def Validate_filename( name ):
    pattern_strings = ['\.', '\&', '\>', 'aaa', '\*']
    pattern_string = '|'.join(pattern_strings)
    searchobj = re.search(pattern_string, name, flags=0)
    if searchobj:
        print "The file " + name + " contains unsupported characters such as quotes, spaces, or &:%?*><\$. \nPlease Provide another file name.\n"
        exit()

def file_exists(path1, path2, reference):

    if not os.path.isfile(path1):
        file_basename = os.path.basename(path1)
        keep_logging('The input file {} does not exists. Please provide another file or check the files path.\n'.format(file_basename), 'The input file {} does not exists. Please provide another file or check the files path.\n'.format(file_basename), logger, 'exception')
        exit()
    if path2 is not None:
        if not os.path.isfile(path2):
            file_basename = os.path.basename(path2)
            keep_logging('The input file {} does not exists. Please provide another file or check the files path.\n'.format(file_basename), 'The input file {} does not exists. Please provide another file or check the files path.\n'.format(file_basename), logger, 'exception')
            exit()
    if not os.path.isfile(reference):
        file_basename = os.path.basename(reference)
        keep_logging('The reference fasta file {} does not exists. Please provide another file or check the files path.\n'.format(file_basename), 'The reference fasta file {} does not exists. Please provide another file or check the files path.\n'.format(file_basename), logger, 'exception')
        exit()
    if ConfigSectionMap("pipeline", Config)['aligner'] == "bwa":
        ref_index_suffix1 = reference + ".bwt"
        ref_index_suffix2 = reference + ".amb"
        ref_index_suffix3 = reference + ".ann"
        ref_index_suffix4 = reference + ".sa"
        ref_index_suffix5 = reference + ".pac"
    else:
        ###########################################

        print "Please change the aligner section in config file."

        print "Different Aligner in config file"

    if not os.path.isfile(ref_index_suffix1):
        # file_basename = os.path.basename(reference)
        keep_logging('The reference index files given below does not exists:\n {}\n {}\n {}\n {}\n {}'.format(ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5), 'The reference index files given below does not exists:\n {}\n {}\n {}\n {}\n {}'.format(ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5), logger, 'warning')
        create_index(reference, ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5)
    else:
        keep_logging('Index file already exists.', 'Index file already exists.', logger, 'info')

    ############################################
    ref_fai_index = reference + ".fai"
    if not os.path.isfile(ref_fai_index):
        # file_basename = os.path.basename(reference)
        keep_logging('The reference fai index file {} required for samtools does not exists.'.format(ref_fai_index), 'The reference fai index file {} required for samtools does not exists.'.format(ref_fai_index), logger, 'warning')
        create_fai_index(reference, ref_fai_index)
    else:
        keep_logging('Samtools fai Index file already exists.', 'Samtools fai Index file already exists.', logger, 'info')

def java_check():
    keep_logging('Checking Java Availability...', 'Checking Java Availability...', logger, 'info')
    jd = sp.check_output(["java", "-version"], stderr=sp.STDOUT)
    jd_version = jd.split('\n', 1)[0]
    if len(jd) < 1:
        keep_logging('Unable to find a java runtime environment. The pipeline requires java 6 or later.', 'Unable to find a java runtime environment. The pipeline requires java 6 or later.', logger, 'exception')
    else:
        keep_logging('Java Availability Check completed ...{}'.format(jd_version), 'Java Availability Check completed ...{}'.format(jd_version), logger, 'info')

def fileformat(file1, file2, final_out):
    print "Checking File format....\n"
    if not file1.endswith('.fastq.gz'):
        base = os.path.basename(file1)
        os.path.splitext(base)
        file_1 = os.path.splitext(base)[0]
        cmdstring = "gzip -d " + file1 + " > " + final_out + file_1
        print "Compressing input file " + base
        os.system(cmdstring)


    if not file2.endswith('.fastq.gz'):
        base = os.path.basename(file2)
        os.path.splitext(base)
        file_2 = os.path.splitext(base)[0]
        cmdstring = "gzip -d " + file2 + " > " + final_out + file_2
        print "Compressing input file " + base
        os.system(cmdstring)

def make_sure_path_exists(out_path):
    try:
        os.makedirs(out_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            keep_logging('Errors in output folder path! please change the output path or analysis name.', 'Errors in output folder path! please change the output path or analysis name', logger, 'exception')
            exit()

def create_index(reference,ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5):
    aligner = ConfigSectionMap("pipeline")['aligner']
    keep_logging('Creating Index of reference fasta file for {} aligner.'.format(aligner), 'Creating Index of reference fasta file for {} aligner'.format(aligner), logger, 'info')
    if aligner == "bwa":
        cmd = "%s %s %s" % (ConfigSectionMap("bwa")['base_cmd'], ConfigSectionMap("bwa")['index'], reference)
        keep_logging(cmd, cmd, logger, 'debug')
        try:
            call(cmd, logger)
        except sp.CalledProcessError:
                keep_logging('Error in {} Indexer. Exiting.'.format(aligner), 'Error in {} Indexer. Exiting.'.format(aligner), logger, 'exception')
                sys.exit(1)
        if not os.path.isfile(ref_index_suffix1):
            keep_logging('The {} reference index files were not created properly. Please try to create the index files again or manually.'.format(aligner), 'The {} reference index files were not created properly. Please try to create the index files again or manually.'.format(aligner), logger, 'exception')
    else:
        print "Different Aligner in config file"

def create_fai_index(reference, ref_fai_index):
    keep_logging('Creating FAI Index using Samtools.', 'Creating FAI Index using Samtools.', logger, 'info')
    cmd = "%s %s %s" % (ConfigSectionMap("samtools")['base_cmd'], ConfigSectionMap("samtools")['faiindex'], reference)
    keep_logging(cmd, cmd, logger, 'debug')
    try:
        call(cmd, logger)
    except sp.CalledProcessError:
        keep_logging('Error in Samtools FAI Indexing step. Exiting.', 'Error in Samtools FAI Indexing step. Exiting.', logger, 'exception')
        sys.exit(1)


    if not os.path.isfile(ref_fai_index):
            keep_logging('The reference fai index file {} was not created properly.\n Please try to create the samtools fai index files manually. \n'.format(ref_fai_index), 'The reference fai index file {} was not created properly.\n Please try to create the samtools fai index files manually. \n'.format(ref_fai_index), logger, 'exception')
    else:
        keep_logging('Samtools Fai Index file created.', 'Samtools Fai Index file created.', logger, 'info')

###

# Main Method
if __name__ == '__main__':
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    args = parser().parse_args()
    global config_file
    config_file = args.config
    global logger
    log_unique_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    logger = generate_logger(args.output_folder, args.analysis_name, log_unique_time)
    global Config
    Config = ConfigParser.ConfigParser()
    Config.read(config_file)
    pipeline(args, logger)
    keep_logging('End: Pipeline', 'End: Pipeline', logger, 'info')
