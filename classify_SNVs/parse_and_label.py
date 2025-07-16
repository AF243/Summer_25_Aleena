import pandas as pd

def parse_and_label_vcf(vcf_path: str, output_csv: str = "cleaned_variants.csv"):
    records = []
    with open(vcf_path, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            chrom, pos, _id, ref, alt, qual, filter_, info = fields[:8]

            info_dict = {kv.split('=')[0]: kv.split('=')[1] for kv in info.split(';') if '=' in kv}

            clnsig = info_dict.get('CLNSIG', 'unknown')
            records.append({
                'chrom': chrom,
                'pos': pos,
                'ref': ref,
                'alt': alt,
                'clnsig_raw': clnsig
            })

    df = pd.DataFrame(records)
    df['clnsig_raw'] = df['clnsig_raw'].str.lower()

    deleterious = ['pathogenic', 'likely_pathogenic']
    neutral = ['benign', 'likely_benign']

    def map_label(val):
        for d in deleterious:
            if d in val:
                return 1
        for n in neutral:
            if n in val:
                return 0
        return None

    df['binary_label'] = df['clnsig_raw'].apply(map_label)
    df_cleaned = df.dropna(subset=['binary_label'])

    df_cleaned.to_csv(output_csv, index=False)
    print(f"Saved cleaned data with {len(df_cleaned)} rows to '{output_csv}'")

    return output_csv 
