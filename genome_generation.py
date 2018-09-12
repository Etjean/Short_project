#!/usr/bin/env python3
from Bio.Seq import *
import random as rd



class Genome(Seq):
    def __init__(self, sequence, circular=True):
        Seq.__init__(self, sequence)
        self.circular=circular
        
    def show(self):
        """Prints the attributes and values of the instance"""
        for key, value in self.__dict__.items():
            print('{:30s}{}'.format(key, value))




size_genome= 10000
genome= Genome(''.join(rd.choices(["A", "T", "G", "C"], k=size_genome)), circular=True)
genome.show()








