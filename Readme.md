EXECUTION INSTRUCTIONS:
1.download the entire folder
2.run originalGame.py for game with user controls (use left and right arrow buttons on keyboard to control the car)
3.run main.py to run the RL agent


# Traffic RIder
> Traffic Rider is an arcade game developed using pygame package of Python. In this game, player make its way through the traffic on highway. Score increase as player overtakes a vehicle successfully.If player crash with another vehicle then game will over. With increase in score,level increases and so the speed of player's car.

## Controls for user:
1. Press left arrow and right arrow key to move left and right respectively.
2. Press upper arrow key to accelerate and lower arrow key to apply break

## Reinforcement Learning Implementation:
    The agent learns the best actions (move left/right/stay) at each state of the game. Positive reward is given to the agent if it passes the obstacles and penalty is given for crashes. The RL is implemented using Q-table.
