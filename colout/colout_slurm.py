
def theme(context):
    # SLURM's states (from squeue manual).

    col_width = 9

    COMPLETED    =r"\bCOMPLETED"
    PENDING      =r"\bPENDING"
    RUNNING      =r"\bRUNNING"
    CONFIGURING  =r"\bCONFIGURING"
    COMPLETING   =r"\bCOMPLETING"
    FAILED       =r"\bFAILED"
    DEADLINE     =r"\bDEADLINE"
    OUT_OF_MEMORY=r"\bOUT_OF_MEMORY"
    TIMEOUT      =r"\bTIMEOUT"
    CANCELLED    =r"\bCANCELLED"
    BOOT_FAIL    =r"\bBOOT_FAIL"
    NODE_FAIL    =r"\bNODE_FAIL"
    PREEMPTED    =r"\bPREEMPTED"
    RESV_DEL_HOLD=r"\bRESV_DEL_HOLD"
    REQUEUE_FED  =r"\bREQUEUE_FED"
    REQUEUE_HOLD =r"\bREQUEUE_HOLD"
    REQUEUED     =r"\bREQUEUED"
    RESIZING     =r"\bRESIZING"
    REVOKED      =r"\bREVOKED"
    SIGNALING    =r"\bSIGNALING"
    SPECIAL_EXIT =r"\bSPECIAL_EXIT"
    STAGE_OUT    =r"\bSTAGE_OUT"
    STOPPED      =r"\bSTOPPED"
    SUSPENDED    =r"\bSUSPENDED"

    return context,[

        ## No problem: greens

        #Job has terminated all processes on all nodes with an exit code of zero.
        [r"\bCD\b", "22"],
        [COMPLETED[0:col_width]+r"\w*\b", "22"],
        #Job is awaiting resource allocation.
        [r"\bPD\b", "28"],
        [PENDING[0:col_width]+r"\w*\b", "28"],
        #Job currently has an allocation.
        [r"\bR\b", "34"],
        [RUNNING[0:col_width]+r"\w*\b", "34"],
        #Job has been allocated resources, but are waiting for them to become ready for use (e.g. booting).
        [r"\bCF\b", "58"],
        [CONFIGURING[0:col_width]+r"\w*\b", "58"],
        #Job is in the process of completing. Some processes on some nodes may still be active.
        [r"\bCG\b", "23"],
        [COMPLETING[0:col_width]+r"\w*\b", "23"],

        ## Problem for the user: bold reds

        #Job terminated with non-zero exit code or other failure condition.
        [r"\bF\b", "196"],
        [FAILED[0:col_width]+r"\w*\b", "196", "bold"],
        #Job terminated on deadline.
        [r"\bDL\b", "160"],
        [DEADLINE[0:col_width]+r"\w*\b", "160", "bold"],
        #Job experienced out of memory error.
        [r"\bOO\b", "197"],
        [OUT_OF_MEMORY[0:col_width]+r"\w*\b", "197", "bold"],
        #Job terminated upon reaching its time limit.
        [r"\bTO\b", "161"],
        [TIMEOUT[0:col_width]+r"\w*\b", "161", "bold"],

        ## Problem for the sysadmin: oranges

        #Job was explicitly cancelled by the user or system administrator. The job may or may not have been initiated.
        [r"\bCA\b", "202"],
        [CANCELLED[0:col_width]+r"\w*\b", "202", "bold"],
        #Job terminated due to launch failure, typically due to a hardware failure (e.g. unable to boot the node or block and the job can not be requeued).
        [r"\bBF\b", "166"],
        [BOOT_FAIL[0:col_width]+r"\w*\b", "166"],
        #Job terminated due to failure of one or more allocated nodes.
        [r"\bNF\b", "208"],
        [NODE_FAIL[0:col_width]+r"\w*\b", "208"],

        ## Non-blocking events: blues

        #Job terminated due to preemption.
        [r"\bPR\b", "105"],
        [PREEMPTED[0:col_width]+r"\w*\b", "105", "bold"],
        #Job is being held after requested reservation was deleted.
        [r"\bRD\b", "25"],
        [RESV_DEL_HOLD[0:col_width]+r"\w*\b", "25"],
        #Job is being requeued by a federation.
        [r"\bRF\b", "26"],
        [REQUEUE_FED[0:col_width]+r"\w*\b", "26"],
        #Held job is being requeued.
        [r"\bRH\b", "27"],
        [REQUEUE_HOLD[0:col_width]+r"\w*\b", "27"],
        #Completing job is being requeued.
        [r"\bRQ\b", "31"],
        [REQUEUED[0:col_width]+r"\w*\b", "31"],
        #Job is about to change size.
        [r"\bRS\b", "32"],
        [RESIZING[0:col_width]+r"\w*\b", "32"],
        #Sibling was removed from cluster due to other cluster starting the job.
        [r"\bRV\b", "33"],
        [REVOKED[0:col_width]+r"\w*\b", "33"],
        #Job is being signaled.
        [r"\bSI\b", "37"],
        [SIGNALING[0:col_width]+r"\w*\b", "37"],
        #The job was requeued in a special state. This state can be set by users, typically in EpilogSlurmctld, if the job has terminated with a particular exit value.
        [r"\bSE\b", "38"],
        [SPECIAL_EXIT[0:col_width]+r"\w*\b", "38"],
        #Job is staging out files.
        [r"\bSO\b", "39"],
        [STAGE_OUT[0:col_width]+r"\w*\b", "39"],
        #Job has an allocation, but execution has been stopped with SIGSTOP signal. CPUS have been retained by this job.
        [r"\bST\b", "44"],
        [STOPPED[0:col_width]+r"\w*\b", "44"],
        #Job has an allocation, but execution has been suspended and CPUs have been released for other jobs.
        [r"\bS\b", "45"],
        [SUSPENDED[0:col_width]+r"\w*\b", "45"],
    ]
