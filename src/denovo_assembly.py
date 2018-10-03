#!/usr/bin/env python3
import time
import argparse


class Read:
    """Representation of a sequencing read."""
    def __init__(self, sequence):
        self.sequence = sequence
        
    def generate_kmers(self, kmers_length):
        """Returns a list of the k-mers (as strings) included in the read."""
        kmers=[]
        for i in range(len(self.sequence) - kmers_length):
            kmer = self.sequence[i:i+kmers_length]
            kmers.append(kmer)
        return kmers


class Graph:
    """Representation of a De Bruijn graph for de novo genome assembly."""
    def __init__(self):
        self.vertices = {}
        self.edges = {}
        self.euler_cycles = []
        self.euler_biggest = []
    
    def add_vertex(self, seq):
        """Add a vertex to the graph"""
        if seq not in self.vertices:
            # If the vertex does not exist, create it
            v = Vertex(seq)
            self.vertices[seq] = v
            return v
        else:
            # If it already exists, just get it
            return self.vertices[seq]
    
    def add_edge(self, seq, v_from, v_to):
        """Add an edge to the graph, connecting two vertices"""
        if seq not in self.edges:
            # If the edge does not exist, create it
            e = Edge(seq, v_from, v_to)
            self.edges[seq] = e
            return e
        else:
            # It it already exists, just get it
            return self.edges[seq]

    def test_eulerian(self):
        """Returns True if the graph is Eulerian, False otherwise."""
        # The graph is Eulerian if, for all vertices, indegree = outdegree
        for vertex in self.vertices.values():
            if len(vertex.edges_in) != len(vertex.edges_out):
                print('PROBLEM : This graph is not Eulerian.')
                return False
        print('SUCCESS : This graph is Eulerian !')
        return True
    
    def find_cycle(self):
        """Returns a list of edges forming an Euler cycle in the graph. 
        Simultaneously deletes those edges from the graph."""
        # Get an edge, and delete it from the graph
        edge = self.edges.popitem()[1]
        # Add the vertex it is pointing to to the cycle
        cycle = [edge.vertex_from]
        # Get next edge : get one edge that point out of the vertex
        e = edge.vertex_to.edges_out.pop()
        # Continue until closing the cycle
        while e != edge:
            self.edges.pop(e.sequence)
            cycle.append(e.vertex_from)
            e = e.vertex_to.edges_out.pop()
        return cycle
    
    def find_all_cycles(self):
        """Returns a list of all Euler cycles in the graph."""
        while len(self.edges) > 0:
            self.euler_cycles.append(self.find_cycle())
            
    def assemble_cycles(self, cycle, tab):
        """Assembles all Euler cycles previously found into the biggest Euler 
        cycle possible in the graph."""
        # Take one cycle, and add its vertices to the biggest cycle
        for v in cycle:
            self.euler_biggest.append(v)
            # If one vertex is also part of another cycle
            for c in tab:
                if v in c:
                    # Recursively call the function
                    # Give it the next cycle to look in,
                    # and re-order it so that the first vertex is the one we found.
                    nextcycle = c[c.index(v)+1:] + c[:c.index(v)+1]
                    # Give it a sub-list of cycles, without nextcycle in it.
                    nexttab = tab[:tab.index(c)] + tab[tab.index(c)+1:]
                    self.assemble_cycles(nextcycle, nexttab)
                    tab.remove(c)
                    break

    def assemble_sequence(self):
        """Returns a re-assembly of the genome's sequence."""
        genome_assembly = ''
        # Add the first nucleotide of each vertex to the sequence
        for v in self.euler_biggest:
            genome_assembly += v.sequence[0]
        return genome_assembly


class Edge:
    """Representation of an Edge of a directed De Bruijn graph."""
    def __init__(self, sequence, vertex_from, vertex_to):
        self.sequence = sequence
        self.vertex_from = vertex_from
        self.vertex_to = vertex_to


class Vertex:
    """Representation of a vertex of a directed De Bruijn graph."""
    def __init__(self, sequence):
        self.sequence = sequence
        self.edges_in = set()
        self.edges_out = set()


# MAIN PROGRAM
if __name__ == "__main__":
    # Arguments parsing
    parser = argparse.ArgumentParser(description='Returns a de novo genome assembly from a list of reads in ".fasta" format.')
    parser.add_argument('k', type=int,
                        help='Length of the k-mers. Ranges from 1 to the length of the reads. \
                        If k-mers are too short : the graph will not be Eulerian, thus making the assembly impossible. \
                        If k-mers are too long : they are likely to be too close to the size of the reads, implying getting too few of them for the assembly. \
                        To increase the k-mers length more, try increasing the sequencing coverage and/or the length of the reads.')
    parser.add_argument('file_in', type=str,
                        help='Input ".fasta" file of the reads from which to execute the assembly.')
    parser.add_argument('file_out', type=str, 
                        help='Output ".fasta" file of the de novo genome assembly.')
    parser.add_argument('--fasta-header', type=str, default='De novo genome assembly',
                        help='Header of the ".fasta" output file FILE_OUT. Default is "De novo genome assembly".')
    args = parser.parse_args()

    # Memorize starting time
    t = time.time()

    # Graph creation (empty)
    graph = Graph()

    # File parsing : Vertices & Edges generation
    with open(args.file_in, 'r') as f:
        print('Parsing file '+args.file_in)
        
        # Do not consider the fasta header of the read
        f.readline()
        
        # Get the read sequence
        read_seq = f.readline().rstrip('\n')
        
        # Iteration for all reads in the file
        i = 0
        while read_seq != '':
            # Increase the counter and print it out every 10000 reads
            i+=1
            if i%10000 == 0:
                print(str(i)+' reads parsed', end = '\r')
            
            # Create a Read object from the read sequence
            r = Read(read_seq)
            
            # Generate k-mers included inside the read sequence
            for kmer in r.generate_kmers(kmers_length=args.k):
                # Create Vertices
                v_from = graph.add_vertex(kmer[:-1])  # prefix
                v_to = graph.add_vertex(kmer[1:])     # suffix
                # Create Edges
                e = graph.add_edge(kmer, v_from, v_to)
                # Add this edge into the vertices attributes
                v_from.edges_out.add(e)
                v_to.edges_in.add(e)
            
            # Get next read sequence
            f.readline()
            read_seq = f.readline().rstrip('\n')
    
    # Print total number of reads parsed
    print(str(i)+' reads parsed in total', end = '\r')

    # Test if the graph is eulerian
    eulerian = graph.test_eulerian()

    # Print number of edges and vertices
    print(str(len(graph.edges))+' edges')
    print(str(len(graph.vertices))+' vertices')

    # If the graph is not eulerian : end the program and return nothing
    if not eulerian:
        print('K-mers need to be longer to get an Eulerian graph. Use --help for more info.')

    # If the graph is eulerian : do the de novo assembly
    else:
        # Find all euler cycles in the graph
        graph.find_all_cycles()
        print('{} Euler cycle{} found in the graph'.format(len(graph.euler_cycles), 's' if len(graph.euler_cycles)>1 else ''))
        
        # Assemble cycles into one big euler cycle
        graph.assemble_cycles(graph.euler_cycles[0], graph.euler_cycles[1:])
        
        # Re-assemble the genome's sequence
        genome_assembly = graph.assemble_sequence()
        
        # Write to output file
        with open(args.file_out, 'w') as fo:
            # Write fasta header
            fo.write('>'+args.fasta_header+'\n')
            for i in range(0, len(genome_assembly), 80):
                # Write genome assembly, and cut line every 80 characters
                fo.write(genome_assembly[i:i+80]+'\n')

    # Print total time
    print('Total execution time : {:.1f}s'.format(float(time.time()-t)))