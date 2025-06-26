import sys
if len(sys.argv)>1:
    sys.exit()
    sequence_file= sys.argv[1]
    print(f"processing sequence file: {sequence_file}")
else:
    print("no sequence file provided")

# dna= sys.argv[1]
# rna=sys.argv[2]
# print("the dna seq", dna)
# print("the rna seq", rna)

# import sys
# print("Python version:",sys.version)
# print("Operating system:",sys.platform)
