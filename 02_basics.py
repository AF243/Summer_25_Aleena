dna="ATGC"
print(dna)
print(type(dna))
length=4
print(length)
print(type(length))
is_dna= True
print(type(is_dna))

dna=5
rna=6
add=dna+rna
print("conactenation=", add)
seq_1="ATGC"
seq_2="ATGGC"
print("seq 1 is equal to seq 2:",seq_1==seq_2)
print("seq 1 is not equal to seq 2:",seq_1!=seq_2)

dna="ATGCCGATTTAACGC"
threshold=10
gc_content=dna.count('G') + dna.count('C')

if gc_content==threshold:
    print("GC content is equals to threshold")
elif gc_content > threshold:
    print("GC content is not equals to threshold")
elif gc_content < threshold:
    print("GC content is less than threshold")
else:
    print(gc_content)

dna=input("enter a DNA sequence:")
print("received DNA:",dna)
gene_id=input("Enter a gene id:")
print("Processing gene id:{gene_id}")
expression=float(input("Enter gene expression level:"))
print(f"Expression level:{expression}")



dna= "ATGCGCGGC"
print("sequence length:",len(dna))
gc_count=dna.count('G')+dna.count('C')
gc_content=gc_count/len(dna)
print("GC content:",gc_content)

dna="ATGX"
is_valid=all(base in 'ATGC' for base in dna)
print("IS Valid DNA:",is_valid)