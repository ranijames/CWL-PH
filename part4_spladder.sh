#!/bin/bash

arg_pass=0

if [ $# -eq 0 ]; then
	echo "Usage: sh `basename $0` <templateFile> <yamlOutFile>"
	arg_pass=1
	echo
	echo "Example: "
	echo "sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/part4_spladder.sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/templateFile_3 /cluster/home/aalva/Projects/PHRT-Immuno/results/PART3/yml3/spladder/part3.yml"
elif [ $1 == "-h" ]; then
	echo "Usage: sh `basename $0` <templateFile> <yamlOutFile>"
	arg_pass=1
	echo
	echo "Example: "
	echo "sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/part4_spladder.sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/templateFile_3 /cluster/home/aalva/Projects/PHRT-Immuno/results/PART3/yml3/spladder/part3.yml"
elif [ $# -lt 2 ]; then
	echo "Usage: sh `basename $0` <templateFile> <yamlOutFile>"
	arg_pass=1
	echo
	echo "Example: "
	echo "sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/part4_spladder.sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/templateFile_3 /cluster/home/aalva/Projects/PHRT-Immuno/results/PART3/yml3/spladder/part3.yml"
fi
cd /cluster/home/aalva/Projects/PHRT-Immuno/results/PART3/yml3/spladder/
if [ ${arg_pass} -eq 0 ] ; then
	templateFile=$1
	yamlOutFile=$2

	echo ${templateFile}
	echo ${yamlOutFile}
	#Making YAML files
	python /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/spladder_4yml.py ${templateFile} ${yamlOutFile}

	# Running the pipeline in luster
	echo "source activate /cluster/home/aalva/software/anaconda/envs/py2
cwltool /cluster/home/aalva/Projects/PHRT-Immuno/scripts/cwl/spladder_part3.cwl" ${yamlOutFile} > ${yamlOutFile%.yml}_job.sh
fi
for f in part3_job.sh;do
    echo bsub -M 80000 -W 48:00 -R "rusage[mem=80000]" -J ${f%%_*} -o ${f%%_*}.job sh ${f}
done >bsub_part4.sh
#sh bsub_part4.sh
