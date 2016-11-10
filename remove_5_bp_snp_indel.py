import sys
import os
import argparse
import errno
from config_settings import ConfigSectionMap
import csv
from logging_subprocess import *
from log_modules import *


indel_positions = []
indel_range_positions = []
#indel removed at this step
def remove_5_bp_snp_indel(raw_vcf_file, out_path, analysis, reference, logger, Config):
    remove_snps_5_bp_snp_indel_file_name = raw_vcf_file + "_5bp_indel_removed.vcf"
    with open(raw_vcf_file, 'rU') as csv_file:
        for line in csv_file:
            #Change this condition; This is hardcoded!
            if line.startswith('gi') or line.startswith('MRSA_8058'):
                line_array = line.split('\t')
                if line_array[7].startswith('INDEL;'):
                     indel_positions.append(line_array[1])
        for i in indel_positions:
            lower_range = int(i) - 5
            upper_range = int(i) + 6
            for positions in range(lower_range,upper_range):
                indel_range_positions.append(positions)
        #print indel_range_positions
    f1=open(remove_snps_5_bp_snp_indel_file_name, 'w+')
    with open(raw_vcf_file, 'rU') as csv_file2:
        for line in csv_file2:
            if line.startswith('gi') or line.startswith('MRSA_8058'):
               line_array = line.split('\t')
               if int(line_array[1]) not in indel_range_positions:
                   #print line_array[1]
                   print_string = line
                   f1.write(print_string)
            else:
                print_string = line
                f1.write(print_string)
    return remove_snps_5_bp_snp_indel_file_name




#remove_5_bp_snp_indel(raw_vcf_file, out_path, analysis)


def remove_proximate_snps(gatk_filter2_final_vcf_file, out_path, analysis, reference, logger, Config):
    all_position = []
    remove_proximate_position_array = []
    gatk_filter2_final_vcf_file_no_proximate_snp = gatk_filter2_final_vcf_file + "_no_proximate_snp.vcf"
    with open(gatk_filter2_final_vcf_file, 'rU') as csv_file:
        for line in csv_file:
            if not line.startswith('#'):
                line_array = line.split('\t')
                all_position.append(line_array[1])
    for position in all_position:
        position_index = all_position.index(position)
        next_position_index = position_index + 1

        if next_position_index < len(all_position):
            diff = int(all_position[next_position_index]) - int(position)
            if diff < 10:
                #print position + "  " + all_position[next_position_index]
                if position not in remove_proximate_position_array and all_position[next_position_index] not in remove_proximate_position_array:
                    remove_proximate_position_array.append(int(position))
                    remove_proximate_position_array.append(int(all_position[next_position_index]))
    #print remove_proximate_position_array
    f1=open(gatk_filter2_final_vcf_file_no_proximate_snp, 'w+')
    with open(gatk_filter2_final_vcf_file, 'rU') as csv_file2:
        for line in csv_file2:
            if line.startswith('gi') or line.startswith('MRSA_8058'):
               line_array = line.split('\t')
               if int(line_array[1]) not in remove_proximate_position_array:
                   #print line_array[1]
                   #print line_array[1]
                   print_string = line
                   f1.write(print_string)
            else:
                print_string = line
                f1.write(print_string)
    gatk_filter2_final_vcf_file_no_proximate_snp_positions = gatk_filter2_final_vcf_file + "_no_proximate_snp.vcf_positions_array"
    f2=open(gatk_filter2_final_vcf_file_no_proximate_snp_positions, 'w+')
    for i in remove_proximate_position_array:
        position_print_string = str(i) + "\n"
        f2.write(position_print_string)
    return gatk_filter2_final_vcf_file_no_proximate_snp
#remove_proximate_snps(gatk_filter2_final_vcf_file, out_path, analysis)


























