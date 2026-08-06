import pandas as pd

def load_data(filepath):
    print("Loading dataset...")

    df = pd.read_csv(filepath)

    print("Dataset loaded successfully!")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    df = df.drop_duplicates()
    df = df.dropna()

    return df