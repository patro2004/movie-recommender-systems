import streamlit as st
import pickle
import pandas as pd
import requests

# Set the page configuration
st.set_page_config(
    page_title="Movie Recommender System",  # The title of the web page
    page_icon="🌟",  # The favicon of the web page. It can be an emoji or a URL to an image.
    layout="wide",  # The layout of the web page ('centered' or 'wide')
    initial_sidebar_state="auto",  # The initial state of the sidebar ('auto', 'expanded', 'collapsed')
    menu_items={  # Custom menu items in the top-right hamburger menu
        'Get Help': 'https://www.example.com/help',
        'Report a bug': 'https://www.example.com/bug',
        'About': """
            ### CineMatch: Your Personalised Movie Guide

            In an era where digital content consumption is at its peak, the ability to efficiently navigate vast libraries of movies is crucial for enhancing user experience. This proposed project aims to deliver precise movie recommendations.

            **Made by Sneha Patro**

            For more information, visit [Streamlit](https://streamlit.io/).
        """
    }
)

# Function to fetch movie details including poster
def fetch_movie_details(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=5e98d851ac4efc723a03ef80a80cd3e1&language=en-US')
    data = response.json()
    poster_path = 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    details = {
        "poster": poster_path,
        "genre": ", ".join([genre['name'] for genre in data['genres']]),
        "release_date": data['release_date'],
        "overview": data['overview'],
        "rating": data['vote_average']
    }
    return details


# Function to get recommendations
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_details = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster and details from API
        recommended_movies_details.append(fetch_movie_details(movie_id))
    return recommended_movies, recommended_movies_details


# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Custom CSS for dark mode
custom_css = """
    <style>
    body {
        background-color: #1f2937; /* Dark mode background color */
        color: #ffffff; /* Dark mode text color */
    }
    .st-bq {
        color: #ffffff; /* Adjusting blockquote text color for dark mode */
    }
    .css-18e3th9 {
        background-color: rgba(31, 41, 55, 0.75); /* Dark background with opacity for content */
        border-radius: 10px;
        padding: 10px;
    }
    </style>
"""

# Streamlit UI
st.markdown(custom_css, unsafe_allow_html=True)
st.title('🎬 Movie Recommender System')

# Sidebar for movie selection
st.sidebar.header("Select a Movie")
selected_movie_name = st.sidebar.selectbox("Choose a movie you like", movies['title'].values, index=0)

# Display selected movie name in the sidebar text box
st.sidebar.text_input("Selected Movie:", selected_movie_name)

# Display balloons when a movie is selected
if selected_movie_name:
    st.balloons()

if st.sidebar.button("Recommend"):
    if selected_movie_name in movies['title'].values:
        names, details = recommend(selected_movie_name)

        st.header(f"Movies recommended for '{selected_movie_name}'")
        cols = st.columns(5)

        for i in range(len(names)):
            with cols[i]:
                st.image(details[i]["poster"], use_column_width=True)
                st.markdown(f"**{names[i]}**")
                st.write(f"Genre: {details[i]['genre']}")
                st.write(f"Release Date: {details[i]['release_date']}")
                st.write(f"Rating: {details[i]['rating']}")
                st.write(details[i]['overview'], unsafe_allow_html=True)
    else:
        st.error("Movie not found! Please enter a valid movie name.")

# Feedback form
st.sidebar.header("Feedback")
feedback_text = st.sidebar.text_area("Share your feedback", "")

if st.sidebar.button("Submit Feedback"):
    # Here you can handle the feedback submission, e.g., store it in a database or send it to an API
    st.sidebar.success("Thank you for your feedback!")

# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #1f2937; /* Dark mode background color */
        color: #ffffff; /* Dark mode text color */
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>Thank you for using our Movie Recommender System! 🎥</p>
    </div>
    """,
    unsafe_allow_html=True
)
