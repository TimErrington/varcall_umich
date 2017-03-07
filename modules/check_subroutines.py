# __author__ = 'alipirani'
#
# import os
<<<<<<< HEAD
# import subprocess
# import errno
# from config_settings import ConfigSectionMap
#
=======
# import sys
# if sys.version_info < (3, 2):
#     import subprocess32 as sp
# else:
#     import subprocess as sp
# import errno
# from config_settings import ConfigSectionMap
# from config_settings import generate_logger
# from config_settings import keep_logging
# import logging
# from logging_subprocess import call
# logger = logging.getLogger("__main__")
>>>>>>> 02b125e3d68903b94aba39c984cecc3b7d770e55
#
#
# def usage():
#     print "Usage: python pipeline.py [-h] -PE1 path-to-forward-PE-read -PE2 path-to-reverse-PE-read -o path-to-OUTPUT_FOLDER -analysis ANALYSIS_NAME -index INDEX_NAME_as_per_config_file \n"
#
# # Validate Filenames for any unsupported characters
# def Validate_filename( name ):
#     pattern_strings = ['\.', '\&', '\>', 'aaa', '\*']
#     pattern_string = '|'.join(pattern_strings)
#     searchobj = re.search(pattern_string, name, flags=0)
#     if searchobj:
#         print "The file " + name + " contains unsupported characters such as quotes, spaces, or &:%?*><\$. \nPlease Provide another file name.\n"
#         exit()
#
# def file_exists(path1, path2, reference):
<<<<<<< HEAD
#     if not os.path.isfile(path1):
#         file_basename = os.path.basename(path1)
#         print "The input file " + file_basename + " does not exists. \nPlease provide another file.\n"
#         exit()
#     if not os.path.isfile(path2):
#         file_basename = os.path.basename(path2)
#         print "The input file " + file_basename + " does not exists. \nPlease provide another file.\n"
#         exit()
#     if not os.path.isfile(reference):
#         file_basename = os.path.basename(reference)
#         print "The reference file " + file_basename + " does not exists. \nPlease provide another file.\n"
#         exit()
#     if ConfigSectionMap("pipeline")['aligner'] == "bwa":
#         ref_index_suffix1 = reference + ".bwt"
#         ref_index_suffix2 = reference + ".amb"
#         ref_index_suffix3 = reference + ".ann"
#         ref_index_suffix4 = reference + ".sa"
#         ref_index_suffix5 = reference + ".pac"
#         ref_index_suffix6 = ""
#     elif ConfigSectionMap("pipeline")['aligner'] == "bowtie":
#         ref_index_suffix1 = reference + ".1.bt2"
#         ref_index_suffix2 = reference + ".2.bt2"
#         ref_index_suffix3 = reference + ".3.bt2"
#         ref_index_suffix4 = reference + ".4.ebwt"
#         ref_index_suffix5 = reference + ".rev.1.bt2"
#         ref_index_suffix6 = reference + ".rev.2.bt2"
#         ###########################################
#
#         #print "Please change the aligner section in config file."
#
#         #print "Different Aligner in config file"
#
#     if not os.path.isfile(ref_index_suffix1):
#         # file_basename = os.path.basename(reference)
#         print "The reference index files:\n %s\n %s\n %s\n %s\n %s\n %s\n does not exists. \n" % (ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5, ref_index_suffix6)
#         create_index(reference, ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5, ref_index_suffix6)
#     else:
#         print "\nIndex file already exists.\n"
#
#     ############################################
#     ref_fai_index = reference + ".fai"
#     if not os.path.isfile(ref_fai_index):
#         # file_basename = os.path.basename(reference)
#         print "The reference fai index file %s required for samtools does not exists. \n" % (ref_fai_index)
#         create_fai_index(reference, ref_fai_index)
#     else:
#         print "\nSamtools fai Index file already exists.\n"
#
# def file_exists_se(path1, reference):
#     if not os.path.isfile(path1):
#         file_basename = os.path.basename(path1)
#         print "The input file " + file_basename + " does not exists. \nPlease provide another file.\n"
#         exit()
#     if not os.path.isfile(reference):
#         file_basename = os.path.basename(reference)
#         print "The reference file " + file_basename + " does not exists. \nPlease provide another file.\n"
=======
#
#     if not os.path.isfile(path1):
#         file_basename = os.path.basename(path1)
#         keep_logging('The input file {} does not exists. Please provide another file or check the files path.\n'.format(file_basename), 'The input file {} does not exists. Please provide another file or check the files path.\n'.format(file_basename), logger, 'exception')
#         exit()
#     if path2 is not None:
#         if not os.path.isfile(path2):
#             file_basename = os.path.basename(path2)
#             keep_logging('The input file {} does not exists. Please provide another file or check the files path.\n'.format(file_basename), 'The input file {} does not exists. Please provide another file or check the files path.\n'.format(file_basename), logger, 'exception')
#             exit()
#     if not os.path.isfile(reference):
#         file_basename = os.path.basename(reference)
#         keep_logging('The reference fasta file {} does not exists. Please provide another file or check the files path.\n'.format(file_basename), 'The reference fasta file {} does not exists. Please provide another file or check the files path.\n'.format(file_basename), logger, 'exception')
>>>>>>> 02b125e3d68903b94aba39c984cecc3b7d770e55
#         exit()
#     if ConfigSectionMap("pipeline")['aligner'] == "bwa":
#         ref_index_suffix1 = reference + ".bwt"
#         ref_index_suffix2 = reference + ".amb"
#         ref_index_suffix3 = reference + ".ann"
#         ref_index_suffix4 = reference + ".sa"
#         ref_index_suffix5 = reference + ".pac"
<<<<<<< HEAD
#         ref_index_suffix6 = ""
#     elif ConfigSectionMap("pipeline")['aligner'] == "bowtie":
#         ref_index_suffix1 = reference + ".1.bt2"
#         ref_index_suffix2 = reference + ".2.bt2"
#         ref_index_suffix3 = reference + ".3.bt2"
#         ref_index_suffix4 = reference + ".4.ebwt"
#         ref_index_suffix5 = reference + ".rev.1.bt2"
#         ref_index_suffix6 = reference + ".rev.2.bt2"
#         ###########################################
#
#         #print "Please change the aligner section in config file."
#
#         #print "Different Aligner in config file"
#
#     if not os.path.isfile(ref_index_suffix1):
#         # file_basename = os.path.basename(reference)
#         print "The reference index files:\n %s\n %s\n %s\n %s\n %s\n %s\n does not exists. \n" % (ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5, ref_index_suffix6)
#         create_index(reference, ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5, ref_index_suffix6)
#     else:
#         print "\nIndex file already exists.\n"
=======
#     else:
#         ###########################################
#
#         print "Please change the aligner section in config file."
#
#         print "Different Aligner in config file"
#
#     if not os.path.isfile(ref_index_suffix1):
#         # file_basename = os.path.basename(reference)
#         keep_logging('The reference index files given below does not exists:\n {}\n {}\n {}\n {}\n {}'.format(ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5), 'The reference index files given below does not exists:\n {}\n {}\n {}\n {}\n {}'.format(ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5), logger, 'warning')
#         create_index(reference, ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5)
#     else:
#         keep_logging('Index file already exists.', 'Index file already exists.', logger, 'info')
>>>>>>> 02b125e3d68903b94aba39c984cecc3b7d770e55
#
#     ############################################
#     ref_fai_index = reference + ".fai"
#     if not os.path.isfile(ref_fai_index):
#         # file_basename = os.path.basename(reference)
<<<<<<< HEAD
#         print "The reference fai index file %s required for samtools does not exists. \n" % (ref_fai_index)
#         create_fai_index(reference, ref_fai_index)
#     else:
#         print "\nSamtools fai Index file already exists.\n"
#
# def java_check():
#     print "\nChecking Java Availability....\n"
#     jd = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
#     if len(jd) < 1:
#         print "Unable to find a java runtime environment. The pipeline requires java 6 or later."
#     else:
#         print "Java Availability Check completed ...\n\n" + jd
=======
#         keep_logging('The reference fai index file {} required for samtools does not exists.'.format(ref_fai_index), 'The reference fai index file {} required for samtools does not exists.'.format(ref_fai_index), logger, 'warning')
#         create_fai_index(reference, ref_fai_index)
#     else:
#         keep_logging('Samtools fai Index file already exists.', 'Samtools fai Index file already exists.', logger, 'info')
#
# def java_check():
#     keep_logging('Checking Java Availability...', 'Checking Java Availability...', logger, 'info')
#     jd = sp.check_output(["java", "-version"], stderr=sp.STDOUT)
#     jd_version = jd.split('\n', 1)[0]
#     if len(jd) < 1:
#         keep_logging('Unable to find a java runtime environment. The pipeline requires java 6 or later.', 'Unable to find a java runtime environment. The pipeline requires java 6 or later.', logger, 'exception')
#     else:
#         keep_logging('Java Availability Check completed ...{}'.format(jd_version), 'Java Availability Check completed ...{}'.format(jd_version), logger, 'info')
>>>>>>> 02b125e3d68903b94aba39c984cecc3b7d770e55
#
# def fileformat(file1, file2, final_out):
#     print "Checking File format....\n"
#     if not file1.endswith('.fastq.gz'):
#         base = os.path.basename(file1)
#         os.path.splitext(base)
#         file_1 = os.path.splitext(base)[0]
#         cmdstring = "gzip -d " + file1 + " > " + final_out + file_1
#         print "Compressing input file " + base
#         os.system(cmdstring)
#
#
#     if not file2.endswith('.fastq.gz'):
#         base = os.path.basename(file2)
#         os.path.splitext(base)
#         file_2 = os.path.splitext(base)[0]
#         cmdstring = "gzip -d " + file2 + " > " + final_out + file_2
#         print "Compressing input file " + base
#         os.system(cmdstring)
#
# def make_sure_path_exists(out_path):
#     try:
#         os.makedirs(out_path)
#     except OSError as exception:
#         if exception.errno != errno.EEXIST:
<<<<<<< HEAD
#             print "Errors in output folder path! please change the output path or analysis name\n"
#             exit()
#
# def create_index(reference,ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5, ref_index_suffix6):
#     aligner = ConfigSectionMap("pipeline")['aligner']
#     if aligner == "bwa":
#         print "Creating Index using %s \n" % aligner
#         cmd = "%s %s %s" % (ConfigSectionMap("bwa")['base_cmd'], ConfigSectionMap("bwa")['index'], reference)
#         print "Running Command: [%s]" % cmd
#         os.system(cmd)
#         if not os.path.isfile(ref_index_suffix1):
#             # file_basename = os.path.basename(reference)
#             print "The reference index files:\n %s\n %s\n %s\n %s\n %s\n were not created properly.\n Please try to create the index files manually. \n" % (ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5)
#             exit()
#     elif aligner == "bowtie":
#         print "Creating Index using %s \n" % aligner
#         cmd = "%s/%s/%s %s %s" % (ConfigSectionMap("bin_path")['binbase'], ConfigSectionMap("bowtie")['bowtie_bin'], ConfigSectionMap("bowtie")['build_cmd'], reference, reference)
#         print "Running Command: [%s]" % cmd
#         os.system(cmd)
#         if not os.path.isfile(ref_index_suffix1):
#             # file_basename = os.path.basename(reference)
#             print "The reference index files:\n %s\n %s\n %s\n %s\n %s\n %s\n were not created properly.\n Please try to create the index files manually. \n" % (ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5, ref_index_suffix6)
#             exit()
#
# def create_fai_index(reference, ref_fai_index):
#     print "Creating FAI Index using %s \n" % ConfigSectionMap("samtools")['base_cmd']
#     cmd = "%s %s %s" % (ConfigSectionMap("samtools")['base_cmd'], ConfigSectionMap("samtools")['faiindex'], reference)
#     print "Running Command: [%s]" % cmd
#     os.system(cmd)
#
#     if not os.path.isfile(ref_fai_index):
#             # file_basename = os.path.basename(reference)
#             print "The reference fai index file %s was not created properly.\n Please try to create the samtools fai index files manually. \n" % ref_fai_index
#             exit()
#     else:
#         print "Samtools Fai Index file created.\n"
=======
#             keep_logging('Errors in output folder path! please change the output path or analysis name.', 'Errors in output folder path! please change the output path or analysis name', logger, 'exception')
#             exit()
#
# def create_index(reference,ref_index_suffix1, ref_index_suffix2, ref_index_suffix3, ref_index_suffix4, ref_index_suffix5):
#     aligner = ConfigSectionMap("pipeline")['aligner']
#     keep_logging('Creating Index of reference fasta file for {} aligner.'.format(aligner), 'Creating Index of reference fasta file for {} aligner'.format(aligner), logger, 'info')
#     if aligner == "bwa":
#         cmd = "%s %s %s" % (ConfigSectionMap("bwa")['base_cmd'], ConfigSectionMap("bwa")['index'], reference)
#         keep_logging(cmd, cmd, logger, 'debug')
#         try:
#             call(cmd, logger)
#         except sp.CalledProcessError:
#                 keep_logging('Error in {} Indexer. Exiting.'.format(aligner), 'Error in {} Indexer. Exiting.'.format(aligner), logger, 'exception')
#                 sys.exit(1)
#         if not os.path.isfile(ref_index_suffix1):
#             keep_logging('The {} reference index files were not created properly. Please try to create the index files again or manually.'.format(aligner), 'The {} reference index files were not created properly. Please try to create the index files again or manually.'.format(aligner), logger, 'exception')
#     else:
#         print "Different Aligner in config file"
#
# def create_fai_index(reference, ref_fai_index):
#     keep_logging('Creating FAI Index using Samtools.', 'Creating FAI Index using Samtools.', logger, 'info')
#     cmd = "%s %s %s" % (ConfigSectionMap("samtools")['base_cmd'], ConfigSectionMap("samtools")['faiindex'], reference)
#     keep_logging(cmd, cmd, logger, 'debug')
#     try:
#         call(cmd, logger)
#     except sp.CalledProcessError:
#         keep_logging('Error in Samtools FAI Indexing step. Exiting.', 'Error in Samtools FAI Indexing step. Exiting.', logger, 'exception')
#         sys.exit(1)
#
#
#     if not os.path.isfile(ref_fai_index):
#             keep_logging('The reference fai index file {} was not created properly.\n Please try to create the samtools fai index files manually. \n'.format(ref_fai_index), 'The reference fai index file {} was not created properly.\n Please try to create the samtools fai index files manually. \n'.format(ref_fai_index), logger, 'exception')
#     else:
#         keep_logging('Samtools Fai Index file created.', 'Samtools Fai Index file created.', logger, 'info')
>>>>>>> 02b125e3d68903b94aba39c984cecc3b7d770e55
