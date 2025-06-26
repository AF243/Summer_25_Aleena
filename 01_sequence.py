# dna_sequence= "TCCAACCGTCCACAGTGAGCCACGTCGCCCAACAAATCTCACACAACAGATCCAGATCCGACAC"
# print("DNA Sequence:", dna_sequence)

import csv
def calculate_gc_content(sequence):
    if len(sequence) == 0:
        return 0
    gc_count = sequence.count('G') + sequence.count('C')
    return int((gc_count / len(sequence)) * 100)

def validate_sequence(sequence):
    return all(base in ('A', 'T', 'C', 'G') for base in sequence)

def get_unique_nucleotides (dna_seq):
    unique_nucleotides = set()
    for seq in dna_seq.values():
        unique_nucleotides.update(seq)
    return unique_nucleotides

def read_fasta(file_path):
    sequences = {}
    with open(file_path, 'r') as f:
        current_id = ""
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                current_id = line[1:]
                sequences[current_id] =""
            else :
                sequences[current_id] += line
    return sequences

def save_to_csv(sequences,output_csv):
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id","length", "gc_content", "valid_dna"])
        for id, seq in sequences.items():
            length= len(seq)
            gc_content_val = calculate_gc_content(seq)
            is_valid = validate_sequence(seq)
            writer.writerow([id, len(seq), gc_content_val, is_valid])

if __name__=="__main__":    
    fasta_file = 'sequence.fasta'
    output_file= "output.csv"
    sequences = read_fasta(fasta_file)
    save_to_csv(sequences, output_file)

print("Unique nucleotides found across all sequences:", get_unique_nucleotides(sequences))
print("Analysis complete. Results saved to:", output_file)