#!/usr/bin/env python

import sys
import argparse

"""
Program:    makeYML_part2.py /cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/templateFile_1 /cluster/home/aalva/Projects/PHRT-Immuno/results/yml2/part2.yml
Purpose:    Generates YAML file for the CWL pipeline part2, given a template file which defines the inputs for the YAML file
Author:     Alva James
Usage:      python makeYML_part2.py <templateFile> <YAMLoutFile>   

"""
parser = argparse.ArgumentParser()
parser.add_argument("<templateFile>", help="templateFile contains the template to give the inputs")
parser.add_argument("<yamlOutFile>", help="name of the output YAML file")
parser.parse_args()


templateFile = sys.argv[1]
yamlFile = sys.argv[2]

#templateFile = '/cluster/home/aalva/Projects/PHRT-Immuno/scripts/yml_scripts/templateFile_1'
#yamlFile     = '/cluster/home/aalva/Projects/PHRT-Immuno/results/yml2/part2.yml'
yml_data     = {}
yml_list     = ['incremnet_tsv','spladder_gtf', 'spladder_outDir','spladder_out_dir1','spladder_out_dir2', 'spladder_bams','spladder_confidence','spladder_merge_graphs','spladder_alt','spladder_RL', 'spladder_phase2','spladder_primary_alignment', 'samples', 'peptide_outDir', 'reference','gtexJunction','spladder_validate']  

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
    elif field == 'incremnet_tsv' and field in yml_data:
        ymlFH.write("sample: sample.hdf5\n")
        ymlFH.write("inputs:\n")
        ymlFH.write(" sample: File\n")
        ymlFH.write("increment_out: " + "'./sample.hdf5'" + "\n")
        ntsv = len(yml_data['incremnet_tsv'].split(','))
        ct = 1
        ymlFH.write("incremnet_tsv: [\n")
        for tsv in yml_data['incremnet_tsv'].split(','):
            if ct < ntsv and ct:
                ymlFH.write(" {class: File, path: "+ tsv + "},\n")
            elif ct == ntsv:
                ymlFH.write(" {class: File, path: "+ tsv + "}\n")
            ct+=1
        ymlFH.write("]\n")
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
    elif field == 'spladder_outDir' and field in yml_data:
        ymlFH.write("spladder_outDir: "+ yml_data['spladder_outDir'] + "\n")
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
    elif field == 'samples' and field in yml_data:
        ymlFH.write("samples: " + yml_data['samples'] + "\n") 
    elif field == 'peptide_outDir' and field in yml_data:
        ymlFH.write('peptide_outDir: ' + yml_data['peptide_outDir'] + "\n")
    elif field == 'reference' and field in yml_data:
        ymlFH.write("reference: \n class: File\n path: " + yml_data['reference'] + "\n")
    elif field == 'gtexJunction' and field in yml_data:
        ymlFH.write("gtexJunction: \n class: File\n path: " + yml_data['gtexJunction'] + "\n")