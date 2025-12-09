import pandas as pd
import matplotlib.pyplot as plt
import os

fn = 'nfl_games_2024.csv'
if not os.path.exists(fn):
    fn = 'nfl_games_sample.csv'
    print('Using sample data:', fn)

df = pd.read_csv(fn)
# Keep completed games - ensure Winner/tie exists
df = df[df['Winner/tie'].notna()]

# Count wins per team
wins = df['Winner/tie'].value_counts().rename_axis('team').reset_index(name='wins')

# Count losses per team by counting appearances as loser
losses = df['Loser/tie'].value_counts().rename_axis('team').reset_index(name='losses')

# Combine
summary = pd.merge(wins, losses, on='team', how='outer').fillna(0)
summary['wins'] = summary['wins'].astype(int)
summary['losses'] = summary['losses'].astype(int)
summary['games'] = summary['wins'] + summary['losses']
summary['win_pct'] = (summary['wins'] / summary['games']).fillna(0).round(3)

summary = summary.sort_values('win_pct', ascending=False)
print(summary)

# Plot top teams (if sample small, all teams shown)
plt.figure(figsize=(8,4))
summary.set_index('team')['win_pct'].plot(kind='bar')
plt.title('NFL Team Win Percentage (sample)')
plt.ylabel('Win %')
plt.tight_layout()
plt.savefig('nfl_win_pct.png')
print('Saved nfl_win_pct.png')
