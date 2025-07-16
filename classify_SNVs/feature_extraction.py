import pandas as pd

def extract_features(csv_path: str):
    df = pd.read_csv(csv_path, low_memory=False)


    # Nucleotide encodings
    nucleotide_encoding = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

    df['ref_encoded'] = df['ref'].map(nucleotide_encoding)
    df['alt_encoded'] = df['alt'].map(nucleotide_encoding)

    # One-hot for variant types
    df['variant_type'] = df.apply(
        lambda row: 'SNV' if len(row['ref']) == 1 and len(row['alt']) == 1 else 'Indel',
        axis=1
    )
    df = pd.get_dummies(df, columns=['variant_type'])

    feature_cols = ['ref_encoded', 'alt_encoded'] + [col for col in df.columns if col.startswith('variant_type_')]
    X = df[feature_cols].values
    y = df['binary_label'].values

    X = X.astype('float32')
    return X, y
