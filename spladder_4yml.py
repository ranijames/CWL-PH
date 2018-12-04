#!/usr/bin/env python
import sys
import argparse
import os

"""
Program:    makeYML_part2.py /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/templateFile_1 /cluster/home/aalva/Projects/PHRT-Immuno/results/yml2/part2.yml
Purpose:    Generates YAML file for the CWL pipeline part2, given a template file which defines the inputs for the YAML file
Author:     Alva James
Usage:      python makeYML_part2.py <templateFile> <YAMLoutFile>

"""
parser = argparse.ArgumentParser()
parser.add_argument("<templateFile>", help="templateFile contains the template to give the inputs")
parser.add_argument("<patyml>", help="name of the output YAML file")
parser.parse_args()

templateFile = '/cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/templateFile_3'
yamlFile     = '/cluster/home/aalva/Projects/PHRT-Immuno/results/PART3/yml3/spladder/part3.yml'
yml_data      = {}
yml_list      = ['spladder_gtf', 'spladder_dir','spladder_bams','spladder_merge_graphs', 'spladder_phase2','spladder_primary_alignment','spladder_qmode','spladder_quantify_graph']

# reading input file and collecting the provided information
fin = open(templateFile, 'r')
for line in fin:
    line = line.strip().split(' ')
    yml_data[line[0]] = line[1]
fin.close()

ymlFH = open(yamlFile, 'w')

for field in yml_list:
    if field not in yml_data:
        print (field, "NOT FOUND. Cannot progress without this field in the input file")
    elif field == 'spladder_gtf' and field in yml_data:
        ymlFH.write("spladder_gtf: \n class: File\n path: " + yml_data['spladder_gtf'] + "\n")
    elif field == 'spladder_bams' and field in yml_data:
        nbam = len(yml_data['spladder_bams'].split(','))
        ct = 1
        ymlFH.write("spladder_bams: [\n")
        for bam in yml_data['spladder_bams'].split(','):
            if ct < nbam and ct:
                ymlFH.write(" {class: File, path: "+ bam + "},\n")
            elif ct == nbam:
                ymlFH.write(" {class: File, path: "+ bam + "}\n")
            ct+=1
        ymlFH.write("]\n")
    elif field == 'spladder_dir' and field in yml_data:
        ymlFH.write("spladder_dir: \n class: Directory\n path: " + yml_data['spladder_dir'] + "\n")
    elif field == 'spladder_merge_graphs' and field in yml_data:
        ymlFH.write("spladder_merge_graphs: " + yml_data['spladder_merge_graphs'] + "\n")
    elif field == 'spladder_phase2' and field in yml_data:
        ymlFH.write("spladder_phase2: " + yml_data['spladder_phase2'] + "\n")
    elif field == 'spladder_qmode' and field in yml_data:
        ymlFH.write("spladder_qmode: " + yml_data['spladder_qmode'] + "\n")
    elif field == 'spladder_quantify_graph' and field in yml_data:
        ymlFH.write("spladder_quantify_graph: " + yml_data['spladder_quantify_graph'] + "\n")
