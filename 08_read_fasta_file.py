import sys
def reader(fasta):
    seq=fasta
    try:
        with open(seq,'r') as f:
            lines =f.readlines()

            header= lines[0].strip
            sequence=""
            for i in lines[1:]:
                sequence+=i.strip()

                print("the fasta header is this:", header)
                print("the fasta sequence is this:", sequence)

        return
    except FileNotFoundError:
       print("the file is not fouond in directory")

if __name__== "main__":
    if len(sys.argv)!=2:
        sys.exit("invalid argument")



