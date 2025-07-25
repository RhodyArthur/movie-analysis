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