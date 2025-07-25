# import evironment variables
from config import TMDB_API_KEY, BASE_URL

# import necessary libraries
import requests
import time

def fetch_movie_data(movie_ids):
    all_movie_data = []
    for movie_id in movie_ids:
        endpoint = f"{BASE_URL}{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits,genres"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            movie_data = response.json()
            if 'id' in movie_data and movie_data['id'] == movie_id:
                all_movie_data.append(movie_data)
        except requests.exceptions.RequestException as http_err:
            print(f"HTTP error occurred for movie ID {movie_id}: {http_err}")
            if response.status_code == 404:
                print(f"Movie ID {movie_id} not found.")
            elif response.status_code == 429:
                print("Rate limit exceeded. Please try again later.")
                time.sleep(5)
    return all_movie_data