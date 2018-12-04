#!/bin/bash

arg_pass=0

if [  $# -eq 0  ]; then
	echo "Usage: sh `basename $0` <templateFile_2> <yml>"
	echo "Example: "
	echo "sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/spladder_quantify_part3.sh /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/templateFile_2 /cluster/home/aalva/Projects/PHRT-Immuno/results/PART3/yml3/"
    arg_pass=1
fi
if [ ${arg_pass} -eq 0 ] ; then
    templateFile_2=$1
    yml=$2
    python /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_maker/makeYML_spladder3.py ${templateFile_2} ${yml} 
    #Running the pipeline in cluster
    cd /cluster/home/aalva/Projects/PHRT-Immuno/results/PART3/yml3
    rm *.sh
    for file in `ls *.yml`
    	do
        echo "source activate /cluster/home/aalva/software/anaconda/envs/py2
cwltool --enable-ext /cluster/home/aalva/Projects/PHRT-Immuno/scripts/cwl/spladder_part3.cwl" ${file} >>${file}.sh        
        done
fi
rm bsub_spladder.sh
for f in *.yml;do
    echo bsub -M 80000 -W 48:00 -R "rusage[mem=80000]" -J ${f%%_*} -o ${f%%_*}.job sh ${f%%%.*}.sh
done >bsub_spladder_qunatify.sh
#find -name 'bsub_spladder_qunatify.sh' | xargs -I% sh %
