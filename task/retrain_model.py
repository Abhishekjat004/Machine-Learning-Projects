# retrain.py
# This file is used to retrain the model with new data.
import streamlit as st
import pandas as pd
import pickle

# Now we have two options for updating the model with new data:
# 1. incremental learning → keep the same vectorizer and partial_fit().
# 2. If you want new vocabulary → store all past data, refit vectorizer, and retrain model from scratch.
# So Now i assume that the new data is kind of similar to the old data, From doing that we can save the time and computationally resource
# so we will go with the first option.


# Load model and vectorizer
@st.cache_resource
def load_model_and_vectorizer():
    with open('nb_model.pkl', 'rb') as f:
        nb_model = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    return nb_model, vectorizer

nb_model, vectorizer = load_model_and_vectorizer()

st.title("🔗 Retrain the model")
st.write("Upload a CSV file with a column named **'ind_feature'** to retrain the model with new data.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if 'ind_feature' not in df.columns:
        st.error("❌ The uploaded file must contain a column named 'ind_feature'.")
    else:
        st.success("✅ File uploaded successfully!")
        # Retrain_models
        st.write("🔄 Update Models with New Data")
        

        # Preprocess the 'ind_feature' column
        df['ind_feature'] = df['ind_feature'].str.lower()
        df['ind_feature'] = df['ind_feature'].str.replace(r'^https?:\/\/(www\.)?', '', regex=True)
        df['ind_feature'] = df['ind_feature'].str.replace(r'\.in|\.com', '', regex=True)
        df['ind_feature'] = df['ind_feature'].str.replace(r'[-/]', ' ', regex=True)
        df.drop_duplicates(subset='ind_feature',keep='last',ignore_index=True,inplace=True)
        df.dropna(inplace=True)
        # Preprocess the 'ind_feature' and 'dep_feature' column
        df['dep_feature'] = df['dep_feature'].str.lower()
        df['dep_feature'] = df['dep_feature'].apply(lambda x: 1 if x == 'product' else 0)   

        st.write("Sample input:")
        st.dataframe(df.head())

        # Transform the 'ind_feature' column using the vectorizer
        X_new = vectorizer.transform(df['ind_feature'])
        classes = nb_model.classes_
        # Update models with new data
        nb_model.partial_fit(X_new, df['dep_feature'], classes=classes)

        # Save updated models
        pickle.dump(nb_model,open("nb_model.pkl",'wb'))
        st.write("Models updated with new data.")

     

        