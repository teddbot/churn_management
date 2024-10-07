import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_and_save_model(training_data_path, model_save_path):
    # Load the training data from Parquet
    data = pd.read_parquet(training_data_path)
    
    # Define features and target variable
    features = [col for col in data.columns if col not in ['SUBSCRIBER', 'CHURN_STATUS', 'ARPU']]
    X = data[features]
    y = data['CHURN_STATUS']
    
    # Split data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = RandomForestClassifier(random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    # Save the trained model
    joblib.dump(model, model_save_path)
    print(f"Model trained and saved to {model_save_path}")
