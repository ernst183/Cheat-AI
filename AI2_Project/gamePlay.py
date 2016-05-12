import Player as P
import PlayerType as PT
from BullshitGame import *
import random
import sys


player_list = []

# make test players	
thisPlayer = P.Player("Terminator", PT.Dolphin(1,0.1,0.98,0.005,"Terminator"))
player_list.append(thisPlayer)
thisPlayer = P.Player("Patrick Swayze", PT.Dolphin(1,0.1,0.98,0.005,"Patrick Swayze"))
player_list.append(thisPlayer)
thisPlayer = P.Player("Zeus", PT.Dolphin(1,0.1,0.98,0.005,"Zeus"))
player_list.append(thisPlayer)	
thisPlayer = P.Player("Ghandi", PT.Dolphin(1,0.1,0.98,0.005,"Ghandi"))
player_list.append(thisPlayer)

# make human
thisPlayer = P.Player("MereMortal", PT.Human())
player_list.append(thisPlayer)

# make sure we play in random order
random.shuffle(player_list)
game = Bullshit_Game(player_list)
game.verbose = True
for player in player_list:
	player.verbose = True
game.deal_game()
numDecks = 1
#Initialize tracker of player moves and evidence for AI agents to use:
for player in player_list:
	tracker = PlayerTracker(player.name, len(player.hand.cards))
	tracker.probability_given_card = tracker.num_cards/52.0*numDecks
	game.players_tracker[player.name] = tracker
	

winner = game.play_game()

