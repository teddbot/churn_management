import pandas as pd
import joblib
import os
import random
import yagmail

# Set up Email Credentials (replace with your email and app password)
EMAIL_ADDRESS = 'cyborggenai@gmail.com'
EMAIL_PASSWORD = 'bvby kwbx zfwq sedu'

# Generate a default personalized message (since OpenAI integration is removed)
def generate_default_message(subscriber_id, offer_name):
    return f"Dear subscriber {subscriber_id}, we have an exclusive offer just for you: {offer_name}! Stay connected with us for more amazing benefits."

# Simulate offer acceptance (mock function)
def simulate_offer_acceptance():
    return random.choice([True, False])  # Randomly simulate offer acceptance

# Measure the impact of interventions
def measure_impact(data):
    total_offers = len(data)
    accepted_offers = data['OFFER_ACCEPTED'].sum()
    retention_rate = accepted_offers / total_offers * 100 if total_offers > 0 else 0
    average_arpu_after = data.loc[data['OFFER_ACCEPTED'], 'ARPU'].mean()
    
    metrics = {
        'Total Offers': total_offers,
        'Accepted Offers': accepted_offers,
        'Retention Rate (%)': retention_rate,
        'Average ARPU After Intervention': average_arpu_after
    }
    
    return metrics

# Send an email report
def send_email_report(output_path, metrics):
    try:
        yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD)
        subject = "Churn Management Report"
        
        # Properly format the content as a string
        contents = [
            f"Here is the churn management report:\n\n"
            f"Total Offers: {metrics['Total Offers']}\n"
            f"Accepted Offers: {metrics['Accepted Offers']}\n"
            f"Retention Rate: {metrics['Retention Rate (%)']:.2f}%\n"
            f"Average ARPU After Intervention: {metrics['Average ARPU After Intervention']}\n"
        ]
        
        # Ensure the output_path is passed as a string for the attachment
        yag.send(
            to='tnzioka@safaricom.co.ke',
            subject=subject,
            contents=contents,
            attachments=[str(output_path)]  # Convert output_path to a string if it isn't already
        )
        
        print("Email report sent successfully!")
    except Exception as e:
        print(f"Failed to send email report: {e}")

def predict_and_assign_offers(submission_data_path, model_path, offers_data_path, output_path):
    # Load the model
    model = joblib.load(model_path)

    # Load the submission data and offers data
    submission_data = pd.read_parquet(submission_data_path)
    offers_data = pd.read_parquet(offers_data_path)

    # Define feature columns for prediction
    features = [col for col in submission_data.columns if col not in ['SUBSCRIBER', 'ARPU']]
    X_submission = submission_data[features]

    # Predict churn status
    churn_predictions = model.predict(X_submission)
    submission_data['PREDICTED_CHURN_STATUS'] = churn_predictions

    # Assign offers and generate default personalized messages
    offers = []
    messages = []
    offer_accepted = []
    for _, row in submission_data.iterrows():
        if row['PREDICTED_CHURN_STATUS'] == 1:  # Churn predicted
            arpu = row['ARPU']
            max_offer_value = 0.1 * arpu  # Maximum offer is 10% of ARPU

            # Find an appropriate offer from the offers data using the 'PRICE' column
            possible_offers = offers_data[offers_data['PRICE'] <= max_offer_value]
            if not possible_offers.empty:
                selected_offer = possible_offers.iloc[0]['PRODUCT_NAME']
            else:
                selected_offer = "Default_Small_Offer"

            # Generate a default personalized message
            message = generate_default_message(row['SUBSCRIBER'], selected_offer)

            # Simulate offer acceptance
            accepted = simulate_offer_acceptance()
        else:
            selected_offer = "No Offer"
            message = "Thank you for being a valued customer!"
            accepted = False

        offers.append(selected_offer)
        messages.append(message)
        offer_accepted.append(accepted)

    # Add offers, messages, and acceptance to the DataFrame
    submission_data['PRODUCT_NAME'] = offers
    submission_data['PERSONALIZED_MESSAGE'] = messages
    submission_data['OFFER_ACCEPTED'] = offer_accepted

    # Measure the impact of interventions
    metrics = measure_impact(submission_data)

    # Save the output to an Excel file
    submission_data[['SUBSCRIBER', 'PREDICTED_CHURN_STATUS', 'PRODUCT_NAME', 'PERSONALIZED_MESSAGE', 'OFFER_ACCEPTED']].to_excel(output_path, index=False)
    print(f"Predictions, offers, and messages saved to {output_path}")

    # Send an email report
    send_email_report(output_path, metrics)
