import pandas as pd

def prepare_promoter_data(input_file, output_file="cleaned_promoters.csv"):
    # Read file and fix header
    df = pd.read_csv(input_file, sep=None, engine='python', comment="#", header=None)
    df.columns = df.iloc[0]   # First row contains actual column names
    df = df[1:]               # Drop that row from data

    # Rename useful columns
    df = df.rename(columns={
        "1)pmId": "pmId",
        "6)pmSequence": "pmSequence",
        "15)confidenceLevel": "confidenceLevel"
    })

    # Drop missing values
    df = df[["pmId", "pmSequence", "confidenceLevel"]].dropna()

    # Map confidence levels (W, S, C → 0, 1, 2)
    label_map = {"W": 0, "S": 1, "C": 2}
    df["label"] = df["confidenceLevel"].map(label_map)

    # Drop any rows with unmapped labels
    df = df.dropna(subset=["label"])

    # Save result
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} labeled promoter sequences to: {output_file}")

