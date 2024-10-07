from train import train_and_save_model
from predict_and_offer import predict_and_assign_offers

if __name__ == "__main__":
    # File paths
    train_data_path = './data/train_set.parquet'
    model_save_path = './churn_model.pkl'
    submission_data_path = './data/submission_set.parquet'
    offers_data_path = './data/offers_monthly.parquet'
    output_path = './submission_output.xlsx'  # Change to .xlsx format

    # Train the model
    train_and_save_model(train_data_path, model_save_path)
    
    # Predict and assign offers
    predict_and_assign_offers(submission_data_path, model_save_path, offers_data_path, output_path)
