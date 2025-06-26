import sys
def gc_content(dna_seq):
    gc_count=dna_seq.count('G') + dna_seq.count('C')
    return (gc_count / len(dna_seq)) * 100

if __name__=="__main__":
    if len(sys.argv)!=2:
        sys.exit("no seq found")

seq = sys.argv[1]
print("DNA sequence:",seq)
print("GC content in dna seq is:",gc_content(seq))
