#!/usr/bin/python
import os

hostname = os.popen("hostname").read().split("\n")[0]

with open("slurmdbd.conf", "w") as slurmdbd:
    slurmdbd.writelines("AuthType=auth/munge\n")
    slurmdbd.writelines("DbdAddr={0}\n".format(hostname))
    slurmdbd.writelines("DbdHost={0}\n".format(hostname))
    slurmdbd.writelines("SlurmUser=slurm\n")
    slurmdbd.writelines("DebugLevel=4\n")
    slurmdbd.writelines("LogFile=/var/log/slurm/slurmdbd.log\n")
    slurmdbd.writelines("PidFile=/var/run/slurmdbd.pid\n")
    slurmdbd.writelines("StorageType=accounting_storage/mysql\n")
    slurmdbd.writelines("StorageHost=localhost\n")
    slurmdbd.writelines("StoragePass={0}\n".format(hostname))
    slurmdbd.writelines("StorageUser=slurm\n")
    slurmdbd.writelines("StorageLoc=slurm_acct_db\n")

try: 
    gpuCount= int(os.popen("nvidia-smi --list-gpus | wc -l").read())
except Exception:
    print("Error in count GPU")

with open("gres.conf", "w") as gres:
    if (gpuCount == 1):
        gres.writelines("NodeName={0} Name=gpu Count={1} File=/dev/nvidia0".format(hostname, gpuCount))
    else:
        gres.writelines("NodeName={0} Name=gpu Count={1} File=/dev/nvidia0-{2}".format(hostname, gpuCount, gpuCount - 1))

nodeConfig = os.popen("slurmd -C").readline().split("\n")[0]

with open("slurm.conf", "w") as  slurm:
    slurm.writelines("ControlMachine={0}\n".format(hostname))
    slurm.writelines("ControlAddr=localhost\n")
    slurm.writelines("MpiDefault=none\n")
    slurm.writelines("ProctrackType=proctrack/linuxproc\n")
    slurm.writelines("ReturnToService=2\n")
    slurm.writelines("SlurmctldPidFile=/var/run/slurmctld.pid\n")
    slurm.writelines("SlurmdPidFile=/var/run/slurmd.pid\n")
    slurm.writelines("SlurmdSpoolDir=/var/spool/slurmd\n")
    slurm.writelines("SlurmUser=slurm\n")
    slurm.writelines("StateSaveLocation=/var/spool/state\n")
    slurm.writelines("SwitchType=switch/none\n")
    slurm.writelines("TaskPlugin=task/affinity\n")
    slurm.writelines("MinJobAge=600\n")
    slurm.writelines("BatchStartTimeout=30\n")
    slurm.writelines("EioTimeout=120\n")
    slurm.writelines("MessageTimeout=60\n")
    slurm.writelines("UnkillableStepTimeout=240\n")
    slurm.writelines("SchedulerType=sched/backfill\n")
    slurm.writelines("SelectType=select/cons_res\n")
    slurm.writelines("SelectTypeParameters=CR_Core_Memory\n")
    slurm.writelines("CpuFreqGovernors=Performance\n")
    slurm.writelines("GresTypes=gpu\n")
    slurm.writelines("DefMemPerCPU=1024\n")
    slurm.writelines("\n")
    slurm.writelines("AccountingStorageType=accounting_storage/slurmdbd\n")
    slurm.writelines("ClusterName={0}\n".format(hostname))
    slurm.writelines("JobAcctGatherFrequency=30\n")
    slurm.writelines("AccountingStorageEnforce=associations,limits,safe\n")
    slurm.writelines("AccountingStorageTRES=gres/gpu\n")
    slurm.writelines("JobAcctGatherType=jobacct_gather/none\n")
    slurm.writelines("JobAcctGatherParams=NoOverMemoryKill,UsePSS\n")
    slurm.writelines("MaxArraySize=5000\n")
    slurm.writelines("\n")
    slurm.writelines("# COMPUTE NODES\n")
    slurm.writelines("\n")
    slurm.writelines("{0} State=UNKNOWN gres=gpu:{1}\n".format(nodeConfig, gpuCount))
    slurm.writelines("\n")
    slurm.writelines("PartitionName=gpu Nodes={0} Default=No MaxTime=168:00:00 State=UP OverSubscribe=No  \\\n".format(hostname))
    slurm.writelines("	DefMemPerCPU=1024 DefaultTime=24:00:00 AllowAccounts={0}s qos={0}sgpu\n".format(hostname))
    slurm.writelines("\n")
    slurm.writelines("PartitionName=cpu Nodes={0} Default=No MaxTime=168:00:00 State=UP OverSubscribe=No  \\\n".format(hostname))
    slurm.writelines("	DefMemPerCPU=1024 DefaultTime=24:00:00 AllowAccounts={0}s qos={0}s\n".format(hostname))


with open("createDB.sql", "w") as  createDB:
    createDB.write()
