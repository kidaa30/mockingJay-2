__author__ = 'Nathan'

import pygame
import graphics
import random
import map
from action import Action
from tribute import Tribute
from goal import Goal
from mapReader import readMap
from random import randint

class GameEngine(object):
    """
    here we will essentially manage everything and probably handle the controls
    """
    constants = range(1)
    is_looping = False
    tributes = []

    @staticmethod
    def start():
        me = GameEngine

        #create actions (will be overwritten in a minute)
        move_up = Action([], '', 1, 0, (0, -1), 'move_up')
        move_down = Action([], '', 1, 1, (0, 1), 'move_down')
        move_right = Action([], '', 1, 2, (1, 0), 'move_right')
        move_left = Action([], '', 1, 3, (-1, 0), 'move_left')
        hunt = Action([5], ["hunger"], 1, 4,(0, 0), 'hunt')
        fight = Action([5], ["kill"], 1, 5, (0, 0), 'fight')
        scavenge = Action([3], ["getweapon"], 1, 6, (0, 0), 'scavenge')
        craft = Action([4], ["getweapon"], 1, 7, (0, 0), 'craft')
        hide = Action([5], ["hide"], 1, 8, (0, 0), 'hide')
        getwater = Action([5], ["thirst"], 1, 9, (0, 0), 'get_water')
        rest = Action([5], ["rest"], 1, 10, (0, 0), 'rest')
        talkAlly = Action([5], ["ally"], 1, 11, (0, 0), 'talk_ally')

        #create actions (will be overwritten in a minute)
        hunger = Goal("hunger", 2)
        thirst = Goal("thirst", 2)
        goalRest = Goal("rest", 0)
        kill = Goal("kill", 0)
        goalHide = Goal("hide", 0)
        getweapon = Goal("getweapon", 0)
        ally = Goal("ally", 0)

        goals = [hunger, thirst, goalRest, kill, goalHide, getweapon, ally]
        actions = [move_up, move_down, move_right, move_left, hunt, fight, scavenge, craft, hide, getwater, rest, talkAlly]

        #create the goals here
        #not really needed right now

        init_locations = [(x, y) for x in range(50) for y in range(50)]
        #creates all the actions
        for i in range(0, 1):
            location = random.choice(init_locations)
            init_locations.remove(location)
            me.tributes.append(Tribute(goals, actions, *location, district='d12', gender='male'))

        for i in range(0, 1):
            location = random.choice(init_locations)
            init_locations.remove(location)
            me.tributes.append(Tribute(goals, actions, *location, district='d12', gender='female'))

        for i in range(len(me.tributes)):
            initTribute = me.create_goals(me.tributes[i])
            me.tributes[i].goals = initTribute

        me.dims = (50, 50)
        me.gameMap = readMap('maps/field.png')
        me.view = graphics.GameView(*me.dims)
        me.map = map.Map('maps/field.png')
        me.state = me.map.seed_game_state(me.tributes)  # game.GameState()
        me.is_looping = True
        while me.is_looping and GameEngine.loop():
            pass

    @staticmethod
    def stop():
        GameEngine.is_looping = False

    @staticmethod
    def loop():
        """
        What to do on each loop iteration
        @return: None
        """
        me = GameEngine

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        for tribute in me.tributes:
            tribute.act(me.gameMap) #finds bestAction and does it.
            tribute.end_turn()
            death = tribute.checkDead()
            if not death is None:
                print tribute.first_name, " ", tribute.last_name, " death by ", death
                me.tributes.remove(tribute)
        me.view.render(me.state)

        me.state.update()
        return True

    @staticmethod
    def create_actions(tribute):
        #Move action
        move_up = Action([], '', 1, 0, (0, -1), 'move_up')
        move_down = Action([], '', 1, 1, (0, 1), 'move_down')
        move_right = Action([], '', 1, 2, (1, 0), 'move_right')
        move_left = Action([], '', 1, 3, (-1, 0), 'move_left')


        ################ INDEX LIST
        # 0-3 movement
        # 4 hunt
        # 5 fight
        # 6 scavenge
        # 7 craft
        # 8 hide
        # 9 water
        # 10 rest
        # 11 talk

        ############## ACTION ATTRIBUTES
        #1. How much I get back for doing the action in 2. EDIT THIS ONE
        #2. The action (lists, so it can affect more than one thing.)
        #3. Duration
        #4. Index
        #5. Movement Stuff (don't mess wid that)

        #as long as you hunt, you'll get at least 10 food points, maybe more depending on attributes & individual
        hungerStats = (tribute.attributes['endurance']/2)+tribute.attributes['hunting_skill']-(tribute.attributes['size']/5)
        foodEnergy = 10 + randint(0, hungerStats)
        foodRest = (tribute.attributes['stamina'] - 1)/100
        hunt = Action([foodEnergy,foodRest], ["hunger","rest"], 1, 4,(0,0),'hunt')

        #if you fight your "bloodlust" goes down. If you're friendly, killng someone drastically reduces your desire to kill
        #someone else. Unless you have a friendliness of 1
        killStats = (((1/tribute.attributes['bloodlust'])*3)+(tribute.attributes['friendliness']-1))
        if(int(tribute.district[1:]) == 1 or int(tribute.district[1:]) == 2 or int(tribute.district[1:])):
            killStats += 3
        else:
            killStats += 5
        fight = Action([killStats], ["kill"], 1, 5, (0,0),'fight')

        #If they find a weapon, they'll get back 15 "find weapon" points, which will generally cover
        #about 150 of wanting a weapon, and not having one. Same w/ crafting
        scavenge = Action([15], ["getweapon"], 1, 6, (0,0),'scavenge')
        craft = Action([15], ["getweapon"], 1, 7, (0,0),'craft')

        #If you're small and good at hiding, you get more points for it
        #You also recover some rest
        hideStats = ((3/(tribute.attributes['size']+tribute.attributes['strength']))+((tribute.attributes['camouflage_skill']-1)/4))
        hide = Action([hideStats, 3], ["hide", "rest"], 1, 8, (0,0),'hide')

        #As long as you drink, you'll get at least 10 drink points. Maybe more depending on attributes & individual
        thirstStats = (tribute.attributes['endurance'])-(tribute.attributes['size']/5)
        thirstEnergy = 10 + randint(0, thirstStats)
        getwater = Action([thirstEnergy], ["thirst"], 1, 9, (0,0),'get_water')

        #Resting will automatically recover 10 rest points. Maybe more depending on attributes & individual
        restStats = (tribute.attributes['stamina'] * 2)
        restEnergy = 10 + randint(0, restStats)
        rest = Action([restEnergy], ["rest"], 1, 10, (0,0), 'rest')

        #If you're friendly, talking to buddies recovers a bunch of talking-to-buddy points
        #And the smaller, weaker, and more terrible at fighting you are, the more recovery you get for making a buddy
        allyStats = (tribute.attributes['friendliness'] + (1/tribute.attributes['size']) + (1/tribute.attributes['strength']) + (0.5/tribute.attributes['fighting_skill']))
        talkAlly = Action([allyStats], ["ally"], 1, 11, (0,0),'talk_ally')

        newActions = [move_up, move_down, move_right, move_left, hunt, fight, scavenge, craft, hide, getwater, rest, talkAlly]

        tribute.actions = newActions

        return tribute

    @staticmethod
    def create_goals(tribute):
        #Just giving default values for now
        #Will figure out exact values later
        #Starting these at zero and plan to increment every turn
        hunger = Goal("hunger", 2)
        thirst = Goal("thirst", 2)
        rest = Goal("rest", 2)

        #KILL and HIDE are Changing Based on Attributes
        district = int(tribute.district[1:])

        #Is going to need to be changed somehow based on attributes
        kill = Goal("kill", 10-tribute.attributes['friendliness'])
        hide = Goal("hide", 0)

        #Also going to be dependent on the value of certain things
        getweapon = Goal("getweapon", 0)
        ally = Goal("ally", tribute.attributes['friendliness'])
        return [hunger, thirst, rest, kill, hide, getweapon, ally]