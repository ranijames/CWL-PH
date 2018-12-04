#!/bin/bash

arg_pass=0

if [ $# -eq 0 ]; then
	echo "Usage: sh `basename $0` <templateFile> <yamlOutFile>"
	arg_pass=1
	echo
	echo "Example: "
	echo "sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/part2.sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/templateFile_1 /cluster/work/grlab/projects/alva_temp/Alignment/part2.yml"
elif [ $1 == "-h" ]; then
	echo "Usage: sh `basename $0` <templateFile> <yamlOutFile>"
	arg_pass=1
	echo
	echo "Example: "
	echo "sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/part2.sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/templateFile_1 /cluster/work/grlab/projects/alva_temp/Alignment/part2yml"
elif [ $# -lt 2 ]; then	
	echo "Usage: sh `basename $0` <templateFile> <yamlOutFile>"
	arg_pass=1
	echo
	echo "Example: "
	echo "sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/part2.sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/templateFile_1 /cluster/work/grlab/projects/alva_temp/Alignment/part2.yml"
fi
find /cluster/home/aalva/Projects/PHRT-Immuno/results/PART1/spladder_out1/ -name '*.out.pickle' -exec cp {} /cluster/work/grlab/projects/alva_temp/Alignment/ \;
cd /cluster/work/grlab/projects/alva_temp/Alignment/
if [ ${arg_pass} -eq 0 ] ; then
	templateFile=$1
	yamlOutFile=$2

	echo ${templateFile}
	echo ${yamlOutFile}
	#Making YAML files
	python /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/makeYML_part2.py ${templateFile} ${yamlOutFile}

	# Running the pipeline in luster
	echo "source activate /cluster/home/aalva/software/anaconda/envs/py2
cwltool /cluster/home/aalva/Projects/PHRT-Immuno/scripts/cwl/pipeline_part2.cwl" ${yamlOutFile} > ${yamlOutFile%.yml}_job.sh
fi
for f in part2_job.sh;do
    echo bsub -M 80000 -W 48:00 -R "rusage[mem=80000]" -J ${f%%_*} -o ${f%%_*}.job sh ${f}
done >bsub_part2.sh
#sh bsub_part2.sh.sh
	
