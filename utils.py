import pandas as pd
import re

columns_to_transform = ["City", "Item Name"]


def load_data():
    try:
        df = pd.read_excel("data/transformed_dummy_dataset.xlsx")
    except FileNotFoundError:
        print(f"Transformed data not found, starting new operation")
        df = pd.read_excel('data/dummy_dataset.xlsx', sheet_name='Database')

        for column in df.columns:
            if column in columns_to_transform:
                df[column] = transform_data(df[column])

        df.to_excel("data/transformed_dummy_dataset.xlsx", index=False)

    return df


def transform_data(data):
    if isinstance(data, str):
        data = re.sub(r'\s+', ' ', data.lower())
        return data
    # data = data.astype(str)
    data = [entry.lower() for entry in data]
    data = [re.sub(r'\s+', ' ', entry) for entry in data]
    return data
