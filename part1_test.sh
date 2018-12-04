#!/bin/bash

arg_pass=0

if [  $# -eq 0  ]; then
	echo "Usage: sh `basename $0` <samplelistFile> <fastqDir> <yml> <count> <alignment>"
	echo "Example: "
	echo "sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/part1_test.sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/useage_shell/sample_fastqs1 /cluster/work/grlab/projects/coukos_immuno/data/20180802/fastqs /cluster/home/aalva/Projects/PHRT-Immuno/results/PART1/yml/ /cluster/home/aalva/Projects/PHRT-Immuno/results/counts/  /cluster/home/aalva/Projects/PHRT-Immuno/results/alignment/ /cluster/home/aalva/Projects/PHRT-Immuno/results/PART1/spladder_out"
    arg_pass=1
fi

if [ ${arg_pass} -eq 0 ] ; then
    samplelistFile=$1
    fastqDir=$2
    yml=$3
    count=$4
    alignment=$5
    spladder=$6
    

	#Making YAML files
	python /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/makeyml1.py ${samplelistFile} ${fastqDir} ${yml} ${count} ${alignment} ${spladders}
	# Running the pipeline in cluster
	cd $3
        rm *.sh
	for file in `ls *yml`
    	    do
            echo "source activate /cluster/home/aalva/software/anaconda/envs/py2
cwltool /cluster/home/aalva/Projects/PHRT-Immuno/scripts/cwl/pipeline_part1.cwl" ${file} >>${file}.sh
 	    #exit           
            done
fi
cd $3
jobname=`ls -1 *yml| xargs -I% echo % | cut -d'_' -f 1` 
rm bsub_command.sh
for f in *yml;do
    echo bsub -M 80000 -W 48:00 -R "rusage[mem=80000]" -J ${f%%_*} -o ${f%%_*}.job sh ${f%%%.*}.sh
done >bsub_command.sh
#find -name 'bsub_command.sh' | xargs -I% sh %
