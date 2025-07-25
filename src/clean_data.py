import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from fetch_data import fetch_movie_data
from utils.helpers import extract_collection, extract_names, extract_director_and_cast

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
all_movies_df['belongs_to_collection'] = all_movies_df['belongs_to_collection'].apply(extract_collection)

json_columns_to_process = {
    'genres': 'genres',
    'production_countries': 'production_countries',
    'production_companies': 'production_companies',
    'spoken_languages': 'spoken_languages'
}

for col_name, new_col_name in json_columns_to_process.items():
    if col_name in all_movies_df.columns:
        all_movies_df[new_col_name] = all_movies_df[col_name].apply(extract_names)


# Extract director, cast, cast_size, crew_size from 'credits'
if 'credits' in all_movies_df.columns:
    all_movies_df[['director', 'cast', 'cast_size', 'crew_size']] = all_movies_df['credits'].apply(
        lambda x: pd.Series(extract_director_and_cast(x))
    )
    all_movies_df = all_movies_df.drop(columns=['credits'], errors='ignore')

# check the data types of the columns
print(all_movies_df.info())

# Convert columns to proper types
numeric_cols = ['budget', 'popularity', 'revenue']

for col in numeric_cols:
    if col in all_movies_df.columns:
        all_movies_df[col] = pd.to_numeric(all_movies_df[col], errors='coerce')

# convert 'release_date' to datetime
all_movies_df['release_date'] = pd.to_datetime(all_movies_df['release_date'], errors='coerce')

# handle missing values
# check for missing values
all_movies_df.isna().sum()

# heatmap to visualize missing values
plt.figure(figsize=(10, 6))
sns.heatmap(all_movies_df.isna(), cbar=False, cmap='viridis')
plt.title('Missing Values Heatmap')
plt.show()

# belongs_to_collection column contains 2 NaN values. budget, revenue, and runtime columns do not have 0 values.so no replacement is needed.

# convert 'budget' and 'revenue' to million USD
all_movies_df['budget_musd'] = all_movies_df['budget'] / 1e6
all_movies_df['revenue_musd'] = all_movies_df['revenue'] / 1e6

# using value_counts to check the distribution of 'vote_count'
if 'vote_count' in all_movies_df.columns and 'vote_average' in all_movies_df.columns:
    all_movies_df.loc[all_movies_df['vote_count'] == 0, 'vote_average'] = np.nan
all_movies_df['vote_count'].value_counts()
# votes_count do not contain 0 values, so no replacement is needed.

#  Remove duplicates and drop rows with unknown 'id' or 'title'
# count the number of duplicates
duplicates_count = all_movies_df.duplicated().sum()
all_movies_df.drop_duplicates(inplace=True)
all_movies_df.dropna(subset=['id', 'title'], inplace=True)

# Keep rows with at least 10 non-NaNs
all_movies_df = all_movies_df[all_movies_df.notna().sum(axis=1) >= 10]


# filter to include only 'Released' movies
if 'status' in all_movies_df.columns:
    all_movies_df = all_movies_df[all_movies_df['status'] == 'Released']
    all_movies_df.drop(columns=['status'], inplace=True, errors='ignore')

# reorder columns
columns_order = [
    'id', 'title', 'tagline', 'release_date', 'genres', 'belongs_to_collection',
    'original_language', 'budget_musd', 'revenue_musd', 'production_companies',
    'production_countries', 'vote_count', 'vote_average', 'popularity', 'runtime',
    'overview', 'spoken_languages', 'poster_path', 'cast', 'cast_size', 'director', 'crew_size']

all_movies_df = all_movies_df[[col for col in columns_order if col in all_movies_df.columns]]

# reset index
all_movies_df.reset_index(drop=True, inplace=True)

# save the cleaned DataFrame to a CSV file
all_movies_df.to_csv('cleaned_movie_data.csv', index=False)

print("\n--- Data Cleaning and Preprocessing Complete ---")
print(f"Final DataFrame shape: {all_movies_df.shape}")
print("\nFinal DataFrame info:")
all_movies_df.info()
print("\nFirst 5 rows of the cleaned DataFrame:")
print(all_movies_df.head())