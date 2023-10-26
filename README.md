# sc2Predict

## Overview

Real-time winrate prediction from starcraft 2 matches. The classification model is trained using 3464 replays released officially by ESL from the 2022/23 ESL Pro Tour. Included models are:

- Logistic Regression
- Gradient Boosting
- Random Forests
- MLP Classification

## How to use

### Setting up virtual env

1. Clone the repository to your local machine
2. Set up the virtual env and install the dependencies:
```
$python3 -m venv env
$source env/bin/activate
(env)$pip install -r requirements.txt
```
