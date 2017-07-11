from __future__ import division
import argparse
import re
import os
import csv
import subprocess
from collections import OrderedDict
from collections import defaultdict
from joblib import Parallel, delayed
import multiprocessing
import thread
import glob
import readline
import pandas as pd
import errno
from pyfasta import Fasta
from datetime import datetime
import threading

parser = argparse.ArgumentParser(description='Parsing filtered VCF files and investigating Variants to determine the reason why it was filtered out from the final list')
required = parser.add_argument_group('Required arguments')
optional = parser.add_argument_group('Optional arguments')
required.add_argument('-filter2_only_snp_vcf_dir', action='store', dest="filter2_only_snp_vcf_dir",
                    help='Directory where all the filter2 only SNP vcf files are saved.')
required.add_argument('-filter2_only_snp_vcf_filenames', action='store', dest="filter2_only_snp_vcf_filenames",
                    help='Names of filter2 only SNP vcf files with name per line.')
optional.add_argument('-jobrun', action='store', dest="jobrun",
                    help='Running a job on Cluster, Running Parallel jobs, Run jobs/commands locally (default): cluster, local, parallel-local, parallel-single-cluster')
optional.add_argument('-cluster_type', action='store', dest="cluster_type",
                    help='Type of Cluster: torque, pbs, sgd')
optional.add_argument('-cluster_resources', action='store', dest="cluster_resources",
                    help='Cluster Resources to use. for example nodes,core. Ex: 1,4')
optional.add_argument('-numcores', action='store', dest="numcores",
                    help='Number of cores to use on local system for parallel-local parameter')
optional.add_argument('-remove_temp', action='store', dest="remove_temp",
                    help='Remove Temporary files generated during the run')
optional.add_argument('-reference', action='store', dest="reference",
                    help='Path to Reference Fasta file for consensus generation')
required.add_argument('-steps', action='store', dest="steps",
                    help='Analysis Steps to be performed. This should be in sequential order.'
                         'Step 1: Run pbs jobs and process all pipeline generated vcf files to generate label files'
                         'Step 2: Analyze label files and generate matrix'
                         'Step 3: DP/FQ Analysis')
args = parser.parse_args()


def create_positions_filestep(vcf_filenames):

    """
    Gather SNP positions from each final *_no_proximate_snp.vcf file (that passed the variant filter parameters
    from variant calling pipeline) and write to *_no_proximate_snp.vcf_position files for use in downstream methods

    """

    filter2_only_snp_position_files_array = []
    for file in vcf_filenames:
        with open(file, 'rU') as csv_file:
            file_name = temp_dir + "/" + os.path.basename(file) + "_positions"
            addpositionfilenametoarray = file_name
            filter2_only_snp_position_files_array.append(addpositionfilenametoarray)
            f1 = open(file_name, 'w+')
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                position = row[0]
                if not position.startswith('#'):
                    p_string = row[1] + "\n"
                    f1.write(p_string)
            f1.close()
        csv_file.close()
    print "End of creating '_positions' file step\n"

    """ Create position array containing unique positiones from positions file """
    position_array = []
    for filess in filter2_only_snp_position_files_array:
        f = open(filess, 'r+')
        for line in f:
            line = line.strip()
            position_array.append(line)
        f.close()
    position_array_unique = set(position_array)
    position_array_sort = sorted(position_array_unique)
    print "\nThe number of unique variant positions:\n" + str(len(position_array_sort)) + "\n"
    unique_position_file = "%s/unique_positions_file" % args.filter2_only_snp_vcf_dir
    f=open(unique_position_file, 'w+')
    for i in position_array_sort:
        f.write(i + "\n")
    f.close()
    if len(position_array_sort) == 0:
        print "ERROR: No unique positions found. Check if vcf files are empty?"
        exit()



####################END: Create position array containing unique positiones from positions file#######################


def make_sure_path_exists(out_path):
    """
    Make sure the output folder exists or create at given path
    :param out_path:
    :return:
    """
    try:
        os.makedirs(out_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            print "Errors in output folder path! please change the output path or analysis name\n"
            exit()

def run_command(i):
    print "Running: %s" % i
    os.system(i)
    done = "done: %s" % i
    return done


def create_job(jobrun, vcf_filenames):

    """
    Based on type of jobrun; generate jobs and run accordingly.
    :param jobrun:
    :param vcf_filenames:
    :return:
    """
    if jobrun == "cluster":
        """
        Supports only PBS clusters for now.
        """
        for i in vcf_filenames:
            job_name = os.path.basename(i)
            job_print_string = "#PBS -N %s\n#PBS -M apirani@med.umich.edu\n#PBS -m abe\n#PBS -V\n#PBS -l nodes=1:ppn=4,pmem=4000mb,walltime=72:00:00\n#PBS -q fluxod\n#PBS -A esnitkin_fluxod\n#PBS -l qos=flux\n\n/home/apirani/anaconda/bin/python /nfs/esnitkin/bin_group/scripts/Scripts_v2.0/variants_position_analysis/reason_job_joyce.py -filter2_only_snp_vcf_dir %s -filter2_only_snp_vcf_file %s\n" % (job_name, args.filter2_only_snp_vcf_dir, i)
            job_file_name = "%s.pbs" % (i)
            f1=open(job_file_name, 'w+')
            f1.write(job_print_string)
            f1.close()
        #os.system("mv %s/*.pbs %s/temp" % (args.filter2_only_snp_vcf_dir, args.filter2_only_snp_vcf_dir))
        pbs_dir = args.filter2_only_snp_vcf_dir + "/*.pbs"
        pbs_scripts = glob.glob(pbs_dir)
        for i in pbs_scripts:
            print "Running: qsub %s" % i
            #os.system("qsub %s" % i)

    elif jobrun == "parallel-local":
        """
        Generate a Command list of each job and run it in parallel on different cores available on local system
        """
        command_array = []
        command_file = "%s/commands_list.sh" % args.filter2_only_snp_vcf_dir
        f3 = open(command_file, 'w+')


        for i in vcf_filenames:
            job_name = os.path.basename(i)
            job_print_string = "#PBS -N %s\n#PBS -M apirani@med.umich.edu\n#PBS -m abe\n#PBS -V\n#PBS -l nodes=1:ppn=4,pmem=4000mb,walltime=72:00:00\n#PBS -q fluxod\n#PBS -A esnitkin_fluxod\n#PBS -l qos=flux\n\n/home/apirani/anaconda/bin/python /nfs/esnitkin/bin_group/scripts/Scripts_v2.0/variants_position_analysis/reason_job_joyce.py -filter2_only_snp_vcf_dir %s -filter2_only_snp_vcf_file %s\n" % (job_name, args.filter2_only_snp_vcf_dir, i)
            job_file_name = "%s.pbs" % (i)
            f1=open(job_file_name, 'w+')
            f1.write(job_print_string)
            f1.close()
        #os.system("mv %s/*.pbs %s/temp" % (args.filter2_only_snp_vcf_dir, args.filter2_only_snp_vcf_dir))
        pbs_dir = args.filter2_only_snp_vcf_dir + "/*.pbs"
        pbs_scripts = glob.glob(pbs_dir)


        for i in pbs_scripts:
            f3.write("bash %s\n" % i)
        f3.close()
        with open(command_file, 'r') as fpp:
            for lines in fpp:
                lines = lines.strip()
                command_array.append(lines)
        fpp.close()
        print len(command_array)
        if args.numcores:
            num_cores = int(num_cores)
        else:
            num_cores = multiprocessing.cpu_count()
        results = Parallel(n_jobs=num_cores)(delayed(run_command)(command) for command in command_array)

    elif jobrun == "parallel-single-cluster":
        print "  "
    else:
        """
        Generate a Command list of each job and run it on local system one at a time
        """
        command_array = []
        command_file = "%s/commands_list.sh" % args.filter2_only_snp_vcf_dir
        os.system("bash %s" % command_file)



if __name__ == '__main__':

    """Start Timer"""
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_time_2 = datetime.now()

    print "\nThe Script started at: %s\n" % start_time

    print "\nThe Script: parse_vcf_for_reason.py will parse the final vcf files generated from Variant Calling Pipeline to generate:\n\n" \
          "1. Final Core SNP Positions list(Variant positions that were not filtered out in any of the samples and passed all the filters)\n" \
          "2. SNP Positions that were filtered out with labels indicating the reason (Depth, FQ, MQ, Unmapped in one or other samples, Proximate SNPS, Quality of Variant) why they were filtered out.\n" \
          "3. Barplot Statistics about the filtered variants and their reason for getting filtered.\n" \
          "4. Final Consensus fasta file generating using Final Core SNP Positions list\n"

    """ Create Temp Directory for storing unwanted temp files generated while running script """
    temp_dir = args.filter2_only_snp_vcf_dir + "/temp"
    make_sure_path_exists(temp_dir)

    filter2_only_snp_vcf_filenames = args.filter2_only_snp_vcf_filenames
    vcf_filenames = []
    with open(filter2_only_snp_vcf_filenames) as fp:
        for line in fp:
            line = line.strip()
            line = args.filter2_only_snp_vcf_dir + line
            vcf_filenames.append(line)
        fp.close()


    """
    Gather SNP positions from each final *_no_proximate_snp.vcf file (that passed the variant filter parameters
    from variant calling pipeline) and write to *_no_proximate_snp.vcf_position files for use in downstream methods
    """
    create_positions_filestep(vcf_filenames)

    """ Get the cluster option; create and run jobs based on given parameter """
    create_job(args.jobrun, vcf_filenames)



    time_taken = datetime.now() - start_time_2
    if args.remove_temp:
        del_command = "rm -r %s" % temp_dir
        os.system(del_command)















