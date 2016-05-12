import Player as P
import PlayerType as PT
from BullshitGame import *
import random
import sys

DavisWins = 0
dav_num_won_BS = 0
dav_num_lost_BS = 0
MarlWins = 0
mar_num_won_BS = 0
mar_num_lost_BS = 0
SvenWins = 0
sven_num_won_BS = 0
sven_num_lost_BS = 0
JorgeWins = 0
jor_num_won_BS = 0
jor_num_lost_BS = 0
JesusWins = 0
JimWins = 0
TerminatorWins = 0
ter_num_won_BS = 0
ter_num_lost_BS = 0

for x in range(1000):
	player_list = []

	# make test players	
	thisPlayer = P.Player("Davis", PT.Frog(random.uniform(.05,.3)))
	player_list.append(thisPlayer)
	thisPlayer = P.Player("Marl", PT.Frog(random.uniform(.05,.3)))
	player_list.append(thisPlayer)
	thisPlayer = P.Player("Sven", PT.Eel(random.uniform(.05,.3)))
	player_list.append(thisPlayer)	
	thisPlayer = P.Player("Jorge", PT.Eel(random.uniform(.05,.3)))
	player_list.append(thisPlayer)

	# make terminator ai
	thisPlayer = P.Player("Terminator", PT.Dolphin(1,0.1,0.98,0.005,"Terminator"))
	player_list.append(thisPlayer)

	# make sure we play in random order
	random.shuffle(player_list)
	game = Bullshit_Game(player_list)
	if len(sys.argv) > 1:
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
	if winner == "Davis":
		DavisWins += 1
	if winner == "Marl":
		MarlWins += 1
	if winner == "Sven":
		SvenWins += 1
	if winner == "Jorge":
		JorgeWins += 1
	if winner == "Terminator":
		TerminatorWins+=1

	ter_num_won_BS += game.players_tracker["Terminator"].num_won_BS
	ter_num_lost_BS += game.players_tracker["Terminator"].num_lost_BS

	dav_num_won_BS += game.players_tracker["Davis"].num_won_BS
	dav_num_lost_BS += game.players_tracker["Davis"].num_lost_BS

	sven_num_won_BS += game.players_tracker["Sven"].num_won_BS
	sven_num_lost_BS += game.players_tracker["Sven"].num_lost_BS

	mar_num_won_BS += game.players_tracker["Marl"].num_won_BS
	mar_num_lost_BS += game.players_tracker["Marl"].num_lost_BS

	jor_num_won_BS += game.players_tracker["Jorge"].num_won_BS
	jor_num_lost_BS += game.players_tracker["Jorge"].num_lost_BS



print("Terminator statistics for calling BS:")
print("\tWon BS challenges: " + str(ter_num_won_BS))
print("\tLost BS challenges: " + str(ter_num_lost_BS))

print("Davis statistics for calling BS:")
print("\tWon BS challenges: " + str(dav_num_won_BS))
print("\tLost BS challenges: " + str(dav_num_lost_BS))

print("Sven statistics for calling BS:")
print("\tWon BS challenges: " + str(sven_num_won_BS))
print("\tLost BS challenges: " + str(sven_num_lost_BS))

print("Marl statistics for calling BS:")
print("\tWon BS challenges: " + str(mar_num_won_BS))
print("\tLost BS challenges: " + str(mar_num_lost_BS))

print("Jorge statistics for calling BS:")
print("\tWon BS challenges: " + str(jor_num_won_BS))
print("\tLost BS challenges: " + str(jor_num_lost_BS))

print("")
print("Terminator Wins: " + str(TerminatorWins))
print("Davis Wins: " + str(DavisWins))
print("Marl Wins: " + str(MarlWins))
print("Sven Wins: " + str(SvenWins))
print("Jorge Wins: " + str(JorgeWins))

