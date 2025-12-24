import pandas as pd
import os

def load_spotify_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    high_pop_path = os.path.join(project_root, 'data', 'high_popularity_spotify_data.csv')
    low_pop_path = os.path.join(project_root, 'data', 'low_popularity_spotify_data.csv')

    high_pop = pd.read_csv(high_pop_path)
    low_pop = pd.read_csv(low_pop_path)
    
    return high_pop, low_pop

