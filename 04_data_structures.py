# Data structures : 4 main: list[], tuple(), dictionary{}, set
# list : ordered, mutable, indexable, duplicate values
# tuple : ordered, immutable, indexable, duplicate values
# dictionary : unordered, mutable, key-value pairs, no duplicate keys
# set : unordered, mutable, no duplicate values

# 1. List
gene_list=["BRCA1", "TP53","gc5p" ]
print(gene_list)
gene_list.append("sum25")
print("After append sum25:",gene_list)
gene_list.insert(1 ,"ABC")
print("After insert ABC at index 1:",gene_list)
gene_list.remove("sum25")
print("After remove sum25:",gene_list)
gene_list[2]="XYZ"
print("updated list:", gene_list)
gene_list.pop(2)
print("After pop(2):",gene_list)


num_list=[5,7,8,11,3]
print("num list:",num_list)
num_list.sort()
print("After sort:",num_list)
num_list.reverse()
print("After reverse:",num_list)
num_list.clear()
print("After clear:",num_list)  #clear() function removes all elements from the list.

# 2. Tuple
gene_tuple=("BRCA1", "TP53","gc5p" )
print("the genes in tuple are:", gene_tuple)

gene_1=((100,200),(500,600))
for start,end in gene_1:
    print("the position of gene 1 start from", start, "and ending to this position is:;", end)

bases=set("ATGCGGGATT")
print("the unique bases of the tuple are:", bases)

# 3. Dictionary

gene_dict={"brca1": 1, "tp53": 2, "gc5p": 3 }
print(gene_dict)
print(type(gene_dict))

