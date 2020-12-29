#!/usr/bin/env python
#Importing libraries
import gym
import gym_csv
import random

import numpy as np 
import time

# X points down (rows)(v), Y points right (columns)(>), Z would point outwards.
LEFT = 0  # < Decrease Y (column)
DOWN = 1  # v Increase X (row)
RIGHT = 2 # > Increase Y (column)
UP = 3    # ^ Decrease X (row)

#Period in ms for renderization
SIM_PERIOD_MS = 250.0

#Loading environment
env = gym.make('csv-v0')
state = env.reset()
print("state: "+str(state))
env.render()
time.sleep(0.5)

#done trigger when goal is reached, state saves where is the "robot" within the map, contador counts the number of steps in the current state
done = False
state = 0
contador = 0

#function movement to renderize the movement of the "robot". It determines when the "robot" changes its state too.
def movement(move, steps, state, contador):
	new_state, reward, done, _ = env.step(move)
	env.render()
	print("new_state: "+str(new_state)+", reward: "+str(reward)+", done: "+str(done))
	time.sleep(SIM_PERIOD_MS/1000.0)
	contador = contador + 1
	#print('contador' +str(contador))
	if contador == steps:
		state = state + 1
		contador = 0
	#print('state' +str(state))
	return state, contador

#While the "robot" has not reached the goal, it moves through the map in the different states (DOWN, RIGHT, UP,etc) until goal is found.
while not done:
	if state == 0:
		state, contador = movement(DOWN, 6, state, contador)
	if state == 1:
		state, contador = movement(RIGHT, 3, state, contador)
	if state == 2:
		state, contador = movement(UP, 6, state, contador)
	if state == 3:
		state, contador = movement(RIGHT, 6, state, contador)
	if state == 4:
		state, contador = movement(DOWN, 6, state, contador)		
	if state == 5:
		state, contador = movement(RIGHT, 3, state, contador)
	if state == 6:
		state, contador = movement(UP, 6, state, contador)
	if state == 7:
		done = True
		print("GOAL")