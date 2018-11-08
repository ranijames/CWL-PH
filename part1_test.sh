#!/bin/bash

arg_pass=0

if [  $# -eq 0  ]; then
	echo "Usage: sh `basename $0` <samplelistFile> <fastqDir> <yml> <count> <alignment>"
	echo "Example: "
	echo "sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/part1_test.sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/useage_shell/sample_fastqs1 /cluster/work/grlab/projects/coukos_immuno/data/20180802/fastqs /cluster/home/aalva/Projects/PHRT-Immuno/results/PART1/yml/ /cluster/home/aalva/Projects/PHRT-Immuno/results/counts/  /cluster/home/aalva/Projects/PHRT-Immuno/results/alignment/"
    arg_pass=1
fi

if [ ${arg_pass} -eq 0 ] ; then
    samplelistFile=$1
	fastqDir=$2
	yml=$3
    count=$4
    alignment=$5
    

	#Making YAML files
	python /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/makeyml1.py ${samplelistFile} ${fastqDir} ${yml} ${count} ${alignment}

        source activating.sh
	# Running the pipeline in cluster
fi
ls -1  ${yml}/*yml | xargs -I% echo bsub -M 60000 -W 12:00 -R "rusage[mem=60000]"  -J % -o %.job cwltool /cluster/home/aalva/Projects/PHRT-Immuno/scripts/cwl/pipline1_test.cwl %  >cmd.sh
find -name 'activating.sh | xargs -I% echo source %'
find -name 'cmd.sh' | xargs -I% sh %
	


