# Flappy Bird Q-Learning

An implementation of flappy bird using pygame that can be played by a person or an agent using Q-Learning.

## Play it Yourself

Run with `--mode 0` or `-m 0` and use space to jump. This is the default mode.

## Train from Scratch

Run with `--mode 1` or `-m 1` and watch as the agent learns. A preview is shown to see how well the agent is doing and the average score is printed regularly.

## Load and Train from Existing Model

Run with `--mode 2` or `-m 2` and provide an epoch number to load using `--epoch {number}` or `-e {number}`. If the model exists it will be loaded from the file and continue training.

## Load and Run from Existing Model

Run with `--mode 3` or `-m 3` and provide an epoch number to load using `--epoch {number}` or `-e {number}`. If the model exists it will be loaded from the file and will play one game.

## Additional Options

- `--model-dir {directory}`|`-d {directory}`: the directory to store the models in