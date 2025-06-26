import sys
def read_fasta(file_path):
    sequences={}
    try:
        with open(file_path, 'r') as file:
            header=''
            for line in file:
                line= line.strip()
                if line.startswith('>'):
                    header=line
                    if header in sequences:
                        raise ValueError("Duplicate header found")
                    sequences[header]=""
                else:
                    sequences[header]+=line
    except FileNotFoundError:
        print("file not found")
    return sequences

def filter_sequences(sequences, min_length):
    filtered_sequence={}
    for header, seq in sequences.items():
            print(f"{header}| Length:{len(seq)}")
            if len(seq)>= min_length:
             filtered_sequence[header]=seq
    return filtered_sequence

def write_fasta(sequences, output_path):
    try:
        with open(output_path,'w')as file:
            for header,seq in sequences.items():
                file.write(f"{header}\n")
                file.write(f"{seq}\n")
    except Exception as e:
        print(f"error writing to file{e}")

def main():
    if len(sys.argv)!=4:
        print("Invalid argument, Enter file_name, input.fasta, output.fasta min_length")
        sys.exit(1)

    input_file= sys.argv[1]
    try:
            min_length= int(sys.argv[2])
    except ValueError:
            print("Error:Minimum length must be an integer")
            sys.exit(1)
    output_file=sys.argv[3]
       
    sequences=read_fasta(input_file)
    filtered=filter_sequences(sequences,min_length)
    write_fasta(filtered,output_file)
    print("Input file:",input_file)
    print("Output file:",output_file)
    print("Total sequences read:",len(sequences))
    print("Sequences passed the length filter:",len(filtered))

if __name__=="__main__":
    main()