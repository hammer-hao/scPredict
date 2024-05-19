# SCPredict: StarCraft II Replay win rate analysis and visualization

[SCPredict](https://hammer-hao.github.io/scPredict/) is an online analysis tool for StarCraft II replay files. 

## Model and Training Data Used

SCPredict is trained on the official posted WCS/ESL Masters replay files from 2020 to May 2024. A total of 4445 replays were used to train the models. 

[Zephyrus Replay Parser](https://github.com/ZephyrBlu/zephyrus-sc2-parser) was used for 1v1 replay parsing. One model for each in-game matchup was trained seperately, as the features used in the model is unique to matchups. Logistic regression models were fitted using scikit-learn's Logisticregression() module with L2(Lasso) penalties. 

## Model Performance

The classification report for the Protoss vs. Terran model:

|            | precision | recall | f1-score | support |
|------------|------------|--------|----------|---------|
| 0.0        | 0.68       | 0.87   | 0.77     | 10601   |
| 1.0        | 0.75       | 0.49   | 0.60     | 8412    |
| **accuracy** |            |        | 0.70     | 19013   |
| **macro avg** | 0.72       | 0.68   | 0.68     | 19013   |
| **weighted avg** | 0.71       | 0.70   | 0.69     | 19013   |

Note that each game start with the highest entropy possible, which gets reduced as in-game events unfold.