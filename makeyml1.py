#!/usr/bin/env python

import sys
import os
import subprocess
import glob
import fnmatch
import re
import scipy as sp
import argparse
from itertools import groupby, chain

"""

Usage : python makeYML_part1.py <sampleListFile> <path_to_fastqDir> <patyml> <outdir_c> <outdir_a> <outdir_s>
Author: Alva James
Purpose : 
    Given the list of sample names and path to the fastq.gz files for those samples, creates YAML input files for the CWL pipeline part1
"""

parser = argparse.ArgumentParser()
parser.add_argument("<sampleListFile>", help="file with the list of sample names in each line")
parser.add_argument("<path_to_fastqDir>", help="directory where the fastq.gz files are stored")
parser.add_argument("<outdir_a>", help="directory where the alignment results should be stored")
parser.add_argument("<ymljobs>", help="directory where the yml submissions should be stored")
parser.add_argument("<outdir_c>", help="directory where the count results should be stored")
parser.add_argument("<outdir_s>", help="directory where the count results should be stored")
parser.parse_args()

samplelistFile = sys.argv[1]
fastqDir  = sys.argv[2]
patyml    = sys.argv[3]
outdir_c  = sys.argv[4]
outdir_a  = sys.argv[5]
outdir_s  = sys.argv[6]

templateFile = '/cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/temp_part1'
samples1     = {}
samples2     = {}
yml_list     = ['spladder_gtf', 'spladder_outDir','spladder_out_dir1','spladder_out_dir2','spladder_confidence','spladder_merge_graphs','spladder_alt','spladder_RL', 'spladder_phase2','spladder_primary_alignment','spladder_validate']  
yml_data     = {} 

fin = open(templateFile, 'r')
for line in fin:
    line = line.strip().split(' ')
    yml_data[line[0]] = line[1]    
fin.close()

FH_sample = open(samplelistFile, 'r')
for line in FH_sample:
    samples1[line.strip().split('\n')[0]] =[]
    samples2[line.strip().split('\n')[0]] =[]
FH_sample.close()
for file in os.listdir(fastqDir):
    m1 = re.search('(.*)_R1', file)
    m2 = re.search('(.*)_R2', file)
    if m1 and m1.group(1) in samples1:
        samples1[m1.group(1)].append(file)
    if m2 and m2.group(1) in samples2:
        samples2[m2.group(1)].append(file)
        
# Merging the dictionaries
        
SAM1 = {}
for k,v in groupby(sorted(samples1.items()), lambda x: x[0].rsplit("_", 1)[0]):
    value = list(v)
    SAM1[value[0][0]] = list(chain.from_iterable([i[1] for i in value]))
SAM2 = {}
for k,v in groupby(sorted(samples2.items()), lambda x: x[0].rsplit("_", 1)[0]):
    value = list(v)
    SAM2[value[0][0]] = list(chain.from_iterable([i[1] for i in value]))
    
# reading input file and collecting the provided information

for sam in SAM1.keys():
    ymlFile = patyml + sam + '_job.yml'
    ymlFH   = open(ymlFile, 'w')
    # writing
    ymlFH.write("reads1: [\n")
    ln1=len(SAM1[sam])
    ct1=0
    for R1 in sorted(SAM1[sam]):
        ct1+=1
        if ct1 < ln1:
            ymlFH.write(" {class: File, path: "+ fastqDir + '/' + R1 + "},\n")
        elif ct1 == ln1 :
            ymlFH.write(" {class: File, path: "+ fastqDir + '/' + R1 + "}\n")
            ymlFH.write("]\n")
    
    # Writing reads2 to the .yml file
    ymlFH.write("reads2: [\n")
    ln2=len(SAM2[sam])
    ct2=0
    for R2 in sorted(SAM2[sam]):
        ct2+=1
        if ct2 < ln2:
            ymlFH.write(" {class: File, path: "+ fastqDir + '/' + R2 + "},\n")
        elif ct2 == ln2 :
            ymlFH.write(" {class: File, path: "+ fastqDir + '/' + R2 + "}\n")
            ymlFH.write("]\n")


     # Writing sample name
    ymlFH.write("sample: " + sam + "\n")

    # star input for BAM name
    ymlFH.write("outSAMattrRGline: " + "ID::" + sam + "\n")
    
    # Writing requirements for FASTQC_check
    ymlFH.write("fastqc_check_script:\n")
    ymlFH.write(" class: File\n")
    ymlFH.write(" path: /cluster/work/grlab/share/software/rnaseq/fastqc_check.sh\n")

    # genomeDir
    ymlFH.write("genomeDir: /cluster/work/grlab/projects/coukos_immuno/genome/hg19_hs37d5.overhang100_STAR\n")

    # genome
    ymlFH.write("genome:\n")
    ymlFH.write(" class: File\n")
    ymlFH.write(" path: /cluster/work/grlab/projects/coukos_immuno/genome/hg19_hs37d5/genome.fa\n")
    # sjdbGTFfile
    ymlFH.write("sjdbGTFfile:\n")
    ymlFH.write(" class: File\n")
    ymlFH.write(" path: /cluster/work/grlab/projects/coukos_immuno/annotation/gencode.v28lift37.annotation.gtf\n")

    # annotation
    ymlFH.write("annotation:\n")
    ymlFH.write(" class: File\n")
    ymlFH.write(" path: /cluster/home/thomasti/phrt_immuno/scripts/gencode.v19.annotation.hs37d5_chr.gtf\n")
    ymlFH.write("bam:\n")
    ymlFH.write(" class: File\n")
    ymlFH.write(" path: " + sam + "Aligned.sortedByCoord.out.bam\n")
    ymlFH.write("exp_out:\n")
    ymlFH.write(" class: File\n")
    ymlFH.write(" path: " + outdir_c + sam + ".tsv\n")
    ymlFH.write("spladder_bam:\n")
    ymlFH.write(" class: File\n")
    ymlFH.write(" path: " + sam + "Aligned.sortedByCoord.out.bam\n")
    for field in yml_list:
        if field not in yml_data:
            print (field, "NOT FOUND. Cannot progress without this field in the input file")
        elif field == 'spladder_gtf' and field in yml_data:
            ymlFH.write("spladder_gtf: \n class: File\n path: " + yml_data['spladder_gtf'] + "\n")
        elif field == 'spladder_outDir' and field in yml_data:
            ymlFH.write("spladder_outDir: "+ yml_data['spladder_outDir'] +"/"+ sam+"'"+ "\n")
        elif field == 'spladder_out_dir1' and field in yml_data:
            ymlFH.write("spladder_out_dir1: "+ yml_data['spladder_out_dir1'] + "\n")    
        elif field == 'spladder_out_dir2' and field in yml_data:
            ymlFH.write("spladder_out_dir2: "+ yml_data['spladder_out_dir2'] + "\n")
        elif field == 'spladder_confidence' and field in yml_data:
            ymlFH.write("spladder_confidence: "+ yml_data['spladder_confidence'] + "\n")
        elif field == 'spladder_merge_graphs' and field in yml_data:
            ymlFH.write("spladder_merge_graphs: " + yml_data['spladder_merge_graphs'] + "\n")
        elif field == 'spladder_phase2' and field in yml_data:
            ymlFH.write("spladder_phase2: " + yml_data['spladder_phase2'] + "\n")
        elif field == 'spladder_alt' and field in yml_data:
            ymlFH.write("spladder_alt: " + yml_data['spladder_alt'] + "\n")
        elif field == 'spladder_RL' and field in yml_data:
            ymlFH.write("spladder_RL: " + yml_data['spladder_RL'] + "\n")
        elif field == 'spladder_primary_alignment' and field in yml_data:
            ymlFH.write("spladder_primary_alignment: " + yml_data['spladder_primary_alignment'] + "\n")
        elif field == 'spladder_validate' and field in yml_data:
            ymlFH.write("spladder_validate: " + yml_data['spladder_validate'] + "\n")
