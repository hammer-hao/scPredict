# %%
import pickle
from tqdm import tqdm
from scpredict.settings import *
import pandas as pd
from scpredict.parsing import ZBulkParser

parser = ZBulkParser()
parsed_replays = parser.parse_folder('replays_raw')
with open('replays_processed/zephyrus/parsed.pt', 'wb') as f:
    pickle.dump(parsed_replays, f)

# %%
path_to_parsed_replays = 'replays_processed/zephyrus/parsed.pt'
with open(path_to_parsed_replays, 'rb') as f:
    parsed_replays = pickle.load(f)

# %%
import warnings

for matchup in matchups:

    print(f'Aggregating matchup data for {matchup}')

    unique_features = set()
    for entry in tqdm(parsed_replays[matchup]):
        unique_features.update(entry.keys())
    # Convert the set to a list
    unique_features = list(unique_features)

    df = pd.DataFrame(columns=unique_features)

    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)

        for entry in tqdm(parsed_replays[matchup]):
            # Create a dictionary with all features, setting missing ones to None
            row = {feature: entry.get(feature, None) for feature in unique_features}
            # Append the row to the DataFrame
            df = df.append(row, ignore_index=True)

    df.to_csv(f'replays_processed/zephyrus/{matchup}.csv', index=False)




