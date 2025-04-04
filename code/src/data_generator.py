# -*- coding: utf-8 -*-
"""data_generator.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QPeL6hLhE358quZIOB1Jk8eu1m_ZjKwg
"""

import pandas as pd
import numpy as np

# Generate sample regulatory report data
np.random.seed(42)
num_records = 500

data = {
    "Customer_ID": np.random.randint(1000, 2000, num_records),
    "Account_Balance": np.random.uniform(0, 10000, num_records),
    "Transaction_Amount": np.random.uniform(-500, 5000, num_records),  # Some negative values for testing
    "Reported_Amount": np.random.uniform(-500, 5000, num_records),  # Some negative values for testing
    "Currency": np.random.choice(["USD", "EUR", "INR", "GBP"], num_records),
    "Country": np.random.choice(["USA", "Germany", "India", "UK"], num_records),
    "Transaction_Date": pd.date_range(start="2023-01-01", periods=num_records, freq="D").strftime('%Y-%m-%d'),
    "Risk_Score": np.random.uniform(0, 1, num_records),
}

# Create DataFrame
df = pd.DataFrame(data)

# Save sample data to CSV
df.to_csv("data/regulatory_report_no_nulls.csv", index=False)

# Display sample data
print(df.head())