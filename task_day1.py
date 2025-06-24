import sys
if len(sys.argv)!=2:  
    sys.exit()

dna_sequence= sys.argv[1]
     
# dna_sequence=input("Enter your DNA sequence:")
print("DNA sequence:", dna_sequence)
print("Length of DNA sequence:",len(dna_sequence))
gc_count=dna_sequence.count('G')+dna_sequence.count('C')
gc_content= gc_count/len(dna_sequence)
print("GC content:",gc_content)
is_valid=all(base in 'ATGC' for base in dna_sequence)
print("IS Valid DNA(contains only ATGC):",is_valid)
print("Occurence of A:",dna_sequence.count('A'))
print("Occurence of T:",dna_sequence.count('T'))
print("Occurence of G:",dna_sequence.count('G'))
print("Occurence of C:",dna_sequence.count('C'))
if is_valid and gc_content>0.4:
    print("High GC content")
else:
    print("Low GC content")
index=len(dna_sequence)-1
reverse_sequence=""
while index>=0:
    reverse_sequence+=dna_sequence[index]
    index-=1
print("Reverse DNA sequence:",reverse_sequence)