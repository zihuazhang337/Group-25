"""
hunter try to learn the best way to kill the monsterw

"""
from __future__ import division
import numpy as np

import MalmoPython
import os
import random
import sys
import time
import json
import random
import math
import errno
import mh_helper as submission
from collections import defaultdict, deque
from timeit import default_timer as timer

monster = 'barroth'
#monster = 'tigrex'
monster_life = 1
hunter_life = 1
m_x = 20.5
m_z = 30
min_epsilon = 0.05

def GetMissionXML(summary):
    ''' Build an XML mission string that uses the RewardForCollectingItem mission handler.'''

    return '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>''' + summary + '''</Summary>
        </About>

        <ModSettings>
            <MsPerTick>100</MsPerTick>
        </ModSettings>

        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>6000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
                <AllowSpawning>false</AllowSpawning>
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,220*1,4*3,2,80;3;biome_1" />
                <DrawingDecorator>
                    <DrawCuboid x1="-3" y1="226" z1="-3" x2="43" y2="236" z2="43" type="stone" />
                    <DrawCuboid x1="0" y1="236" z1="0" x2="40" y2="240" z2="40" type="glass" />
                    <DrawCuboid x1="1" y1="226" z1="1" x2="39" y2="239" z2="39" type="air" />
                </DrawingDecorator>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>hunter</Name>
            <AgentStart>
                <Placement x="20.5" y="227.0" z="30" yaw="90"/>
                <Inventory>
                    <InventoryItem slot="8" type="stone"/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
            <DiscreteMovementCommands>
                <ModifierList type="deny-list">
                    <command>attack</command>
                </ModifierList>
            </DiscreteMovementCommands>
            <ContinuousMovementCommands>
                <ModifierList type="allow-list">
                    <command>attack</command>
                </ModifierList>
            </ContinuousMovementCommands>
            <AbsoluteMovementCommands/>
                <ChatCommands/>
                <MissionQuitCommands/>
                <InventoryCommands/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="60" yrange="20" zrange="60"/>
                </ObservationFromNearbyEntities>
                <ObservationFromFullInventory/>
                <AgentQuitFromCollectingItem>
                    <Item type="rabbit_stew" description="Supper's Up!!"/>
                </AgentQuitFromCollectingItem>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''


class hunter(object):
    def __init__(self, alpha=0.3, gamma=1, n=10):
        """Constructing an RL agent.

        Args
            alpha:  <float>  learning rate      (default = 0.3)
            gamma:  <float>  value decay rate   (default = 1)
            n:      <int>    number of back steps to update (default = 1)
        """
        self.epsilon = 0.3  # chance of taking a random action instead of the best
        self.q_table = {}
        self.n, self.alpha, self.gamma = n, alpha, gamma
        self.t = 0

    @staticmethod
    def get_obj_locations(agent_host):
        """Queries for the object's location in the world.
            
            As a side effect it also returns Odie's location.
            """
        nearyby_obs = {}
        while True:
            world_state = agent_host.getWorldState()
            if world_state.number_of_observations_since_last_state > 0:
                msg = world_state.observations[-1].text
                ob = json.loads(msg)
                for ent in  ob['entities']:
                    name = ent['name']
                    if name == 'hunter' or name == monster:
                        nearyby_obs[name] = (ent['yaw'], ent['x'], ent['z'], ent['life'], ent['y'])
                
                return nearyby_obs


    def teleport(self, agent_host, teleport_x, teleport_z, yaw):
        """Directly teleport to a specific position."""
        tp_command = "tp " + str(teleport_x)+ " 226 " + str(teleport_z)
        agent_host.sendCommand(tp_command)
        good_frame = False
        start = timer()
        while not good_frame:
            world_state = agent_host.getWorldState()
            if not world_state.is_mission_running:
                print("Mission ended prematurely - error.")
                exit(1)
            if not good_frame and world_state.number_of_video_frames_since_last_state > 0:
                frame_x = world_state.video_frames[-1].xPos
                frame_z = world_state.video_frames[-1].zPos
                if math.fabs(frame_x - teleport_x) < 0.001 and math.fabs(frame_z - teleport_z) < 0.001:
                    good_frame = True
                    end_frame = timer()

#monster init pos: 20.5 30
    def battlesetup(self, agent_host, teleport_x = 24, teleport_z = 30):
        """Set up the battle"""
        tp_command = "tp " + str(teleport_x)+ " 226 " + str(teleport_z)

        agent_host.sendCommand("chat /give @p diamond_sword 1 0 {ench:[{id:16,lvl:1000},{id:19,lvl:50}]}")
        agent_host.sendCommand("chat /replaceitem entity @p slot.armor.chest minecraft:diamond_chestplate 1 0 {ench:[{id:0,lvl:9000},{id:4,lvl:9000}]}")
        agent_host.sendCommand("chat /effect @p health_boost 99999 30") # max health
        agent_host.sendCommand("chat /effect @p 6 1 40") # healing 40
        agent_host.sendCommand("chat /effect @p 17 4 230") # hungry 4 230
#changing the summon need to also change the monster in global variable
        agent_host.sendCommand("chat /summon MHFC:Barroth")
#        agent_host.sendCommand("chat /summon MHFC:Tigrex")
#        agent_host.sendCommand("chat /summon sheep")
        time.sleep(0.2)

        agent_host.sendCommand(tp_command)

        good_frame = False
        start = timer()
        while not good_frame:
            world_state = agent_host.getWorldState()
            if not world_state.is_mission_running:
                print("Mission ended prematurely - error.")
                exit(1)
            if not good_frame and world_state.number_of_video_frames_since_last_state > 0:
                frame_x = world_state.video_frames[-1].xPos
                frame_z = world_state.video_frames[-1].zPos
                if math.fabs(frame_x - teleport_x) < 0.001 and math.fabs(frame_z - teleport_z) < 0.001:
                    good_frame = True
                    end_frame = timer()

    def front(self, sou, des):
        x = 1.0
        z = 1.0
        deltax = des[1] - sou[1]
        deltaz = des[2] - sou[2]
        if deltaz < 0:
            z = -1.0
        if deltax < 0:
            x = -1.0
        
        # need to move toward the target
        if abs(deltax) > 4 or abs(deltaz) > 4:
            if deltax == 0:
                if des[2] > sou[2]:
                    return (0,0.0,z)
                else:
                    return (180,0.0,z)

            elif deltaz == 0:
                if des[1] > sou[1]:
                    return (270,x,0.0)
                else:
                    return (90,x,0.0)
        
            deltaprop = abs(deltax / deltaz)
            if deltaprop > 2.0:
                return (-57*math.atan2(deltax,deltaz),x,0.0)
            elif deltaprop < 0.5:
                return (-57*math.atan2(deltax,deltaz),0.0,z)
            else:
                return (-57*math.atan2(deltax,deltaz),x,z)
        else:
            return (sou[0],0,0)
    
    def get_state(self, hunter, monster):
        distance = math.sqrt((hunter[1] - monster[1]) **2 + (hunter[2] - monster[2])**2)
#        if distance < 5:
#            d = "A"
#        elif distance < 10:
#            d = "B"
#        elif distance < 15:
#            d = "C"
#        elif distance < 20:
#            d = "D"
#        else:
#            d = "E"
        if distance < 5:
            d = 0
        else:
            d = distance // 1
        facing = 0
        if hunter[0]*monster[0] < 0 and (180 - 45 < (abs(hunter[0]) % 180) + (abs(monster[0]) % 180) < 180 + 45):
            facing  = 1
        speed = math.sqrt((m_x-monster[1])**2 + (m_z-monster[2])**2)
        speed = speed // 3
        s = [d, facing,speed]
        return tuple(s)

    
    def check_boundary(self, location, monster, next_move):
        if 1 < location[1] + next_move[1] < 39 and 1 < location[2] + next_move[2] < 39:
            return True
    
    def get_action(self, hunter, monster):
        #front
        f = self.front(hunter, monster)
        a = {}
        if self.check_boundary(hunter, monster, f):
            a["F"] = f
        #back
        if f[1] == 0 and f[2] == 0:
            if hunter[0] > 0:
                f = (f[0], -1, f[2])
            else:
                f = (f[0], 1, f[2])
        b = (f[0], -1*f[1], -1*f[2])
        if self.check_boundary(hunter, monster, b):
            a["B"] = b
        #left
        l = (f[0], -1*f[1], -1*f[2])
        if f[1] == 0 and f[2] == 1:
            l = (f[0], -1, 0)
        if f[1] == -1 and f[2] == 1:
            l = (f[0], -1, -1)
        if f[1] == -1 and f[2] == 0:
            l = (f[0], 0, -1)
        if f[1] == -1 and f[2] == -1:
            l = (f[0], 1, -1)
        if f[1] == 0 and f[2] == -1:
            l = (f[0], 1, 0)
        if f[1] == 1 and f[2] == -1:
            l = (f[0], 1, 1)
        if f[1] == 1 and f[2] == 0:
            l = (f[0], 0, 1)
        if f[1] == 1 and f[2] == 1:
            l = (f[0], -1, 1)
        if self.check_boundary(hunter, monster, l):
            a["L"] = l
        #right
        r = (l[0], -1*l[1], -1*l[2])
        if self.check_boundary(hunter, monster, r):
            a["R"] = r
        if not a:
            a["F"] = (f[0],0,0)
        return a

    def movement(self, agent_host, x, z, yaw):
        agent_host.sendCommand("tp "+str(x)+" 226 "+str(z))
        agent_host.sendCommand("setYaw "+str(yaw))


    def update_q_table(self, tau, S, A, R, T):
        """Performs relevant updates for state tau.
            
            Args
            tau: <int>  state index to update
            S:   <dequqe>   states queue
            A:   <dequqe>   actions queue
            R:   <dequqe>   rewards queue
            T:   <int>      terminating state index
            """
        curr_s, curr_a, curr_r = S.popleft(), A.popleft(), R.popleft()
        G = sum([self.gamma ** i * R[i] for i in range(len(S))])
        if tau + self.n < T:
            G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]
        
        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)


    def choose_action(self, curr_state, possible_actions, eps):
        """Chooses an action according to eps-greedy policy. """
        if curr_state not in self.q_table:
            self.q_table[curr_state] = {}
        for action in possible_actions:
            if action not in self.q_table[curr_state]:
                self.q_table[curr_state][action] = 0
        return submission.choose_action(curr_state, possible_actions, eps, self.q_table)


    def act(self, agent_host, current_a, current_obj):
        reward = -3
        self.movement(agent_host, current_a[1]+current_obj['hunter'][1], current_a[2]+current_obj['hunter'][2], current_a[0])
        global hunter_life
        global monster_life
# wait for updating the new status
        time.sleep(0.20)
        new_obj = self.get_obj_locations(agent_host)
        
# get hit: -loss * 1
# die: -1000
        if 'hunter' not in new_obj:
            reward -= 1000
        elif new_obj['hunter'][3] < hunter_life:
            reward -= (hunter_life - new_obj['hunter'][3]) * 1
            hunter_life = new_obj['hunter'][3]
        
# hit the monster: +loss * 2
# kill the monster: + 1500
        if monster not in new_obj:
            reward += 1500
        elif new_obj[monster][3] < monster_life:
            reward += (monster_life - new_obj[monster][3]) * 2
            monster_life = new_obj[monster][3]
        return reward
    

    def run(self, agent_host):
        '''
            S: state queue
            A: action queue
            R: reward queue
            obj['hunter] = ["yaw","x","z","life","y"]
        '''
        score = 0
        damage = 0
        S, A, R = deque(), deque(), deque()
        done_update = False
        while not done_update:
            # change the epsilon
            if self.t > 500 and self.t % 20 == 0:
                self.epsilon -= 0.01
            self.t += 1
            
            obj = self.get_obj_locations(agent_host)
            monster_hp =obj[monster][3]
            s0 = self.get_state(obj['hunter'],obj[monster])
            a = self.get_action(obj['hunter'],obj[monster])
            possible_actions = list(a.keys())
            a0 = self.choose_action(s0, possible_actions, self.epsilon)
            S.append(s0)
            A.append(a0)
            R.append(0)
            
            global hunter_life
            global monster_life
            monster_life = obj[monster][3]
            hunter_life = obj['hunter'][3]
            run_t = 0
            T = sys.maxsize
            for t in range(sys.maxsize):
                if run_t >= 600:
                    break
                else:
                    run_t += 1
                obj = self.get_obj_locations(agent_host)
                if not 225 < obj['hunter'][4] < 227:
                    if obj['hunter'][3] > 0:
                        for i in range(50):
                            obj = self.get_obj_locations(agent_host)
                            if 225 < obj['hunter'][4] < 227:
                                break
                            else:
                                time.sleep(0.1)
                if t < T:
# do the last action and get the reward
                    agent_host.sendCommand("attack 1")
                    time.sleep(0.20)
                    current_r = self.act(agent_host, a[A[-1]],obj)
                    score += current_r
                    R.append(current_r)
# get the next action
#                   obj = self.get_obj_locations(agent_host)
                    if ('hunter' not in obj) or (monster not in obj) or obj[monster][3] < 1 or obj['hunter'][3] < 1:
                        T = t + 1
                        damage = monster_hp - obj[monster][3]
                        S.append((None,None))
                    else:
                        s = self.get_state(obj['hunter'],obj[monster])
                        S.append(s)
                        a = self.get_action(obj['hunter'],obj[monster])
                        possible_actions = list(a.keys())
                        next_a = self.choose_action(s, possible_actions, self.epsilon)
# for learning
                        A.append(next_a)
# test for kill the monster
#                        if "F" in possible_actions:
#                            A.append("F")
#                        else:
#                            A.append(possible_actions[0])

                tau = t - self.n + 1
                if tau >= 0:
                    self.update_q_table(tau, S, A, R, T)
                if tau == T - 1:
                    while len(S) > 1:
                        tau = tau + 1
                        self.update_q_table(tau, S, A, R, T)
                    done_update = True
                    break

        return (score, damage)

if __name__ == '__main__':
    random.seed(time.clock())
    print('Starting...', flush=True)

    expected_reward = 3390
    my_client_pool = MalmoPython.ClientPool()
    my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))

    agent_host = MalmoPython.AgentHost()
    try:
        agent_host.parse(sys.argv)
    except RuntimeError as e:
        print('ERROR:', e)
        print(agent_host.getUsage())
        exit(1)
    if agent_host.receivedArgument("help"):
        print(agent_host.getUsage())
        exit(0)
    sco = open("score.txt","w+")
    dam = open("damage.txt","w+")
    tim = open("time.txt","w+")
# how many battle the agent need to run
    battle_reps = 100
    n=1
    hunter = hunter(n=n)
    print("n=",n)
    for iRepeat in range(battle_reps):
        print("Round "+str(iRepeat+1))
        my_mission = MalmoPython.MissionSpec(GetMissionXML("Round #" + str(iRepeat)), True)
        my_mission_record = MalmoPython.MissionRecordSpec()  # Records nothing by default
        my_mission.requestVideo(800, 500)
        my_mission.setViewpoint(0)
        max_retries = 3

        for retry in range(max_retries):
            try:
                # Attempt to start the mission:
                agent_host.startMission(my_mission, my_client_pool, my_mission_record, 0, "hunter")
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission", e)
                    print("Is the game running?")
                    exit(1)
                else:
                    time.sleep(2)

        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()
        
        hunter.battlesetup(agent_host)
        time.sleep(0.5)
        start_time = time.time()
        eva = hunter.run(agent_host)
        run_time = (time.time() - start_time) // 1
        print("Score: "+str(eva[0])+". Damage: "+str(eva[1])+". Time: "+str(run_time))
        sco.write(str(eva[0])+"\n")
        dam.write(str(eva[1])+"\n")
        tim.write(str(run_time)+"\n")
        time.sleep(0.5)
        agent_host.sendCommand("quit")
