
import streamlit as st
import pandas as pd
import pickle

# Load model and vectorizer
@st.cache_resource
def load_model_and_vectorizer():
    with open('nb_model.pkl', 'rb') as f:
        nb_model = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    return nb_model, vectorizer

nb_model, vectorizer = load_model_and_vectorizer()

st.title("🔗 URL Product Classifier")
st.write("Upload a CSV file with a column named **'ind_feature'** to classify whether each URL points to a product or not.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if 'ind_feature' not in df.columns:
        st.error("❌ The uploaded file must contain a column named 'ind_feature'.")
    else:
        st.success("✅ File uploaded successfully!")
        

        # Preprocess the 'ind_feature' column
        df['ind_feature'] = df['ind_feature'].str.lower()
        df['ind_feature'] = df['ind_feature'].str.replace(r'^https?:\/\/(www\.)?', '', regex=True)
        df['ind_feature'] = df['ind_feature'].str.replace(r'\.in|\.com', '', regex=True)
        df['ind_feature'] = df['ind_feature'].str.replace(r'[-/]', ' ', regex=True)
        df.drop_duplicates(subset='ind_feature', keep='last', ignore_index=True, inplace=True)
        df.dropna(inplace=True)

        st.write("Sample input:")
        st.dataframe(df.head())



        
        # Transform the 'ind_feature' column using the vectorizer
        X_new = vectorizer.transform(df['ind_feature'])
        # Predict using the model(🔍 Classifying URLs...)
        df['prediction'] = nb_model.predict(X_new)
        print(df['prediction'])
        df['prediction'] = df['prediction'].apply(lambda x: 'product' if x == 1 else 'not product')
        st.write("🔍 Predictions:")
        st.dataframe(df)


        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Predictions as CSV",
            data=csv,
            file_name='predicted_urls.csv',
            mime='text/csv',
        )

        
