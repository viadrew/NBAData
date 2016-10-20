from os import path, listdir
from src.game.Game import Game


ROOT_DIR = path.dirname(path.abspath(__file__))
DATASET = path.join(ROOT_DIR, 'data/json')
if __name__ == "__main__":
  files = listdir(DATASET)

  for file in files:
    if file.startswith('.'):
      continue
    dir = path.join(DATASET, file)
    print(dir)
    game = Game(dir)
    game.read_json()

  # visualize
  # game.start()