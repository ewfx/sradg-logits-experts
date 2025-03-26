import streamlit as st
import os
import PyPDF2
import openai
# import google.generativeai as genai
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import numpy as np
# from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt



openai.api_key = os.environ.get("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF document."""
    text = ""
    with open(pdf_path, "rb") as file_stream:
        pdf_file = PyPDF2.PdfReader(file_stream)
        for page in pdf_file.pages:
            text += page.extract_text() + "\n"
    return text

def generate_profiling_rules(reporting_guidelines):
    """
    Uses a Generative AI model to create data profiling rules based on regulatory guidelines.
    """
    prompt = f"""
    Given the following regulatory reporting guidelines:
    {reporting_guidelines}
    
    Generate structured data profiling rules to ensure compliance. Include rules for:
    - Data completeness (e.g., required fields, missing values)
    - Data consistency (e.g., currency format, value ranges)
    - Allowed value ranges (e.g., non-negative values for transactions)
    - Formatting (e.g., date formats should follow YYYY-MM-DD)
    - Compliance checks (e.g., all monetary values must be in USD)
    
    Provide the rules in a structured JSON format.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a regulatory compliance expert."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

def suggest_remediation(issue_description):
    """
    Uses LLM to suggest remediation actions for data quality issues.
    """
    prompt = f"""
    Given the following data quality issue in a regulatory report:
    {issue_description}

    Suggest an appropriate remediation action to ensure compliance.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a regulatory compliance expert."},
                  {"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

def risk_scoring(df):
    """Performs anomaly detection and clustering-based risk scoring"""
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df.select_dtypes(include=[np.number]))  # Normalize numeric data

    # Isolation Forest for anomaly detection
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    anomaly_labels = iso_forest.fit_predict(df_scaled)

    # K-Means for clustering risk groups
    kmeans = KMeans(n_clusters=3, random_state=42)
    risk_groups = kmeans.fit_predict(df_scaled)

    df["Anomaly"] = anomaly_labels
    df["Risk_Score"] = risk_groups  # Assign risk levels

    return df


with st.spinner('Waiting for file to be uploaded...'):
    pass

st.title("Upload a file to generate profiling rules")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully")

    pdf_text = extract_text_from_pdf(file_path)

    # Example usage
    data = pd.read_csv("data/regulatory_report_no_nulls.csv")

    profiling_rules = generate_profiling_rules(pdf_text)
    remediation_actions = suggest_remediation(profiling_rules)

    scored_data = risk_scoring(data)

    st.title("WF88 Data Profiler")
    st.header("Profiling Rules")
    st.write(profiling_rules)
    st.header("Remediation Actions")
    st.write(remediation_actions)
    st.header("Scored Data")
    st.write(scored_data)

    # Create anomaly dot graph
    anomaly_points = scored_data[scored_data["Anomaly"] == -1]
    normal_points = scored_data[scored_data["Anomaly"] == 1]

    fig, ax = plt.subplots()
    ax.scatter(normal_points.iloc[:, 0], normal_points.iloc[:, 1], label="Normal")
    ax.scatter(anomaly_points.iloc[:, 0], anomaly_points.iloc[:, 1], label="Anomaly")
    ax.legend()

    st.pyplot(fig)
