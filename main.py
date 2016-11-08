from os import path, listdir
from src.game.Game import Game
import csv

ROOT_DIR = path.dirname(path.abspath(__file__))
DATASET = path.join(ROOT_DIR, 'data/json')
TABLES = path.join(ROOT_DIR, 'data/tables')
action_table = path.join(TABLES, 'actions.csv')

if __name__ == "__main__":
    with open(action_table, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow( ('Game Date', 'Teams', 'Event Index', 'Quarter', 'Start Time', 'Duration') )

    files = listdir(DATASET)
    for seed, file in enumerate(files):
        #Ignore hidden files
        if file.startswith('.'):
          continue
        #debug
        if "CHA.at.GSW" in file:
            dir = path.join(DATASET, file)
            game = Game(dir)
            game.read_json(seed)
            game.actions_to_csv(action_table, file[:-5])

        # dir = path.join(DATASET, file)
        # game = Game(dir)
        # game.read_json(seed)
        #Write results to csv, remove 'json'
        # game.actions_to_csv(action_table, file[:-5])

  # visualize
  # game.start()