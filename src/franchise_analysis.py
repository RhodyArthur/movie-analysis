from clean_data import all_movies_df

# This script analyzes the performance of franchise movies versus standalone movies.
franchise_df = all_movies_df.copy()
franchise_df['is_franchise'] = franchise_df['belongs_to_collection'].notna()

franchise_summary = franchise_df.groupby('is_franchise').agg({
    'revenue_musd': 'mean',
    'roi': 'median',
    'budget_musd': 'mean',
    'popularity': 'mean',
    'vote_average': 'mean'
}).rename(index={True: 'Franchise', False: 'Standalone'})

print("\n Franchise vs. Standalone Movie Performance")
print(franchise_summary)

# most successful franchise movies
franchise_stats = franchise_df.groupby('belongs_to_collection').agg({
    'title': 'count',
    'budget_musd': ['sum', 'mean'],
    'revenue_musd': ['sum', 'mean'],
    'vote_average': 'mean'
}).sort_values(('revenue_musd', 'sum'), ascending=False)

print("\n Most Succesful Franchise")
print(franchise_stats)

# Most successful directors
director_stats = franchise_df.groupby('director').agg({
    'title': 'count',
    'budget_musd': ['sum', 'mean'],
    'revenue_musd': ['sum', 'mean'],
    'vote_average': 'mean'
}).sort_values(('revenue_musd', 'sum'), ascending=False)

# Rename columns for clarity
director_stats.columns = ['Total Movies', 'Total Budget', 'Avg Budget', 'Total Revenue', 'Avg Revenue', 'Avg Rating']

print("\n🎬 Most Successful Directors")
print(director_stats.head())