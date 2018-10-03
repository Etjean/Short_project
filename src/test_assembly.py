#! /usr/bin/env python3
import sequencing
import argparse


# Arguments parsing
parser = argparse.ArgumentParser(description='Compares a re-assembled genome with the reference genome.')
parser.add_argument('file_ref', type=str,
                    help='Input ".fasta" file of the reference genome.')
parser.add_argument('file_ass', type=str, 
                    help='Input ".fasta" file of the de novo genome assembly.')
args = parser.parse_args()

# Load both genomes
genome_reference = sequencing.Genome()
genome_reference.load_genome(args.file_ref)
genome_assembly = sequencing.Genome()
genome_assembly.load_genome(args.file_ass)

# Compare both sequence, taking into account that both genome are circular
if genome_reference.sequence in genome_assembly.sequence*2:
    print('BRAVO : The re-assembled genome matches the reference genome !!')
else :  
    print('SORRY : The re-assembled genome does not match the reference genome.')