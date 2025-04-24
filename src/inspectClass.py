import pandas as pd

df = pd.read_csv("/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/class/labels.csv")
print(df['transcript'].unique().shape)