from models.baseline import MLPClassifier, concatenate_rows_single_last_column
import sc2reader
import torch

mlp = MLPClassifier()
mlp.load_state_dict(torch.load('saved_models/baseline.pt'))
mlp.eval()

@torch.no_grad
def mlp_predict(path_to_replay):
    game_data = []
    replay = sc2reader.load_replay(path_to_replay)
    for event in replay.events:
        if event.name == "PlayerStatsEvent":
            stats = torch.tensor(list(event.stats.values()))
            time = torch.tensor(event.second).unsqueeze(0)
            x = torch.concat((stats, time))
            game_data.append(x)
    game_data_tensor = torch.stack(game_data)
    game_data_tensor = concatenate_rows_single_last_column(game_data_tensor)
    print(f'predicted win rate: {mlp(game_data_tensor.float())}')
    return(mlp(game_data_tensor.float()).tolist())