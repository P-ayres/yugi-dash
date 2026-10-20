import pandas as pd
import streamlit as st
import kagglehub as kh

import kagglehub

# Download latest version
path = kagglehub.dataset_download("hammadus/yugioh-full-card-database-index-august-1st-2025")

print("Path to dataset files:", path)

# Load the dataset into a pandas DataFrame
df = pd.read_csv(f"{path}/yugioh-ccd-2025SEP12-163128.csv")

print("Dataset loaded successfully.")
print(df.head())