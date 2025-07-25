from clean_data import all_movies_df

def rank_movies(df, metric, top=True, n=10, min_votes=0, min_budget=0, label=None):
    filtered = df.copy()
    if min_votes > 0:
        filtered = filtered[filtered['vote_count'] >= min_votes]
    if min_budget > 0:
        filtered = filtered[filtered['budget_musd'] >= min_budget]
    ranked = filtered.sort_values(by=metric, ascending=not top)
    result = ranked[['title', metric, 'release_date']].head(n)
    if label:
        print(f"\n📌 {label}")
    return result

rank_movies(all_movies_df, 'revenue_musd', top=True, label='Top 10 by Revenue')
rank_movies(all_movies_df, 'budget_musd', top=True, label='Top 10 by Budget')
rank_movies(all_movies_df, 'profit_musd', top=True, label='Top 10 by Profit')
rank_movies(all_movies_df, 'profit_musd', top=False, label='Bottom 10 by Profit')
rank_movies(all_movies_df, 'roi', top=True, min_budget=10, label='Top 10 by ROI (Budget ≥ 10M)')
rank_movies(all_movies_df, 'roi', top=False, min_budget=10, label='Bottom 10 by ROI (Budget ≥ 10M)')
rank_movies(all_movies_df, 'vote_count', top=True, label='Top 10 by Vote Count')
rank_movies(all_movies_df, 'vote_average', top=True, min_votes=10, label='Top 10 by Rating (≥10 votes)')
rank_movies(all_movies_df, 'vote_average', top=False, min_votes=10, label='Bottom 10 by Rating (≥10 votes)')
rank_movies(all_movies_df, 'popularity', top=True, label='Top 10 by Popularity')

# Search 1: Best-rated Science Fiction Action movies starring Bruce Willis
sci_fi_action_bruce = all_movies_df[
    all_movies_df['genres'].str.contains("Science Fiction") &
    all_movies_df['genres'].str.contains("Action") &
    all_movies_df['cast'].apply(lambda x: "Bruce Willis" in x)
].sort_values(by="vote_average", ascending=False)

print("\n🔍 Best-rated Sci-Fi Action Movies starring Bruce Willis")
print(sci_fi_action_bruce[['title', 'vote_average', 'genres']])

# Search 2: Movies starring Uma Thurman directed by Quentin Tarantino
uma_tarantino = all_movies_df[
    all_movies_df['cast'].apply(lambda x: "Uma Thurman" in x) &
    (all_movies_df['director'] == "Quentin Tarantino")
].sort_values(by="runtime", ascending=True)

print("\n🔍 Movies starring Uma Thurman and directed by Quentin Tarantino")
print(uma_tarantino[['title', 'runtime', 'release_date']])