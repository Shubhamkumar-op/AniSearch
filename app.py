import streamlit as st
import pandas as pd
import pickle

# Load the data
animes = pd.read_csv("anime.csv")
animes = animes.reset_index()

# Add "Search anime" as the default option
options = ["Search anime"] + list(animes['Name'].values)

@st.cache_resource
def recommend(anime):
    if anime == "Search anime":
        return [], [], []

    similarity = pickle.load(open('models/model.pkl', 'rb'))
    try:
        index = animes[animes["Name"] == anime]["index"].values[0]
    except IndexError:
        st.error(f"Anime titled '{anime}' not found in the dataset.")
        return [], [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_anime_names = []
    recommended_anime_summery = []
    recommended_anime_tags = []
    for i in distances[1:6]:
        recommended_anime_names.append(animes.iloc[i[0]].Name)
        recommended_anime_summery.append(animes.iloc[i[0]].Synopsis)
        recommended_anime_tags.append(animes.iloc[i[0]].Tags)

    return recommended_anime_names, recommended_anime_summery, recommended_anime_tags

def main():
    st.set_page_config(page_title="Anime Recommender", layout="wide")

    st.markdown("""
    <style>
    body {
        background-color: #2c2c2c; 
        color: #f5f5f5; 
    }
    .stSelectbox div {
        color: #888;
    }
    .stSelectbox div div:first-child {
        color: #ff6f61; 
        cursor: pointer;
    }
    .stSelectbox div div:last-child {
        color: #f5f5f5;
    }
    .stButton button {
        background-color: #ff6f61; 
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #e55d50;
    }
    .recommendation-card {
        padding: 1rem;
        border: 2px solid #ff6f61;
        border-radius: 10px;
        background: #3c3c3c;
        margin-bottom: 1rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Anime Recommender")

    st.markdown("""
    <div style=" padding: 1rem; border-radius: 10px; margin-bottom: 1rem; color: #fff;">
        <h3>Hello my friends, My name is Killa Tava and I am here to help you all</h3>
        <h3>Just enter the name of the anime and I will recommend you similar types of anime based</h3>
    </div>
    """, unsafe_allow_html=True)

    selected_anime = st.selectbox('Which anime did you like?', options)

    if selected_anime == "Search anime":
        st.info("Please select an anime from the list.")
    elif selected_anime and st.button('Recommend'):
        with st.spinner('Finding recommendations...'):
            recommendations, summery, tags = recommend(selected_anime)
            st.success('Recommendations ready!')

            for i in range(len(recommendations)):
                st.markdown(f"""
                <div class="recommendation-card">
                    <h3 style="color: #ff6f61;">{i + 1}. {recommendations[i]}</h3>
                    <p><strong>Summary:</strong> {summery[i]}</p>
                    <p><strong>Tags:</strong> {tags[i]}</p>
                </div>
                """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
