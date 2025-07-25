# import evironment variables
from config import TMDB_API_KEY, BASE_URL

# import necessary libraries
import requests
import time

# list of movie ids to fetch
movie_ids = [0, 299534, 19995, 140607, 299536, 597, 135397,
             420818, 24428, 168259, 99861, 284054, 12445,
             181808, 330457, 351286, 109445, 321612, 260513]

# fetch movie data

all_movie_data = []

for movie_id in movie_ids:
    endpoint = endpoint = f"{BASE_URL}{movie_id}?api_key={TMDB_API_KEY}"

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