---
layout: default
title: Proposal
---

## Summary of the Project
    For our project, we are going to build an agent that is able to learn how to kill a monster in the mod, monster hunter frontier. Our goal is to let the agent make the right action when facing a monster and kill the monster in the least amount of time. The agent will ultimately learn what to do, such as attack the dragon or step away to avoid damage from the monster since the monster is also moving and can do damage to the agent. We will set up an 21 x 21 battleground for an agent and a monster to fight each other. The agent will be given a melee weapon, long sword, and monster will move based on its setting on the mod. The input semantics in our case would be the monster, containing the health point of that monster and the movements of that monster. The sample out semantics would be a sequence of actions that can lead the agent to kill the monster efficiently. The agent will take the information of the monster’s health point from input to produce a better output.

## AI/ML Algorithms
    We are planning to use Q-learning with neural network for improving our agent.


## Evaluation Plan
# Quantitative evaluation
    One of the numerical metrics would be the time spending of an agent to kill the monster. The baselines of our project consist of the following components: the loss of the agent’s health point and the loss of the monster’s health point. We want our agent to learn to attack the monster and ultimately kill the monster. Our design is to let the agent study from its actions so that each action that leads to the loss of the monster’s health point would be considered a successful action, then the agent would do that same with higher probability. We also want the agent to learn to avoid damage, so actions that would lead to the state that the agent loses his health point would be reduced.

# Qualitative evaluation	
    In general cases, the examples that our idea will definitely work on is that the agent spends some period to kill the monster or be killed by the monster. The expected outputs are a long sequence of actions. Error analysis and introspection: suppose we have a plot with typical Cartesian graph, and the x-axis indicates each trial, and the y-axis would the score of each trial. We would use this plot to keep track of our agent’s behavior. If the plot performs an increasing trend line, then the agent is doing the right thing; otherwise, we may need to make changes on the AI algorithm. The total score of each run will be calculated based on the loss agent’s health point, the monster’s health point and time spending on each run. The best case will be  the agent can kill the monster with the least amount of time and least cost of the agent’s health pint
