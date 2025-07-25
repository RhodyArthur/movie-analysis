import pandas as pd
from fetch_data import fetch_movie_data

# list of movie ids to fetch
movie_ids = [0, 299534, 19995, 140607, 299536, 597, 135397,
             420818, 24428, 168259, 99861, 284054, 12445,
             181808, 330457, 351286, 109445, 321612, 260513]


# convert data to a DataFrame
all_movies_df = pd.DataFrame(fetch_movie_data(movie_ids))

# drop irrelevant columns
columns_to_drop = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
all_movies_df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

# extract nested fields
def extract_collection(collection):
    return collection['name'] if isinstance(collection, dict) and 'name' in collection else None

def extract_names(lst, key='name'):
    return '| '.join([item[key] for item in lst if key in item]) if isinstance(lst, list) else None

all_movies_df['belongs_to_collection'] = all_movies_df['belongs_to_collection'].apply(extract_collection)
all_movies_df['genres'] = all_movies_df['genres'].apply(lambda x: extract_names(x))
all_movies_df['spoken_languages'] = all_movies_df['spoken_languages'].apply(lambda x: extract_names(x))
all_movies_df['production_countries'] = all_movies_df['production_countries'].apply(lambda x: extract_names(x))
all_movies_df['production_companies'] = all_movies_df['production_companies'].apply(lambda x: extract_names(x))