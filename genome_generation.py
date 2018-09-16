#!/usr/bin/env python3
import random as rd












size_genome= 10000
genome= Genome(''.join(rd.choices(["A", "T", "G", "C"], k=size_genome)), circular=True)
genome.show()








