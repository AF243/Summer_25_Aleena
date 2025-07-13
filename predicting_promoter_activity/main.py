from prepare_data import prepare_promoter_data
from extract_features import promoter_feature_analysis
from train_model import train_model
from compare_models import compare_models
def main():
    promoters=prepare_promoter_data("D:\machine_learning\gene_promoter_prediction\PromoterSet.tsv") 
    features= promoter_feature_analysis("cleaned_promoters.csv")
    # comparison=compare_models("promoter_features.csv")
    model=train_model("promoter_features.csv")


if __name__ == "__main__":
    main()