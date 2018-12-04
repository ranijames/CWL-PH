#!/bin/bash
arg_pass=0
#source activate /cluster/home/aalva/software/anaconda/envs/py2
cd /cluster/home/aalva/Projects/PHRT-Immuno/results/PART1/yml/
rm cwl.sh
for file in `ls *yml`
    do
    echo "source activate /cluster/home/aalva/software/anaconda/envs/py2
cwltool /cluster/home/aalva/Projects/PHRT-Immuno/scripts/cwl/pipeline_part1.cwl" ${file} >>cwl.sh
    done
