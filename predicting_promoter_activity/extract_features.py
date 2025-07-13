import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import sys

def promoter_feature_analysis(csv_file):
    try:
        df = pd.read_csv(csv_file)
        sequences = df["pmSequence"].str.upper() 

        all_features = []

        def gc_content(seq):
            return round((seq.count("G") + seq.count("C")) / len(seq), 4)

        def at_content(seq):
            return round((seq.count("A") + seq.count("T")) / len(seq), 4)

        def has_tata_box(seq):
            return int("TATA" in seq)  

        def dinuc_repeats(seq):
            return sum(1 for i in range(len(seq) - 1) if seq[i] == seq[i + 1])

        # Compute 3-mer frequencies
        vectorizer = CountVectorizer(analyzer='char', ngram_range=(3, 3))
        kmer_matrix = vectorizer.fit_transform(sequences)
        kmer_df = pd.DataFrame(kmer_matrix.toarray(), columns=vectorizer.get_feature_names_out())

        for i, seq in enumerate(sequences):
            features = {
                "gc_content": gc_content(seq),
                "at_content": at_content(seq),
                "tata_box": has_tata_box(seq),
                "dinuc_repeat": dinuc_repeats(seq),
                "label": df.loc[i, "label"]
            }
            all_features.append(features)

        feature_df = pd.DataFrame(all_features).reset_index(drop=True)
        final_df = pd.concat([kmer_df, feature_df], axis=1)

        print(" All promoter features extracted")

        # save the result
        final_df.to_csv("promoter_features.csv", index=False)
        print("Saved features to promoter_features.csv")

        return final_df

    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
        sys.exit(1)
