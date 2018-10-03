Author : Etienne JEAN
Date : 18th september 2018

This program is a de novo genome assembler. 
It uses Euler cycles in balanced De Bruijn Graphs in order to re-assemble a genome from a file of reads obtained by sequencing. See /doc directory for more information.
It runs in python 3. Only the basic libraries are needed. The source code and python executables are in the /src directory.
Some test data to run the program are in the /data directory.
Some results already generated are in the /results directory

All scripts implement a help display. Use the option -h with any of them to show the help.

---------------------------------------------------------------------
Examples of commands to run the program. All of the following should be executed in the base directory.


I - Generation of a random genome
Random genome of size 10kb
	src/genome_generation.py 10000 > data/random_10kb.fasta
Random genome of size 1Mb, with 60% GC content
	src/genome_generation.py 1000000 --gc-content 0.6 > data/random_1Mb.fasta


II - Sequencing simulation of a genome
Sequencing with default parameters (reads 100bp, coverage 50)
	src/sequencing.py data/random_10kb.fasta > data/random_10kb_reads.fasta
Sequencing with read length 120bp and coverage 60
	src/sequencing.py data/random_1Mb.fasta -l 120 -c 60 > data/random_1Mb_reads.fasta
Sequencing the genome of Mycoplasma geniotalium, read length 400bp, coverage 100
	src/sequencing.py -l 400 -c 100 data/NC_000908.2.fasta > data/NC_000908.2_reads.fasta


III - De novo assembly from a file of reads
De novo assembly of the genome of size 10kb, with k-mers length 30bp
	src/denovo_assembly.py 30 data/random_10kb_reads.fasta results/random_10kb_assembly.fasta > random_10kb_assembly.log
De novo assembly of the genome of size 1Mb, with k-mers length 60bp
	src/denovo_assembly.py 60 data/random_1Mb_reads.fasta results/random_1Mb_assembly.fasta > results/random_1Mb_assembly.log
De novo assembly of the genome of Mycoplasma genitalium, k-mers length 250bp
	src/denovo_assembly.py 250 data/NC_000908.2_reads.fasta results/NC_000908.2_assembly.fasta > results/NC_000908.2_assembly.log


IV - Compare the assembly with the reference genome
Test between reference and assembly for genome of size 10kb
	src/test_assembly.py data/random_10kb.fasta results/random_10kb_assembly.fasta 
Test between reference and assembly for genome of size 1Mb
	src/test_assembly.py data/random_1Mb.fasta results/random_1Mb_assembly.fasta
Test between reference and assembly for genome of Mycoplasma genitalium
	src/test_assembly.py data/NC_000908.2.fasta results/NC_000908.2_assembly.fasta