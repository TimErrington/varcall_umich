__author__ = 'alipirani'
import os
from modules.log_modules import keep_logging
from modules.logging_subprocess import *

<<<<<<< HEAD
###Pending
#################################################### BWA Alignment ############################################
def align_bwa(base_cmd,forward_clean, out_path, reference, split_field, analysis, files_to_delete):
    print "\n################## BWA Alignment ##################\n"
    cmd = "%s mem -M -R %s -t 8 %s %s > %s/%s_aln.sam" % (base_cmd,split_field, reference, forward_clean, out_path, analysis)
    print "\nRunning:\n [%s] \n" % cmd
    os.system(cmd)
    out_sam = "%s/%s_aln.sam" % (out_path, analysis)
    files_to_delete.append(out_sam)
    if not os.path.isfile(out_sam):
        print "Problem in aligning the reads\n"
        exit()
        usage()
    else:
        print "\n################## END: BWA Alignment ##################\n"
=======
#################################################### BWA Alignment ############################################
def align_bwa(base_cmd,forward_clean, reverse_clean, out_path, reference, split_field, analysis, files_to_delete, logger, Config, type):
    if type == "PE":
        cmd = "%s mem -M -R %s -t 8 %s %s %s > %s/%s_aln.sam" % (base_cmd,split_field, reference, forward_clean, reverse_clean, out_path, analysis)
    else:
        cmd = "%s mem -M -R %s -t 8 %s %s > %s/%s_aln.sam" % (base_cmd,split_field, reference, forward_clean, out_path, analysis)
    keep_logging(cmd, cmd, logger, 'debug')
    try:
        call(cmd, logger)
        print ""
    except sp.CalledProcessError:
        keep_logging('Error in Alignment step. Exiting.', 'Error in Alignment step. Exiting.', logger, 'exception')
        sys.exit(1)
    out_sam = "%s/%s_aln.sam" % (out_path, analysis)
    files_to_delete.append(out_sam)
    if not os.path.isfile(out_sam):
        keep_logging('Problem in BWA alignment. SAM file was not generated.', 'Problem in BWA alignment. SAM file was not generated', logger, 'exception')
        exit()
    else:
>>>>>>> 02b125e3d68903b94aba39c984cecc3b7d770e55
        return out_sam
#################################################### END: BWA Alignment #######################################


