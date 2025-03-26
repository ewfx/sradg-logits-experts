import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample regulatory report data
np.random.seed(42)
num_records = 500

# Define high-risk countries and accepted jurisdictions
high_risk_countries = ["India", "Russia", "North Korea"]
accepted_jurisdictions = ["USA", "Germany", "India", "UK", "Canada", "Australia"]
valid_currencies = ["USD", "EUR", "INR", "GBP", "AUD", "CAD"]

# Generate DataFrame
data = {
    "Customer_ID": np.random.randint(1000, 2000, num_records),
    "Account_Balance": np.random.uniform(-1000, 10000, num_records),
    "Transaction_Amount": np.random.uniform(10, 15000, num_records),
    "Currency": np.random.choice(valid_currencies, num_records),
    "Country": np.random.choice(accepted_jurisdictions + high_risk_countries, num_records),
    "Transaction_Date": [datetime.today() - timedelta(days=np.random.randint(0, 730)) for _ in range(num_records)],
    "OD_Flag": np.random.choice(["Yes", "No"], num_records),
    "Risk_Score": np.random.uniform(0, 1, num_records),
}

# Ensure Reported_Amount follows cross-currency conversion rule
data["Reported_Amount"] = [
    amt if np.random.rand() > 0.1 else amt * np.random.uniform(0.99, 1.01)
    for amt in data["Transaction_Amount"]
]

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert Transaction_Date to string format
df["Transaction_Date"] = df["Transaction_Date"].dt.strftime('%Y-%m-%d')

# Save to CSV
df.to_csv("data/regulatory_report_no_nulls.csv", index=False)

# Display sample data
print(df.head())
