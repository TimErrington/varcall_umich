__author__ = 'alipirani'
import os
<<<<<<< HEAD
from config_settings import ConfigSectionMap
from modules.log_modules import keep_logging
from modules.logging_subprocess import *


## picard: remove duplicates
=======
from modules.log_modules import keep_logging
from modules.logging_subprocess import *
from config_settings import ConfigSectionMap


#################################################### picard: remove duplicates ############################################
>>>>>>> 02b125e3d68903b94aba39c984cecc3b7d770e55
def markduplicates(out_sorted_bam, out_path, analysis, files_to_delete, logger, Config):
    base_cmd = ConfigSectionMap("bin_path", Config)['binbase'] + "/" + ConfigSectionMap("picard", Config)['picard_bin'] + "/" + ConfigSectionMap("picard", Config)['base_cmd']
    keep_logging('Removing PCR duplicates using PICARD', 'Removing PCR duplicates using PICARD', logger, 'info')
    cmd = "java -jar %s MarkDuplicates REMOVE_DUPLICATES=true INPUT=%s OUTPUT=%s/%s_aln_marked.bam METRICS_FILE=%s/%s_markduplicates_metrics CREATE_INDEX=true VALIDATION_STRINGENCY=LENIENT" % (base_cmd, out_sorted_bam, out_path, analysis, out_path, analysis)
<<<<<<< HEAD
    keep_logging("COMMAND: " + cmd, cmd, logger, 'debug')
    try:
        call(cmd, logger)
=======
    keep_logging(cmd, cmd, logger, 'debug')
    try:
        call(cmd, logger)
        #print ""
>>>>>>> 02b125e3d68903b94aba39c984cecc3b7d770e55
    except sp.CalledProcessError:
            keep_logging('Error in Picard Duplicates Removal step. Exiting.', 'Error in Picard Duplicates Removal step. Exiting.', logger, 'exception')
            sys.exit(1)
    out_marked_bam = "%s/%s_aln_marked.bam" % (out_path, analysis)
    #files_to_delete.append(out_marked_bam)
    if not os.path.isfile(out_marked_bam):
        print "Problem in Picard MarkDuplicate Step\n"
        keep_logging('Problem in Picard MarkDuplicate Step', 'Problem in Picard MarkDuplicate Step', logger, 'exception')
        exit()
    else:
        return out_marked_bam
#################################################### END: picard: remove duplicates ############################################

<<<<<<< HEAD
## picard: Prepare Reference Sequence Dictionary for GATK indel realignment
=======
######################### picard: Prepare Reference Sequence Dictionary for GATK indel realignment #############################
>>>>>>> 02b125e3d68903b94aba39c984cecc3b7d770e55
def picard_seqdict(reference_filename, reference):
    dict_name = os.path.splitext(os.path.basename(reference_filename))[0] + ".dict"
    cmd = "java -jar %s CreateSequenceDictionary REFERENCE=%s OUTPUT=%s/%s" % (base_cmd, reference_filename, ConfigSectionMap(reference, Config)['ref_path'],dict_name)
    print "\nRunning:\n [%s] \n" % cmd
    os.system(cmd)
<<<<<<< HEAD

=======
######################### END: picard: Prepare Reference Sequence Dictionary for GATK indel realignment #############################
>>>>>>> 02b125e3d68903b94aba39c984cecc3b7d770e55
