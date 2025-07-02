from Bio import AlignIO
from Bio import pairwise2
from Bio.Seq import Seq
import sys

def align_seq(seq1, seq2, match=2, mismatch=-2, gap_open=-2, gap_extended=-2):
    alignment= pairwise2.align.globalms(seq1,seq2,match, mismatch, gap_open, gap_extended)
    best_alignment=alignment[0]

    print("the alignment score is:",best_alignment.score)
    print("the aligned sequence 1 is:",best_alignment.seqA)
    print("the aligned sequence 2 is:",best_alignment.seqB)
    print("the start of alignment is:", best_alignment.start)        # gives starting index
    print("the end of alignment is:", best_alignment.end)            # gives ending index
    return best_alignment

def similarity(alignment):
    # seq1=alignment.seqA
    # seq2=alignment.seqB
    aligned1=alignment.seqA
    aligned2=alignment.seqB
    matches=0
    for i in range(len(aligned1)):
        if aligned1[i]==aligned2[i] and aligned1!='-':
            matches+=1

    length = len(aligned1)
    similarity=(matches/length)*100 if length>0 else 0   
    print("the similarity of the alignment is:",similarity,'%')
    return

# calculating gap frequency
def gap_frequency(alignment):
    seq1=alignment.seqA
    seq2=alignment.seqB
    gapA=seq1.count('-')
    gapB=seq2.count('-')
    alignment_length = len(seq1)
    total_gaps = gapA + gapB
    gap_frequency = (total_gaps / (alignment_length * 2)) * 100
    print("Gap frequency:",gap_frequency,"%")
    return

# find conserved regions
def conserved_regions(alignment):
    seq1 = alignment.seqA
    seq2 = alignment.seqB
    conserved_regions = []
    threshold = 6
    i = 0

    while i <= len(seq1) - threshold:
        if all(seq1[i + j] == seq2[i + j] != '-' for j in range(threshold)):
            start = i
            region = seq1[i:i+threshold]
            i += threshold
            while i < len(seq1) and seq1[i] == seq2[i] != '-':
                region += seq1[i]
                i += 1
            conserved_regions.append((start, i - 1, region))
        else:
            i += 1
    if conserved_regions:
        print(f"Conserved regions of at least {threshold} bp (no gaps, perfect match):")
        for start, end, region in conserved_regions:
            print(f"Start: {start}, End: {end}, Length: {end-start+1}, Sequence: {region}")
    else:
        print(f"No conserved regions of length ≥ {threshold}")

# if __name__ == "__main__":
#     if len(sys.argv)!=3:
#         sys.exit("Invalid argument")
        
# seq1=sys.argv[1]
# seq2=sys.argv[2]

seq1="ACGACAGCGACTGCAGTTATATACGCAGAGTAGACGACGACGACGAGGGCCCTATTAGGGGGACCCCATAGAGGAGAG"
seq2="ATCGATAGCAGTAGACGATAGACGACAGCGACTGCAGTTATATACGCAGAGTAGACGACGACGACGACTATTAGGGGGACCCCATAGAGGAGAGAGAGGAGAGGAAATTTCAA"
alignment_results=align_seq(seq1,seq2)
similarity(alignment_results)
gap_frequency(alignment_results)
conserved_regions(alignment_results)
