#!/usr/bin/env python3
import random as rd
import argparse


class Range(object):
    """Representation of a floating range."""
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __eq__(self, other):
        """Float numbers from start to end are equal to any instance of this class"""
        return self.start <= other <= self.end
    def __repr__(self):
        """Reoresentation of this class under the form 'start-end'"""
        return '{}-{}'.format(self.start, self.end)


if __name__ == "__main__":
    # Arguments parsing
    parser = argparse.ArgumentParser(description='Generates a random genome of length L. It prints as ".fasta" format to standard output')
    parser.add_argument('l', type=int, 
                        help='length of the genome to generate')
    parser.add_argument('-g', '--gc-content', type=float, default=0.5, choices=[Range(0., 1.)],
                        help='GC content of the genome, ranging from 0 to 1')
    args = parser.parse_args()

    # Fasta header
    fasta_header = 'Random Genome, size='+str(args.l)+', GC content='+str(args.gc_content)
    print('>'+fasta_header)

    # Genomic sequence generation
    i = 1
    while i <= args.l:
        # Print 1 random nucleotide
        nt = rd.choices(['A', 'T', 'G', 'C'], weights=(1-args.gc_content, 1-args.gc_content, args.gc_content, args.gc_content))[0]
        print(nt, end='')
        #  Cut in lines of length 80
        if i%80 == 0:
            print()
        # Increase counter
        i += 1

    # Add new line in the end
    print()