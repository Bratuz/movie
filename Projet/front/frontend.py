import streamlit as st
import requests

# Configuration des URL de l'API
API_BASE_URL = "https://movie-reco5-b4owfwjgaq-oa.a.run.app"

# Fonctions d'appel API
def call_autocomplete_api(query):
    response = requests.get(f"{API_BASE_URL}/autocomplete?query={query}")
    return response.json()

def add_to_favorites(user_id, movie_id):
    response = requests.post(f"{API_BASE_URL}/add_favorite", json={"user_id": user_id, "movie_id": movie_id})
    return response.status_code == 200

def load_favorites(user_id):
    response = requests.get(f"{API_BASE_URL}/get_favorites?user_id={user_id}")
    return response.json() if response.status_code == 200 else None

def get_recommendations(user_id):
    response = requests.post(f"{API_BASE_URL}/recommendations", json={"user_id": user_id})
    return response.json() if response.status_code == 200 else []

# Interface utilisateur Streamlit
def main():
    # Réinitialiser les favoris à chaque nouvelle session
    if "first_run" not in st.session_state:
        st.session_state.favorites = []
        st.session_state.first_run = True

    st.title('Movie Recommendation App')

    # Text input field for movie search
    query = st.text_input('Enter a movie title:', '')

    # Autocomplete suggestions
    if query:
        st.write('Autocomplete Suggestions:')
        suggestions = call_autocomplete_api(query)
        for suggestion in suggestions:
            # Styliser le titre du film
            st.markdown(f'<h3 style="color:blue;">{suggestion}</h3>', unsafe_allow_html=True)

            # Add button to add movie to favorites
            if st.button(f'Add "{suggestion}" to Favorites'):
                if add_to_favorites("123", suggestion):
                    st.session_state.favorites.append(suggestion)
                    st.success(f'"{suggestion}" added to favorites!')
                else:
                    st.error(f'Failed to add "{suggestion}" to favorites.')

    # Button to load favorites
    if st.button('Load Favorites'):
        if st.session_state.favorites:
            st.header('Favorites')
            for favorite in st.session_state.favorites:
                st.write(favorite)
        else:
            st.error('No favorites saved.')

    # Button to load recommendations
    if st.button('Get Recommendations'):
        recommendations = get_recommendations("123")
        if recommendations:
            st.header('Recommendations')
            for recommendation in recommendations:
                # Styliser le titre du film
                st.markdown(f'<h3 style="color:green;">{recommendation}</h3>', unsafe_allow_html=True)
                
                # Display movie poster if available
                poster_path = recommendation.get("poster_path")
                if poster_path:
                    st.image(poster_path, caption=recommendation["movie_title"])
                else:
                    st.write("No poster available.")
        else:
            st.error('Failed to fetch recommendations.')

if __name__ == "__main__":
    main()
