from analysis.tiers.scrape import scrape
from sklearn.cluster import KMeans
import json
import math
import matplotlib.pyplot as plt
import pandas as pd

# Elbow Method for determining k
def elbow_method(cluster_data):
    inertias = []
    for k in range(2, 100):
        clstr = KMeans(n_clusters=k, random_state=42)
        clstr.fit(cluster_data)
        inertias.append(clstr.inertia_)

    plt.figure(0)
    plt.plot(inertias)
    plt.savefig('./elbow_method.png')

# Converts clusters into dictionary compatible for visualization
def clusters_to_json(player_clusters):
    players_grouped = player_clusters.groupby('tier')
    tiers_dict = players_grouped.mean().sum(axis=1).rank(ascending=False) - 1
    tiers = list(range(1,len(tiers_dict) + 1))
    print(list(players_grouped))
    players_dict = list(map(lambda x:{'tier':tiers[int(tiers_dict[int(x[0])])], 'players':list(map(
        lambda x: x , x[1]['name']))}, players_grouped))
    return json.dumps(players_dict)

def cluster(year):
    # Load data
    df = pd.read_csv('./../../data/bballref/players_advanced_' + year + '.csv')

    # NBA statistical minimums is usually 58 games (>70%)
    data = df[ df['G'] >= (0.7 * df['G'].max())]
    df = data
    names = data['Player']

    # Remove irrelevant data for clustering (player, position, age, team)
    data = data.drop(data.columns[[0,1,2,3]], axis=1)

    # Apply z-scores to columns; normalize data
    for col in list(data.columns):
        a = data[col]
        data[col] = (a-a.mean())/a.std()

    # remove nans
    data = data.fillna(method='ffill')

    # Rule of thumb k (k=sqrt(n/2))
    num_clusters = int(math.sqrt(len(data)/2))

    clstr = KMeans(n_clusters=num_clusters)
    clstr.fit(data)
    df['tier'] = clstr.labels_
    df['name'] = names
    return clusters_to_json(df)

if __name__ == '__main__':
    season = '2017'

    scrape(season)
    result = cluster(season)

    print(result)