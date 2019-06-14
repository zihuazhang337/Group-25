
---
layout: default
title:  Final Report
---


## Video

[![](MHF.jpg)](https://www.youtube.com/watch?v=4P6WUhySQ3o "Monster HUnter")


## Project Summary


## Approach





## Evaluation
### Quantitative evaluation
We use the monster total damage for the quantitative evaluation. The goal of our project is let the agent learns how to kill the monster efficiently, so if the agent does learn the policy of killing the monster, it will try to damage the monster as much as possible. Therefore, the damage for each trial is a good parameter to estimate how good the agent performs. 

![](/status_result/Damage_Barroth.png){:height="35%" width="35%"}
![](/status_result/Damage_Tigrex.png){:height="35%" width="35%"}

When agent combat with Barroth. With only a few trains, it learns how to kill the monster. Then when it deals with Tigrex, which is another monster and harder to fight, the result is worse. However, after some overlayers, the agent begins to learn how to fight. The above graph has shown that the average damage of the last three trials are better than the first three trials, indicating that the agent does learn how to fight with the monster by Q-learning.

### Qualitative evaluation	
For qualitative evaluation, we use the final score of each trial. The final score is the cumulated reward that the agent gets in a trial. It shows how well the agent can kill the monster. The final score will be decreased if the agent is hit by the monster or it takes too long to kill the monster. It will ensure that the agent really knows the best way to handle the monster, like dodging monster’s attack.

![](/status_result/Final_score_Barroth.png){:height="35%" width="35%"}
![](/status_result/Final_score_Tigrex.png){:height="35%" width="35%"}

The above two graphs are very similar. Comparing the first few trials and the last few one, the score does improve, but it does not seem like it finds the best way to fight. The score is fluctuating.





## Remaining Goals and Challenges
First, our agent knows how to kill the monster, but can’t avoid damage from the monster and it takes a long time to kill the monster, so we want to let it learn a way to maximize the final score. Secondly, in this prototype, we only use the Q-learning, so we may try other methods in the next few weeks, like gradient policy. At last, we will change our states, since they are quite simple, so in many different circumstances; they may be represented by the same state. Also, we want to add more features. Currently, we only have two features to represent the circumstance, which is hard for the agent to predict the next action of the monster precisely. We will not change the hard coding part since we want the agent to always face the monster and attack when it is close to the monster. Learning those skills waste a lot of time, so hard coding this part is better, and it does improve the final score. Our ultimate goal is let the agent know how to kill the monster without getting damage and with least amount of time, which means the agents need to predict monster’s next action and choose the best action to do. Therefore, locating the monster and sequence of actions that make the agent get close to it are essential.

    
    
## Resources Used
Reference code: 

UCI CS175 2019 spring assignment2

Reference article: 

https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-0-q-learning-with-tables-and-neural-networks-d195264329d0

https://medium.com/@m.alzantot/deep-reinforcement-learning-demysitifed-episode-2-policy-iteration-value-iteration-and-q-978f9e89ddaa

