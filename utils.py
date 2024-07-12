import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

will_transform = ["City", "Channel", "Category", "Segment", "Manufacturer", "Brand", "Item Name"]


def find_closest_item_cosine(target, items):
    vectorizer = TfidfVectorizer().fit_transform([target] + items)
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:])

    closest_idx = cosine_similarities.argmax()
    closest_item = items[closest_idx]

    return closest_item


def load_data():
    try:
        df = pd.read_excel("data/transformed_dummy_dataset.xlsx")
    except FileNotFoundError:
        print(f"Transformed data not found, starting new operation")
        df = pd.read_excel('data/dummy_dataset.xlsx', sheet_name='Database')

        for column in df.columns:
            if column in will_transform:
                df[column] = transform_data(df[column])

        df.to_excel("data/transformed_dummy_dataset.xlsx", index=False)

    return df


def transform_data(data):
    if isinstance(data, str):
        data = data.lower()
        return data
    data = data.astype(str)
    data = [entry.lower() for entry in data]
    data = [re.sub(r'\s+', ' ', entry) for entry in data]
    return data
