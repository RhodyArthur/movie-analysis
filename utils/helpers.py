import numpy as np
import pandas as pd

def extract_collection(collection):
    return collection['name'] if isinstance(collection, dict) and 'name' in collection else np.nan

def extract_names(lst, key='name'):
    return '| '.join([item[key] for item in lst if key in item]) if isinstance(lst, list) else np.nan

def extract_director_and_cast(credits, num_cast=5):
    """
    Extracts director(s) and top N cast members from the 'credits' JSON.
    Returns a tuple: (director_names_str, cast_names_str, cast_size, crew_size).
    """
    director_names = []
    cast_names = []
    cast_size = 0
    crew_size = 0

    if pd.isna(credits):
        return np.nan, np.nan, 0, 0
    try:
        if 'crew' in credits:
            crew_size = len(credits['crew'])
            director_names = [member['name'] for member in credits['crew'] if member.get('job') == 'Director']
        
        if 'cast' in credits:
            cast_size = len(credits['cast'])
            cast_names = [member['name'] for member in credits['cast'][:num_cast]]
        
        director_names_str = '| '.join(director_names) if director_names else np.nan
        cast_names_str = '| '.join(cast_names) if cast_names else np.nan
        
        return director_names_str, cast_names_str, cast_size, crew_size
    except (TypeError, KeyError):
        return np.nan, np.nan, 0, 0
    