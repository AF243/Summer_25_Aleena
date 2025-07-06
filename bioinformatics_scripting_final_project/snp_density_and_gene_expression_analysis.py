import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Step 1: Parse GFF and extract exons (2L only, with FBgn conversion)
def get_exons_from_gff(gff_filename):
    print("\n Parsing GFF file for exon coordinates on 2L only...")
    exons = {}
    transcript_to_gene = {}

    with open(gff_filename, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) != 9:
                continue
            feature = parts[2]
            chrom = parts[0]
            start = int(parts[3])
            end = int(parts[4])
            attributes = parts[8]

            if feature in ["mRNA", "transcript", "lnc_RNA", "ncRNA", "tRNA", "rRNA"]:
                transcript_id = ""
                gene_id = ""
                for item in attributes.split(";"):
                    if "ID=" in item:
                        transcript_id = item.split("=")[-1].strip()
                    elif "Parent=" in item:
                        gene_id = item.split("=")[-1].strip()
                if transcript_id and gene_id:
                    transcript_to_gene[transcript_id] = gene_id

            elif feature.lower() == "exon" and chrom == "2L":
                for item in attributes.split(";"):
                    if "Parent=" in item:
                        parent_id = item.split("=")[-1].strip()
                        break
                gene_id = transcript_to_gene.get(parent_id)
                if gene_id:
                    if gene_id not in exons:
                        exons[gene_id] = []
                    exons[gene_id].append((chrom, start, end))

    print(f"Extracted {len(exons)} genes with exons on 2L (FBgn IDs).")
    return exons

# Step 2: Parse VCF and extract SNP positions
def get_snp_positions(vcf_filename):
    print("\n Reading SNP positions from VCF file...")
    snps = {}
    with open(vcf_filename, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            chrom = parts[0]
            pos = int(parts[1])
            snps.setdefault(chrom, []).append(pos)
    print(f"SNPs loaded for {len(snps)} chromosomes.")
    return snps

# Step 3: Map SNPs to exons
def map_snps_to_exons(exons, snps):
    print("\nMapping SNPs to exons...")
    snp_counts = {}
    for gene_id, regions in exons.items():
        count = 0
        for chrom, start, end in regions:
            if chrom in snps:
                for snp in snps[chrom]:
                    if start <= snp <= end:
                        count += 1
        snp_counts[gene_id] = count
    print("SNP mapping complete.")
    return snp_counts

# Step 4: Calculate exon lengths
def calculate_exon_lengths(exons):
    print("\nCalculating exon lengths...")
    exon_lengths = {}
    for gene_id, regions in exons.items():
        total = sum(end - start + 1 for _, start, end in regions)
        exon_lengths[gene_id] = total
    print(f"Calculated lengths for {len(exon_lengths)} genes.")
    return exon_lengths

# Step 5: Parse gene expression file
def read_expression_data(expression_file):
    print(f"\nReading gene expression data from: {expression_file}...")
    expression_data = {}
    try:
        df = pd.read_csv(expression_file, sep='\t')
        df.columns = df.columns.str.strip()
        gene_column = df.columns[0]
        expression_columns = df.columns[1:]
        for _, row in df.iterrows():
            gene_id = str(row[gene_column]).strip()
            avg_expr = row[expression_columns].astype(float).mean()
            expression_data[gene_id] = avg_expr
        print(f"Expression data loaded for {len(expression_data)} genes.")
    except Exception as e:
        print(f"Error reading expression data: {e}")
    return expression_data

# Step 6: Prepare final dataset
def prepare_final_data(snp_counts, exon_lengths, expression_data):
    print("\nPreparing final dataset...")
    genes, densities, expressions, snp_vals, exon_vals = [], [], [], [], []

    for gene_id in snp_counts:
        if gene_id in exon_lengths and gene_id in expression_data:
            length = exon_lengths[gene_id]
            if length > 0:
                count = snp_counts[gene_id]
                density = count / length

                genes.append(gene_id)
                densities.append(density)
                expressions.append(expression_data[gene_id])
                snp_vals.append(count)
                exon_vals.append(length)

    print(f"Final dataset prepared with {len(genes)} genes.")
    return pd.DataFrame({
        'GeneID': genes,
        'SNP_Count': snp_vals,
        'Exon_Length': exon_vals,
        'SNP_Density': densities,
        'Expression': expressions
    })


# Step 6.5: Save final dataset to CSV
def save_results_to_csv(df, filename="snp_density_expression.csv"):
    df.to_csv(filename, index=False)
    print(f"\nResults saved to: {filename}")

# Step 7: Plot and Correlation
def plot_and_correlation(densities, expressions):
    print("\nPerforming correlation analysis and plotting...")
    plt.figure(figsize=(10, 6))
    plt.scatter(expressions, densities, alpha=0.5)
    plt.title("SNP Density vs Gene Expression (Chromosome 2L)")
    plt.xlabel("Gene Expression (Avg.)")
    plt.ylabel("SNP Density in Exons")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("snp_vs_expression_plot_2L.png", dpi=300)
    plt.close()
    corr, pval = pearsonr(expressions, densities)
    print("\nPearson Correlation Results:")
    print(f"Correlation Coefficient (r): {corr:.4f}")
    print(f"P-value: {pval:.4e}")

# Main function
def main():
    gff_file = "drosophila_melanogaster.gff"
    vcf_file = "drosophila_snps.vcf"
    expression_file = "expression.tsv"

    exons = get_exons_from_gff(gff_file)
    snps = get_snp_positions(vcf_file)
    snp_counts = map_snps_to_exons(exons, snps)
    exon_lengths = calculate_exon_lengths(exons)
    expression_data = read_expression_data(expression_file)

    final_df = prepare_final_data(snp_counts, exon_lengths, expression_data)
    save_results_to_csv(final_df)
    plot_and_correlation(final_df['SNP_Density'], final_df['Expression'])

    print("\nAnalysis complete.")

if __name__ == "__main__":
    main()
