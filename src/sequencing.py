#!/usr/bin/env python3
import random as rd
import argparse


class Genome:
    """Representation of a genome."""
    def __init__(self):
        self.sequence = ''
    
    def load_genome(self, file):
        """Loads the genome's sequence into memory from a fasta file."""
        with open(file, 'r') as f:
            # Do not consider the fasta header
            f.readline()
            # Reconstructs the genome sequence
            self.sequence=''
            for line in f:
                self.sequence += line.rstrip('\n')

    def generate_read(self, read_length):
        """Returns a read sequence from a random position in the genome."""
        # Define a random start position for the read
        start = rd.randint(0, len(self.sequence)-1)
        # Return the read sequence, taking into account that the genome is circular
        read_seq = self.sequence[start:min(start+read_length, len(self.sequence))] + \
                    self.sequence[0:max(start+read_length-len(self.sequence), 0)]
        return read_seq


# MAIN PROGRAM
if __name__ == "__main__":
     # Arguments parsing
    parser = argparse.ArgumentParser(description='Simulates the sequencing of a genome. It prints reads in ".fasta" format to standard output.')
    parser.add_argument('-l', type=int, default=100,
                        help='Length of the reads. Positive values only. Default is 100.')
    parser.add_argument('-c', type=int, default=50,
                        help='Coverage of the sequencing. Positives values only. Default is 50.')
    parser.add_argument('file', type=str, 
                        help='Input fasta file of the genome to sequence.')
    args = parser.parse_args()

    # Loads genome into memory
    genome = Genome()
    genome.load_genome(args.file)

    # Get filename
    filename=args.file.split('/')[-1]

    # Generate and print reads
    for i in range(args.c*len(genome.sequence)//args.l):
        # Print fasta header for the read. Define read ids as 'filename.id'
        print('>'+filename+'.'+str(i+1))
        # Print read sequence
        print(genome.generate_read(args.l))